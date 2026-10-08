// Edge entry for loveikolabs.com: canonical host redirect, static assets, response headers.
// (With run_worker_first the _headers file is not applied, so headers live here.)
const SECURITY = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'SAMEORIGIN',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.loveikolabs.com') {
      url.hostname = 'loveikolabs.com';
      return Response.redirect(url.toString(), 301);
    }
    const res = await env.ASSETS.fetch(request);
    const out = new Response(res.body, res);
    for (const [k, v] of Object.entries(SECURITY)) out.headers.set(k, v);
    if (res.ok) {
      if (url.pathname.startsWith('/icons/')) out.headers.set('Cache-Control', 'public, max-age=2592000');
      else if (url.pathname === '/styles.css' || url.pathname === '/site.js') out.headers.set('Cache-Control', 'public, max-age=86400');
    }
    return out;
  },
};
