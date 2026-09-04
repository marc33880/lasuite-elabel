/**
 * Hostname-Router für die E-Label-Subdomains.
 *
 *   loure2024-nutri.lasuite.vin   ->  dist/loure2024-nutri/index.html
 *   <irgendwas>.lasuite.vin       ->  dist/index.html   (Übersicht, nie 404)
 *
 * Die Subdomain ist die einzige Adresse, die auf dem Etikett gedruckt ist.
 * Sie darf niemals ins Leere laufen — deshalb hat jeder unbekannte Hostname
 * eine gültige Antwort statt eines Fehlers.
 *
 * Zweiter Weg, absichtlich: liegt die Anfrage NICHT auf einer
 * *.lasuite.vin-Subdomain (workers.dev, Vorschau-URL, oder weil eine
 * Weiterleitung beim Registrar hierher zeigt), entscheidet der erste
 * Pfadabschnitt:
 *
 *   lasuite-elabel.<konto>.workers.dev/loure2024-nutri/  ->  dieselbe Seite
 *
 * Ohne diesen Weg liefe jede Registrar-Weiterleitung auf der Übersichtsseite
 * auf, nicht auf der Seite des Weins.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    // Assets (Schrift, Bilder) unverändert durchlassen
    if (url.pathname.startsWith('/assets/')) {
      return env.ASSETS.fetch(request);
    }

    let sub = host.endsWith('.lasuite.vin')
      ? host.slice(0, -'.lasuite.vin'.length)
      : '';
    if (sub === 'www') sub = '';

    // Auf einer Wein-Subdomain ist nur die Wurzel gültig; alles andere
    // wandert dorthin, damit eine krumm abgetippte URL nicht ins Leere läuft.
    if (sub && url.pathname !== '/') {
      return Response.redirect('https://' + host + '/', 301);
    }

    // Subdomain gewinnt; sonst entscheidet der erste Pfadabschnitt.
    const slug = sub || url.pathname.split('/').filter(Boolean)[0] || '';

    const target = new URL(request.url);
    target.pathname = slug ? '/' + slug + '/' : '/';

    let res = await env.ASSETS.fetch(new Request(target, request));

    // Unbekannte Subdomain -> Übersichtsseite ausliefern (Status 200)
    if (res.status === 404) {
      target.pathname = '/';
      res = await env.ASSETS.fetch(new Request(target, request));
    }

    const out = new Response(res.body, res);
    out.headers.set('Cache-Control', 'public, max-age=3600');
    out.headers.set('X-Content-Type-Options', 'nosniff');
    out.headers.set('Referrer-Policy', 'no-referrer');
    // Keine Analytics, keine Cookies, kein Fremd-Request: strikte CSP.
    out.headers.set(
      'Content-Security-Policy',
      "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; " +
      "script-src 'unsafe-inline'; font-src 'self'; base-uri 'none'; " +
      "form-action 'none'"
    );
    return out;
  },
};
