// Prefix internal paths with the site's base path (needed on GitHub Pages
// project sites like username.github.io/repo). External links pass through.
export function u(path: string = '/'): string {
  if (!path) return path;
  if (/^(https?:|mailto:|tel:|#)/.test(path)) return path;
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return base + (path.startsWith('/') ? path : '/' + path);
}

export const skillColour: Record<string, string> = {
  'Creative Direction': 'var(--cd)',
  'Ecosystem Design': 'var(--eco)',
  'Cultural Leadership': 'var(--cul)',
  'Campaign Marketing': 'var(--cam)',
};
