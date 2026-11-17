// v1.5 Session scenes: three full-bleed night worlds, drawn like the live site's Door.
(function(){
let seed=7;const r=()=>((seed=(seed*16807)%2147483647)-1)/2147483646;const f=n=>(+n).toFixed(1);
const W=1440,H=960;
const defs=`<defs>
<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070A22"/><stop offset=".35" stop-color="#121A55"/><stop offset=".62" stop-color="#2A2470"/><stop offset=".78" stop-color="#5A3478"/><stop offset=".88" stop-color="#9A5480"/><stop offset="1" stop-color="#D9907E"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2A74"/><stop offset=".25" stop-color="#1D2766"/><stop offset="1" stop-color="#070A1C"/></linearGradient>
<linearGradient id="pool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9EDCF2" stop-opacity=".9"/><stop offset=".1" stop-color="#5AA6DC"/><stop offset=".45" stop-color="#2D5DB0"/><stop offset="1" stop-color="#1A1F5E"/></linearGradient>
<linearGradient id="au1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#45E992" stop-opacity="0"/><stop offset=".25" stop-color="#7FD8F0" stop-opacity=".75"/><stop offset=".6" stop-color="#8FB4F6" stop-opacity=".6"/><stop offset=".85" stop-color="#A996FF" stop-opacity=".55"/><stop offset="1" stop-color="#E04BAE" stop-opacity="0"/></linearGradient>
<linearGradient id="au2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7C5CFF" stop-opacity="0"/><stop offset=".4" stop-color="#A996FF" stop-opacity=".55"/><stop offset=".75" stop-color="#7FD8F0" stop-opacity=".45"/><stop offset="1" stop-color="#7FD8F0" stop-opacity="0"/></linearGradient>
<linearGradient id="beam" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#FFF3E0" stop-opacity=".85"/><stop offset=".3" stop-color="#F2DDB4" stop-opacity=".35"/><stop offset="1" stop-color="#F2B48C" stop-opacity="0"/></linearGradient>
<linearGradient id="fall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE2C2" stop-opacity=".7"/><stop offset="1" stop-color="#F2B48C" stop-opacity="0"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#FFF3E0"/><stop offset=".35" stop-color="#F2B48C" stop-opacity=".7"/><stop offset="1" stop-color="#F2B48C" stop-opacity="0"/></radialGradient>
<radialGradient id="cool"><stop offset="0" stop-color="#CFE3FF" stop-opacity=".6"/><stop offset="1" stop-color="#CFE3FF" stop-opacity="0"/></radialGradient>
<radialGradient id="moon"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#F4F7FF"/><stop offset="1" stop-color="#DCE6FF"/></radialGradient>
<radialGradient id="hz" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F2B48C" stop-opacity=".55"/><stop offset=".5" stop-color="#E08C7E" stop-opacity=".2"/><stop offset="1" stop-color="#8A4C8E" stop-opacity="0"/></radialGradient>
<linearGradient id="skn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05081E"/><stop offset=".45" stop-color="#0E1548"/><stop offset=".8" stop-color="#1C1F62"/><stop offset="1" stop-color="#2A2470"/></linearGradient>
<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b18" x="-50%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="b40" x="-50%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="40"/></filter>
</defs>`;
const stars=(n,y1)=>{let o='';for(let i=0;i<n;i++){const big=r()<.12;o+=`<circle class="tw" style="animation-delay:-${f(r()*5)}s" cx="${f(r()*W)}" cy="${f(r()*y1)}" r="${big?1.6:.8}" fill="#fff" opacity="${f(.4+r()*.6)}"/>`}return o};
const aurora=(y,amp)=>`<g class="aur" filter="url(#b18)"><path d="M-100 ${y} C 300 ${y-amp}, 600 ${y+amp*.6}, 900 ${y-amp*.4} S 1400 ${y-amp}, 1600 ${y-amp*.2} L1600 ${y+120} C 1200 ${y+40}, 800 ${y+150}, 400 ${y+80} S 0 ${y+130}, -100 ${y+110} Z" fill="url(#au1)"/></g>
<g class="aur2" filter="url(#b40)"><path d="M-100 ${y+60} C 400 ${y-20}, 700 ${y+140}, 1100 ${y+40} S 1500 ${y+100}, 1600 ${y+60} L1600 ${y+200} L-100 ${y+220} Z" fill="url(#au2)"/></g>`;
const reflect=(cx,y0,y1,w,col)=>{let o='';for(let y=y0;y<y1;y+=7+r()*6){const t=(y-y0)/(y1-y0);const ww=w*(.4+t*1.4)*(.5+r()*.8);o+=`<line x1="${f(cx-ww/2+(r()-.5)*20)}" y1="${f(y)}" x2="${f(cx+ww/2+(r()-.5)*20)}" y2="${f(y)}" stroke="${col}" stroke-opacity="${f(.75-t*.6)}" stroke-width="${f(1.2+t*1.6)}" stroke-linecap="round"/>`}return `<g class="shim">${o}</g>`};
const fig=(x,y,s=1)=>`<g transform="translate(${x} ${y}) scale(${s})" fill="#04061A"><circle cx="0" cy="-46" r="8"/><path d="M-9 -37 L9 -37 L13 0 L5 0 L3 -14 L-2 0 L-12 0 Z"/></g>`;
const city=(x0,x1,base,hmax,dim)=>{let o='',w2='';let x=x0;while(x<x1){const w=18+r()*34,h=30+r()*hmax;o+=`<rect x="${f(x)}" y="${f(base-h)}" width="${f(w)}" height="${f(h)}"/>`;for(let wy=base-h+8;wy<base-6;wy+=9)for(let wx=x+4;wx<x+w-4;wx+=7)if(r()<dim)w2+=`<rect x="${f(wx)}" y="${f(wy)}" width="2.4" height="3" />`;x+=w+1+r()*3}return `<g fill="#0A0D2A">${o}</g><g fill="#F2DDB4" opacity=".75">${w2}</g>`};

// 1 · THE LIGHTHOUSE: a beam sweeping the sky, a lit path along the coast to the door at its foot
function lighthouse(){seed=11;const lx=1150,ly=372;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice">${defs}
<rect width="${W}" height="620" fill="url(#skn)"/>${stars(140,520)}${aurora(150,70)}
<ellipse cx="760" cy="616" rx="760" ry="40" fill="#3A3A8A" opacity=".35" filter="url(#b18)"/>
<g class="sweep" style="transform-origin:${lx}px ${ly}px"><path d="M${lx} ${ly-6} L-200 ${ly-170} L-200 ${ly+90} L${lx} ${ly+6} Z" fill="url(#beam)" filter="url(#b6)"/></g>
<rect y="618" width="${W}" height="${H-618}" fill="url(#sea)"/>
${reflect(lx,632,900,60,'#FFE2C2')}${reflect(420,632,760,40,'#BFD9FF')}
<path d="M860 640 C 940 560, 1010 520, 1080 510 C 1140 500, 1210 492, 1290 470 C 1360 452, 1420 440, 1500 436 L1500 ${H} L700 ${H} C 760 820, 800 720, 860 640 Z" fill="#05071C"/>
<rect x="${lx-14}" y="${ly}" width="28" height="140" fill="#0D1035"/><path d="M${lx-14} ${ly} L${lx+14} ${ly} L${lx+20} ${ly+142} L${lx-20} ${ly+142} Z" fill="#0D1035"/>
<g fill="#E9E6F5" opacity=".14"><rect x="${lx-16}" y="${ly+40}" width="32" height="10"/><rect x="${lx-18}" y="${ly+90}" width="36" height="10"/></g>
<rect x="${lx-10}" y="${ly-26}" width="20" height="26" fill="#FFF3E0"/><path d="M${lx-16} ${ly-26} L${lx} ${ly-44} L${lx+16} ${ly-26} Z" fill="#0D1035"/>
<circle class="br" cx="${lx}" cy="${ly-13}" r="70" fill="url(#warm)"/>
<path d="M${lx-11} ${ly+142} L${lx-11} ${ly+118} Q${lx} ${ly+106} ${lx+11} ${ly+118} L${lx+11} ${ly+142} Z" fill="#FFE2C2"/><ellipse class="br" cx="${lx}" cy="${ly+148}" rx="60" ry="14" fill="url(#warm)"/>
<path class="trail" d="M120 ${H} C 380 900, 560 860, 720 800 S 960 640, ${lx-6} ${ly+144}" fill="none" stroke="#FFE2C2" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="2 12" opacity=".9"/>
${[[470,872],[760,782],[1000,610]].map(([x,y],i)=>`<g class="lan" style="animation-delay:-${i*1.3}s"><circle cx="${x}" cy="${y}" r="34" fill="url(#warm)"/><circle cx="${x}" cy="${y}" r="3.5" fill="#FFF3E0"/></g>`).join('')}
${fig(1060,580,.9)}
</svg>`}

// 2 · THE LIT WINDOW: a sleeping city by the water, one window on, its light falling to the water and running to you
function windowCity(){seed=23;const wx=930,wy=300;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice">${defs}
<rect width="${W}" height="600" fill="url(#sk)"/>${stars(160,480)}${aurora(90,50)}
<circle cx="1240" cy="140" r="90" fill="url(#cool)" class="br"/><circle cx="1240" cy="140" r="26" fill="url(#moon)"/>
<ellipse cx="720" cy="596" rx="820" ry="60" fill="url(#hz)"/>
${city(-10,560,598,40,.05)}${city(1080,1460,598,190,.05)}
<rect x="590" y="598" width="490" height="2" fill="#0A0D2A"/>${city(600,850,598,120,.04)}${city(1010,1090,598,130,.04)}
<rect x="860" y="${wy-60}" width="150" height="${598-wy+60}" fill="#0C0F31"/><rect x="890" y="${wy-110}" width="90" height="56" fill="#0C0F31"/><rect x="933" y="${wy-170}" width="4" height="64" fill="#0C0F31"/>
<g fill="#F2DDB4" opacity=".35">${Array.from({length:40},(_,i)=>`<rect x="${872+(i%8)*16}" y="${wy+70+Math.floor(i/8)*42}" width="4" height="5"/>`).join('')}</g>
<rect x="${wx-28}" y="${wy-10}" width="56" height="72" fill="#FFF3E0"/><rect x="${wx-1}" y="${wy-10}" width="2" height="72" fill="#E0B48C"/><rect x="${wx-28}" y="${wy+24}" width="56" height="2" fill="#E0B48C"/>
<circle class="br" cx="${wx}" cy="${wy+26}" r="150" fill="url(#warm)" opacity=".85"/>
${fig(wx+8,wy+60,.42)}
<path d="M${wx-30} ${wy+62} L${wx+30} ${wy+62} L${wx+90} 600 L${wx-90} 600 Z" fill="url(#fall)" opacity=".35" filter="url(#b6)"/>
<rect y="600" width="${W}" height="${H-600}" fill="url(#sea)"/>
${reflect(wx,606,940,90,'#FFE2C2')}${reflect(1240,606,760,30,'#DCEBFF')}
<g opacity=".35" fill="#0A0D2A" transform="translate(0 1200) scale(1 -1)">${city(1080,1460,598,40,0)}</g>
</svg>`}

// 3 · THE PIER: under the aurora, a pier runs out over the pool to your door, lit at the end
function pier(){seed=5;const dx=720,dy=520;
const L=dx-46,R=dx+46,T=dy-118;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice">${defs}
<rect width="${W}" height="560" fill="url(#sk)"/>${stars(170,460)}${aurora(110,90)}${aurora(250,40)}
<ellipse cx="720" cy="556" rx="700" ry="56" fill="url(#hz)"/>
<rect y="556" width="${W}" height="${H-556}" fill="url(#pool)"/>
<rect y="556" width="${W}" height="${H-556}" fill="#070A1C" opacity=".35"/>
<g stroke="#E6F7FF" stroke-opacity=".16">${[600,650,710,790,880].map(y=>`<line x1="0" y1="${y}" x2="${W}" y2="${y}"/>`).join('')}</g>
<ellipse class="mist" cx="720" cy="560" rx="700" ry="16" fill="#BFD9FF" opacity=".3" filter="url(#b18)"/>
${reflect(dx,566,950,70,'#FFE2C2')}
<path d="M${dx-34} ${dy+4} L${dx+34} ${dy+4} L${dx+330} ${H} L${dx-330} ${H} Z" fill="#0A0C26"/>
<g stroke="#2A2F6E" stroke-width="1.2">${Array.from({length:14},(_,i)=>{const t=Math.pow((i+1)/14,1.8);const y=dy+4+t*(H-dy-4);const hw=34+t*296;return `<line x1="${f(dx-hw)}" y1="${f(y)}" x2="${f(dx+hw)}" y2="${f(y)}"/>`}).join('')}</g>
<path d="M${dx-34} ${dy+4} L${dx-330} ${H}" stroke="#4B4F9A" stroke-width="2"/><path d="M${dx+34} ${dy+4} L${dx+330} ${H}" stroke="#4B4F9A" stroke-width="2"/>
<path d="M${dx-20} ${dy+4} L${dx+20} ${dy+4} L${dx+180} ${H} L${dx-180} ${H} Z" fill="url(#fall)" opacity=".5" filter="url(#b6)"/>
${[[.18,1],[.42,-1],[.7,1]].map(([t,s],i)=>{const y=dy+4+t*(H-dy-4),x=dx+s*(34+t*296);const h=30+t*60;return `<rect x="${f(x-1.5)}" y="${f(y-h)}" width="${f(2+t*2)}" height="${f(h)}" fill="#04061A"/><g class="lan" style="animation-delay:-${i*1.2}s"><circle cx="${f(x)}" cy="${f(y-h)}" r="${f(26+t*30)}" fill="url(#warm)"/><circle cx="${f(x)}" cy="${f(y-h)}" r="${f(2+t*2.5)}" fill="#FFF3E0"/></g>`}).join('')}
<circle class="br" cx="${dx}" cy="${dy-50}" r="190" fill="url(#warm)" opacity=".75"/>
<path d="M${L} ${dy} L${L} ${T+40} Q${L} ${T} ${dx} ${T} Q${R} ${T} ${R} ${T+40} L${R} ${dy} Z" fill="#FFF3E0"/>
<path d="M${L} ${dy} L${L} ${T+40} Q${L} ${T} ${dx} ${T} Q${R} ${T} ${R} ${T+40} L${R} ${dy}" fill="none" stroke="#C9DCF7" stroke-width="3"/>
<path d="M${R} ${T+40} L${R+22} ${T+54} L${R+22} ${dy-4} L${R} ${dy}" fill="#0E0C2C" stroke="#A9B4E8" stroke-opacity=".6" stroke-width="1.5"/>
${fig(dx-30,dy+150,1.05)}
</svg>`}

// 4 · POP-UP: aurora over the water, a lit door far off on the horizon
function popsky(){seed=31;const W2=760,H2=300;
return `<svg viewBox="0 0 ${W2} ${H2}" preserveAspectRatio="xMidYMid slice"><defs>
<linearGradient id="ps-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#080C28"/><stop offset=".55" stop-color="#141C5A"/><stop offset="1" stop-color="#2A2470"/></linearGradient>
<linearGradient id="ps-a" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#45E992" stop-opacity="0"/><stop offset=".3" stop-color="#7FD8F0" stop-opacity=".7"/><stop offset=".65" stop-color="#8FB4F6" stop-opacity=".55"/><stop offset="1" stop-color="#A996FF" stop-opacity="0"/></linearGradient>
<linearGradient id="ps-b" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A996FF" stop-opacity="0"/><stop offset=".45" stop-color="#A996FF" stop-opacity=".55"/><stop offset=".8" stop-color="#7C5CFF" stop-opacity=".35"/><stop offset="1" stop-color="#7C5CFF" stop-opacity="0"/></linearGradient>
<filter id="ps-f" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="16"/></filter></defs>
<rect width="${W2}" height="${H2}" fill="url(#ps-sky)"/>
${(()=>{let o='';for(let i=0;i<90;i++)o+=`<circle class="tw" style="animation-delay:-${f(r()*5)}s" cx="${f(r()*W2)}" cy="${f(r()*H2)}" r="${r()<.12?1.3:.7}" fill="#fff" opacity="${f(.35+r()*.6)}"/>`;return o})()}
</svg>`}
// 5 · HERO FX: aurora, stars, a shooting star and light on the water, laid over the hero picture
function herofx(){seed=41;const W2=1440,H2=900;
let st='';for(let i=0;i<60;i++)st+=`<circle class="tw" style="animation-delay:-${f(r()*5)}s" cx="${f(r()*W2)}" cy="${f(r()*520)}" r="${r()<.15?1.4:.8}" fill="#fff" opacity="${f(.4+r()*.5)}"/>`;
let sh='';for(let y=612;y<760;y+=5+r()*6){const t2=(y-612)/148;const x=1160+r()*240;const w=(20+r()*50)*(1-t2*.4);sh+=`<line x1="${f(x)}" y1="${f(y)}" x2="${f(x+w)}" y2="${f(y)}" stroke="${r()<.5?'#F2DDB4':'#9EDCF2'}" stroke-opacity="${f(.45-t2*.3)}" stroke-width="1.2" stroke-linecap="round"/>`}
return `<svg viewBox="0 0 ${W2} ${H2}" preserveAspectRatio="xMidYMid slice">${defs}
${st}
<line class="shoot" x1="420" y1="70" x2="980" y2="250" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
<g class="shim">${sh}</g>
</svg>`}
const scenes={lighthouse,window:windowCity,pier,popsky,herofx};
document.querySelectorAll('[data-scene]').forEach(e=>{e.innerHTML=scenes[e.dataset.scene]()});
})();
