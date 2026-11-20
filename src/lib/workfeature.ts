// Home page "The work." section (20 Nov 2026, mock-up Home A v1.1, Ashah's pick).
// Tabs: New (the three newest = the first three by `order`), then one tab per category.
// 3+ pieces = Spotlight (one big, two beside); 1 piece = its cover whole on the left, its words on the right.
// The panel keeps one height on every tab so the page never jumps.
import { skillColour } from './url';

type Entry = { id: string; data: any };
const TABS = ['Brand Identity', 'Art Direction', 'Creative Strategy'] as const;
const esc = (t: string) => t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c] as string);

export function workFeature(work: Entry[], base: string, feedUrl: string): string {
  const u = (p: string) => (/^https?:/.test(p) ? p : base + p);
  const glow = (e: Entry) => e.data.glow || skillColour[e.data.skill] || '#8FB4F6';
  const live = (e: Entry) => (e.id === 'field-notes' && feedUrl ? ' data-live-cover' : '');
  const frame = (e: Entry, one: boolean) => {
    const img = esc(u(e.data.cover));
    const tall = e.data.coverRatio === 'portrait';
    if (tall || one) return `<div class="fr${tall ? ' tall' : ''}"><span class="bl" style="background-image:url('${img}')"></span><img src="${img}" alt="${esc(e.data.title)}" loading="lazy" decoding="async"${live(e)}></div>`;
    return `<div class="fr"><img src="${img}" alt="${esc(e.data.title)}" loading="lazy" decoding="async"${live(e)}></div>`;
  };
  const card = (e: Entry, cls: string) =>
    `<a class="cd ${cls}" href="${u(`/work/${e.id}/`)}" style="--c:${glow(e)}">${frame(e, cls === 'one')}<div class="in"><h3>${esc(e.data.title)}</h3><p>${esc(e.data.summary)}</p></div></a>`;
  const panel = (list: Entry[]) =>
    list.length >= 3 ? card(list[0], 'big') + card(list[1], 'sm') + card(list[2], 'sm')
    : list.length === 2 ? card(list[0], 'half') + card(list[1], 'half')
    : card(list[0], 'one');

  const tabs: [string, Entry[]][] = [['New', work.slice(0, 3)]];
  for (const t of TABS) { const l = work.filter((e) => e.data.category === t); if (l.length) tabs.push([t, l]); }

  const buttons = tabs.map(([n], i) => `<button type="button" role="tab" aria-selected="${i === 0}" class="${i === 0 ? 'on' : ''}" data-t="${i}">${n}</button>`).join('');
  const panels = tabs.map(([, l], i) => `<div class="g${i === 0 ? ' on' : ''}" role="tabpanel" data-t="${i}" data-n="${Math.min(l.length, 3)}">${panel(l)}</div>`).join('');
  const dots = '<i class="on"></i><i></i><i></i>';

  return `<style>
.hwk{padding:40px 96px 120px;position:relative}
.hwk .ih{display:flex;justify-content:space-between;align-items:center;gap:40px;margin-bottom:34px}
.hwk h2{font-size:54px!important;margin:0!important;line-height:1.2}
.hwk .wtabs{display:flex;padding:5px;border-radius:999px;background:rgba(12,16,48,.7);border:1px solid rgba(159,182,236,.28);box-shadow:inset 0 1px 0 rgba(255,255,255,.05)}
.hwk .wtabs button{font:inherit;border:0;background:none;cursor:pointer;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#C9CFEA;padding:13px 22px;border-radius:999px;transition:color .4s,background .4s,box-shadow .4s}
.hwk .wtabs button:hover{color:#F6F1E7}
.hwk .wtabs button.on{color:#06081A;font-weight:600;background:linear-gradient(90deg,#8FB3F6,#9EA1FB 50%,#A498FE 75%,#B49AD8);box-shadow:0 0 22px rgba(127,216,240,.5),0 0 50px rgba(169,150,255,.3)}
.hwk .pn{position:relative}
.hwk .g{display:none;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:20px;height:100%}
.hwk .g.on{display:grid;animation:hwkIn .7s ease-out}
@keyframes hwkIn{from{opacity:0;transform:translateY(10px)}}
.hwk .cd{display:flex;flex-direction:column;background:#0C1030;border:1px solid rgba(246,241,231,.14);border-radius:6px;overflow:hidden;box-shadow:0 34px 80px -50px var(--c);transition:box-shadow .6s,border-color .6s}
.hwk .cd:hover{box-shadow:0 40px 100px -40px var(--c);border-color:rgba(246,241,231,.24)}
.hwk .fr{position:relative;overflow:hidden;background:#05071A}
.hwk .fr img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 1.4s cubic-bezier(.2,.7,.2,1)}
.hwk .cd:hover .fr img{transform:scale(1.03)}
.hwk .fr:after{content:"";position:absolute;inset:auto 0 0 0;height:1px;background:linear-gradient(90deg,transparent,var(--c),transparent);z-index:2}
.hwk .fr.tall img,.hwk .one .fr img{position:relative;z-index:1;object-fit:contain}
.hwk .fr .bl{position:absolute;inset:-30px;background:center/cover;filter:blur(30px) saturate(1.3) brightness(.5)}
.hwk .big{grid-row:1/3}.hwk .big .fr{flex:1;min-height:0}
.hwk .sm .fr,.hwk .half .fr{aspect-ratio:16/9}
.hwk .half{grid-row:1/3}.hwk .g[data-n="2"]{grid-template-columns:1fr 1fr}
.hwk .in{padding:22px 24px}
.hwk h3{font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:400;color:#F6F1E7;text-transform:none;letter-spacing:0;font-size:30px;line-height:1.2;margin:0 0 6px}
.hwk .big h3,.hwk .one h3{font-size:44px;line-height:1.1}
.hwk p{color:#C9CFEA;font-size:14px;line-height:21px;margin:0}.hwk .big p,.hwk .one p{font-size:16px;line-height:24px}
.hwk .one{grid-column:1/-1;grid-row:1/3;display:grid;grid-template-columns:calc((100% - 20px)*2/3) 1fr;column-gap:20px;background:none;border:0;box-shadow:none;overflow:visible}
.hwk .one:hover{box-shadow:none}
.hwk .one .fr{height:100%;border:1px solid rgba(246,241,231,.14);border-radius:6px;box-shadow:0 34px 80px -50px var(--c)}
.hwk .one .in{display:flex;flex-direction:column;justify-content:flex-end;background:radial-gradient(ellipse 120% 70% at 50% 0,color-mix(in srgb,var(--c) 22%,transparent),transparent 70%),#0C1030;border:1px solid rgba(246,241,231,.14);border-radius:6px;padding:28px 24px}
.hwk .more{display:flex;justify-content:flex-end;margin-top:30px}
.hwk .fl{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#F6F1E7;white-space:nowrap}.hwk .fl:hover{color:var(--peach,#F2B48C)}
.hwk .wdots{display:none}
@media (max-width:600px){.hwk{padding:30px 18px 70px}.hwk h2{font-size:38px!important}
.hwk .ih{flex-direction:column;align-items:flex-start;gap:20px;margin-bottom:24px}
.hwk .wtabs{display:grid;grid-template-columns:1fr 1fr;border-radius:22px;width:100%}.hwk .wtabs button{padding:12px 0;font-size:10px;letter-spacing:.18em}
.hwk .g,.hwk .g[data-n="2"]{grid-template-columns:none;grid-template-rows:none;gap:14px;margin:0 -18px;padding:0 18px 4px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.hwk .g::-webkit-scrollbar{display:none}
.hwk .g.on{display:flex}
.hwk .cd,.hwk .one{flex:0 0 84%;scroll-snap-align:center;grid-row:auto;grid-column:auto;display:flex;flex-direction:column;background:#0C1030;border:1px solid rgba(246,241,231,.14);border-radius:6px;overflow:hidden}
.hwk .g[data-n="1"] .one{flex:0 0 100%}
.hwk .big .fr,.hwk .one .fr{flex:none;height:auto;aspect-ratio:16/9;border:0;border-radius:0;box-shadow:none}
.hwk .one .in{flex:1;justify-content:flex-start;border:0;border-radius:0;padding:22px 24px}
.hwk .big h3,.hwk .one h3{font-size:30px;line-height:1.2}.hwk .big p,.hwk .one p{font-size:14px;line-height:21px}
.hwk .wdots{display:flex;justify-content:center;gap:8px;margin-top:22px}.hwk .wdots i{width:6px;height:6px;border-radius:9px;background:rgba(246,241,231,.3);transition:width .3s}.hwk .wdots i.on{width:22px;background:#C9DCF7}.hwk .wdots.hide{visibility:hidden}
.hwk .more{justify-content:center;margin-top:22px}}
</style>
<section class="hwk" id="work"><div class="ih"><h2 class="ser">The work.</h2><div class="wtabs" role="tablist" aria-label="The work">${buttons}</div></div><div class="pn">${panels}</div><div class="wdots">${dots}</div><div class="more"><a class="fl" href="${u('/work/')}">All work →</a></div></section>
<script>(function(){var s=document.getElementById('work');if(!s)return;var bs=s.querySelectorAll('.wtabs button'),gs=s.querySelectorAll('.pn .g'),pn=s.querySelector('.pn'),d=s.querySelector('.wdots'),dd=d.children;
function ph(){return window.innerWidth<=600}
function fit(){pn.style.height='auto';var h=0;gs.forEach(function(g,i){if(!ph()&&i)return;g.style.display=ph()?'flex':'grid';h=Math.max(h,g.offsetHeight);g.style.display='';});pn.style.height=h+'px';}
function dots(){var g=s.querySelector('.pn .g.on'),n=g.children.length;d.classList.toggle('hide',n<2);for(var i=0;i<dd.length;i++)dd[i].style.display=i<n?'':'none';var k=Math.round(g.scrollLeft/((g.children[0]||g).offsetWidth+14));for(var j=0;j<dd.length;j++)dd[j].classList.toggle('on',j===Math.min(k,n-1));}
gs.forEach(function(g){g.addEventListener('scroll',dots,{passive:true})});
bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on)});gs.forEach(function(g){var on=g.dataset.t===b.dataset.t;g.classList.toggle('on',on);if(on)g.scrollLeft=0});dots();});});
fit();dots();window.addEventListener('resize',fit);window.addEventListener('load',fit);s.querySelectorAll('img').forEach(function(i){if(!i.complete)i.addEventListener('load',fit,{once:true})});
// Field Notes: the first slide of the latest Field Notes carousel, live from Instagram (same rule as /work/)
var lv=s.querySelectorAll('img[data-live-cover]');if(lv.length&&${JSON.stringify(feedUrl)}){fetch(${JSON.stringify(feedUrl)}).then(function(r){return r.json()}).then(function(dt){var ps=Array.isArray(dt)?dt:(dt.posts||[]);var end=Date.parse('2026-11-09T00:00:00+11:00');var c=ps.filter(function(p){return p.mediaType==='CAROUSEL_ALBUM'&&!(p.timestamp&&Date.parse(p.timestamp)>=end)})[0];if(!c)return;var k=(c.children&&c.children[0])||c;var src=(k.sizes&&k.sizes.large&&k.sizes.large.mediaUrl)||k.mediaUrl||k.thumbnailUrl;if(!src)return;lv.forEach(function(i){i.src=src;var b=i.parentNode.querySelector('.bl');if(b)b.style.backgroundImage="url('"+src+"')"})}).catch(function(){})}
})();</script>`;
}
