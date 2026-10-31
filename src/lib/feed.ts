// The live Instagram feed (Behold JSON, site.json → instagramFeedUrl), loaded once per page in the visitor's browser.
// Field Notes and the home feed both read from it, so new posts show up without rebuilding the site.
export type Post = {
  id?: string; permalink: string; timestamp?: string; mediaType?: string;
  mediaUrl?: string; thumbnailUrl?: string; caption?: string; prunedCaption?: string;
  sizes?: Record<string, { mediaUrl?: string }>; children?: Post[];
};

export function loadFeed(url: string): Promise<Post[]> {
  const w = window as unknown as { __amwFeed?: Record<string, Promise<Post[]>> };
  w.__amwFeed ??= {};
  w.__amwFeed[url] ??= fetch(url)
    .then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
    .then((d) => (Array.isArray(d) ? d : d.posts ?? []) as Post[]);
  return w.__amwFeed[url];
}

export const imageOf = (p: Post) =>
  p.sizes?.large?.mediaUrl || p.sizes?.medium?.mediaUrl || (p.mediaType === 'VIDEO' ? p.thumbnailUrl : p.mediaUrl) || p.thumbnailUrl || '';

// Field Notes are the carousel posts on Instagram, newest first. The series ends with the November 2026 posts
// (Ashah, 31 Oct 2026): anything posted after 30 Nov (Melbourne time) is never treated as a Field Note.
export const FIELD_NOTES_END = Date.parse('2026-12-01T00:00:00+11:00');
export const carousels = (posts: Post[]) =>
  posts.filter((p) => p.mediaType === 'CAROUSEL_ALBUM' && !(p.timestamp && Date.parse(p.timestamp) >= FIELD_NOTES_END));
export const slidesOf = (p: Post) => (p.children?.length ? p.children : [p]).filter((c) => c.mediaType !== 'VIDEO' || c.thumbnailUrl).map(imageOf).filter(Boolean);
export const firstLine = (p: Post, max = 90) => (p.prunedCaption || p.caption || '').split('\n')[0].slice(0, max);

export const esc = (t: string) => t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c] as string);
