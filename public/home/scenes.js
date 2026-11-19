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

// Reflections only where a light is (Ashah 18 Nov): aurora = broad soft sheen; a point light = a column under it, narrow near the light, wider toward you
const aurRefl=(y0,h)=>{let o=`<g class="aref"><rect x="-100" y="${y0}" width="1640" height="${h}" fill="url(#au1)" opacity=".22" filter="url(#b18)"/></g>`;for(let i=0;i<16;i++){const y=y0+6+Math.pow(r(),1.3)*h,x=r()*1300,w=60+r()*220;o+=`<line class="rip" style="--dx:${f(r()*40-20)}px;animation-duration:${f(4+r()*4)}s;animation-delay:-${f(r()*6)}s" x1="${f(x)}" y1="${f(y)}" x2="${f(x+w)}" y2="${f(y)}" stroke="${r()<.5?'#7FD8F0':'#A996FF'}" stroke-opacity=".14" stroke-width="3" stroke-linecap="round"/>`}return o};
const colRefl=(cx,y0,y1,w,col,op)=>{let o='';for(let y=y0;y<y1;y+=5+r()*5){const t=(y-y0)/(y1-y0);const ww=w*(.25+t*1.2)*(.5+r()*.7);const x=cx-ww/2+(r()-.5)*w*.3*(t+.2);o+=`<line class="rip" style="--dx:${f((r()-.5)*8*(t+.3))}px;animation-duration:${f(2.5+r()*3)}s;animation-delay:-${f(r()*5)}s" x1="${f(x)}" y1="${f(y)}" x2="${f(x+ww)}" y2="${f(y)}" stroke="${col}" stroke-opacity="${f(op*(1-t*.6))}" stroke-width="${f(1.1+t*1.4)}" stroke-linecap="round"/>`}return o};
function lighthouse(){seed=11;const lx=1150,ly=372;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice">${defs}
<rect width="${W}" height="620" fill="url(#skn)"/>${stars(140,520)}${aurora(150,70)}
<ellipse cx="760" cy="616" rx="760" ry="40" fill="#3A3A8A" opacity=".35" filter="url(#b18)"/>
<g class="sweep" style="transform-origin:${lx}px ${ly}px"><path d="M${lx} ${ly-6} L-200 ${ly-170} L-200 ${ly+90} L${lx} ${ly+6} Z" fill="url(#beam)" filter="url(#b6)"/></g>
<rect y="618" width="${W}" height="${H-618}" fill="url(#sea)"/>
${aurRefl(624,150)}
<path d="M860 640 C 940 560, 1010 520, 1080 510 C 1140 500, 1210 492, 1290 470 C 1360 452, 1420 440, 1500 436 L1500 ${H} L700 ${H} C 760 820, 800 720, 860 640 Z" fill="#05071C"/>
<rect x="${lx-14}" y="${ly}" width="28" height="140" fill="#0D1035"/><path d="M${lx-14} ${ly} L${lx+14} ${ly} L${lx+20} ${ly+142} L${lx-20} ${ly+142} Z" fill="#0D1035"/>
<g fill="#E9E6F5" opacity=".14"><rect x="${lx-16}" y="${ly+40}" width="32" height="10"/><rect x="${lx-18}" y="${ly+90}" width="36" height="10"/></g>
<rect x="${lx-10}" y="${ly-26}" width="20" height="26" fill="#FFF3E0"/><path d="M${lx-16} ${ly-26} L${lx} ${ly-44} L${lx+16} ${ly-26} Z" fill="#0D1035"/>
<circle class="br" cx="${lx}" cy="${ly-13}" r="70" fill="url(#warm)"/>
<path d="M${lx-11} ${ly+142} L${lx-11} ${ly+118} Q${lx} ${ly+106} ${lx+11} ${ly+118} L${lx+11} ${ly+142} Z" fill="#FFE2C2"/><ellipse class="br" cx="${lx}" cy="${ly+148}" rx="60" ry="14" fill="url(#warm)"/>
<path class="trail" d="M120 ${H} C 380 900, 560 860, 720 800 S 960 640, ${lx-6} ${ly+144}" fill="none" stroke="#FFE2C2" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="2 12" opacity=".9"/>
${[[470,872],[760,782]].map(([x,y])=>colRefl(x,y+10,y+70,26,'#FFE2C2',.7)).join('')}${[[470,872],[760,782],[1000,610]].map(([x,y],i)=>`<g class="lan" style="animation-delay:-${i*1.3}s"><circle cx="${x}" cy="${y}" r="34" fill="url(#warm)"/><circle cx="${x}" cy="${y}" r="3.5" fill="#FFF3E0"/></g>`).join('')}
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
function herofx(){seed=41;const W2=1440,H2=900,HZ=646;
let st='';for(let i=0;i<110;i++){const big=r()<.14;st+=`<circle class="tw3" style="animation-duration:${f(2+r()*4)}s;animation-delay:-${f(r()*6)}s" cx="${f(r()*W2)}" cy="${f(r()*(HZ-60))}" r="${big?1.6:.9}" fill="#fff"/>`}
let sh='';for(const x of [1150,1200,1245,1290,1335,1380,1420])sh+=colRefl(x+r()*14,HZ+6,HZ+150+r()*60,22,r()<.65?'#F2DDB4':'#9EDCF2',.6);
return `<svg viewBox="0 0 ${W2} ${H2}" preserveAspectRatio="xMidYMid slice">${defs}
${st}
<line class="shoot" x1="420" y1="70" x2="980" y2="250" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
<g>${aurRefl(HZ+4,140)}${sh}</g>
</svg>`}
// 6 · THE NEXT MORNING (Session page, "What you leave with"): night lifting off the sea, first light on the horizon, the lighthouse still lit
function dawn(){seed=61;const lx=250,ly=560,hz=640;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMax slice">${defs}<defs>
<linearGradient id="dw-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070A22"/><stop offset=".45" stop-color="#121A55"/><stop offset=".72" stop-color="#2C2A78"/><stop offset=".86" stop-color="#5A4A9A"/><stop offset=".95" stop-color="#C79AB4"/><stop offset="1" stop-color="#FFD9B0"/></linearGradient>
<radialGradient id="dw-sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF3E0" stop-opacity=".95"/><stop offset=".25" stop-color="#FFD9B0" stop-opacity=".55"/><stop offset=".6" stop-color="#F2B48C" stop-opacity=".18"/><stop offset="1" stop-color="#F2B48C" stop-opacity="0"/></radialGradient>
<linearGradient id="dw-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6A5A9E"/><stop offset=".2" stop-color="#2A2A72"/><stop offset="1" stop-color="#070A1C"/></linearGradient></defs>
<rect width="${W}" height="${hz}" fill="url(#dw-sky)"/>${stars(150,380)}
<ellipse cx="900" cy="${hz}" rx="520" ry="210" fill="url(#dw-sun)"/>
<rect y="${hz}" width="${W}" height="${H-hz}" fill="url(#dw-sea)"/>
${colRefl(900,hz+4,H,170,'#FFE2C2',.8)}
<path d="M-20 ${hz+4} L-20 ${ly+40} C 80 ${ly+20}, 180 ${ly+6}, 300 ${ly+10} C 360 ${ly+12}, 400 ${ly+40}, 470 ${hz+4} Z" fill="#05071C"/>
<path d="M${lx-11} ${ly} L${lx+11} ${ly} L${lx+15} ${ly+70} L${lx-15} ${ly+70} Z" fill="#0D1035"/>
<rect x="${lx-7}" y="${ly-18}" width="14" height="18" fill="#FFF3E0"/><path d="M${lx-12} ${ly-18} L${lx} ${ly-31} L${lx+12} ${ly-18} Z" fill="#0D1035"/>
<circle cx="${lx}" cy="${ly-9}" r="46" fill="url(#warm)"/>
${colRefl(lx,hz+6,hz+120,22,'#FFE2C2',.55)}
<g stroke="#FFE2C2" stroke-opacity=".18">${[hz+30,hz+70,hz+130,hz+210].map(y=>`<line x1="0" y1="${y}" x2="${W}" y2="${y}"/>`).join('')}</g>
</svg>`}
// 7 · IT ARRIVES (Session page): a glowing parcel washed up on the shore under the stars, the lighthouse beam passing overhead
function parcel(){seed=71;const px=720,py=760,hz=600;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMax slice">${defs}<defs>
<linearGradient id="pc-sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A1A4A"/><stop offset="1" stop-color="#07081C"/></linearGradient></defs>
<rect width="${W}" height="${hz}" fill="url(#skn)"/>${stars(170,520)}${aurora(120,60)}
<g transform="translate(1300 ${hz-30})"><path d="M-8 0 L8 0 L10 30 L-10 30 Z" fill="#0D1035"/><rect x="-5" y="-12" width="10" height="12" fill="#FFF3E0"/><circle cx="0" cy="-6" r="30" fill="url(#warm)"/></g>
<path d="M1300 ${hz-36} L-200 ${hz-250} L-200 ${hz-150} Z" fill="url(#beam)" filter="url(#b6)" opacity=".7"/>
<rect y="${hz}" width="${W}" height="140" fill="url(#sea)"/>${aurRefl(hz+4,90)}
<path d="M0 ${hz+120} C 300 ${hz+100}, 600 ${hz+140}, 900 ${hz+118} S 1300 ${hz+110}, 1440 ${hz+124} L1440 ${H} L0 ${H} Z" fill="url(#pc-sand)"/>
<path d="M0 ${hz+122} C 300 ${hz+102}, 600 ${hz+142}, 900 ${hz+120} S 1300 ${hz+112}, 1440 ${hz+126}" fill="none" stroke="#C9DCF7" stroke-opacity=".35" stroke-width="2"/>
<circle cx="${px}" cy="${py}" r="210" fill="url(#warm)" opacity=".55"/>
<ellipse cx="${px}" cy="${py+34}" rx="120" ry="16" fill="#FFE2C2" opacity=".25" filter="url(#b6)"/>
<g transform="translate(${px} ${py}) rotate(-6)"><rect x="-62" y="-38" width="124" height="76" rx="6" fill="#FFF3E0"/><path d="M-62 -38 L0 6 L62 -38" fill="none" stroke="#E0B48C" stroke-width="3"/><rect x="-62" y="-38" width="124" height="76" rx="6" fill="none" stroke="#C9DCF7" stroke-width="2"/><circle cx="0" cy="6" r="7" fill="#F2B48C"/></g>
${[[420,820],[1010,800],[250,900],[1210,890]].map(([x,y],i)=>`<g class="lan" style="animation-delay:-${i*1.1}s"><circle cx="${x}" cy="${y}" r="18" fill="url(#warm)" opacity=".6"/><circle cx="${x}" cy="${y}" r="2" fill="#FFF3E0"/></g>`).join('')}
</svg>`}
// 8 · THE BEAM REACHES YOU (Session page): across the bay one small house, one lit window, and the lighthouse beam resting on it
function beamhome(){seed=81;const lx=180,ly=470,hx=1080,hy=640,hz=600;
return `<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMax slice">${defs}
<rect width="${W}" height="${hz}" fill="url(#skn)"/>${stars(170,520)}${aurora(110,60)}
<path d="M${lx} ${ly-12} L${hx+60} ${hy-70} L${hx+60} ${hy+10} Z" fill="url(#beam)" filter="url(#b6)" opacity=".85"/>
<rect y="${hz}" width="${W}" height="${H-hz}" fill="url(#sea)"/>${aurRefl(hz+4,140)}
<path d="M-20 ${hz+10} L-20 ${ly+40} C 60 ${ly+20}, 160 ${ly+6}, 260 ${ly+30} C 320 ${ly+50}, 360 ${hz-10}, 420 ${hz+10} Z" fill="#05071C"/>
<path d="M${lx-12} ${ly} L${lx+12} ${ly} L${lx+16} ${ly+90} L${lx-16} ${ly+90} Z" fill="#0D1035"/>
<rect x="${lx-8}" y="${ly-20}" width="16" height="20" fill="#FFF3E0"/><path d="M${lx-13} ${ly-20} L${lx} ${ly-34} L${lx+13} ${ly-20} Z" fill="#0D1035"/><circle cx="${lx}" cy="${ly-10}" r="54" fill="url(#warm)"/>
<path d="M860 ${hz+10} C 920 ${hy-10}, 1000 ${hy-30}, 1100 ${hy-26} C 1220 ${hy-22}, 1340 ${hy-6}, 1480 ${hy} L1480 ${H} L760 ${H} C 800 ${hz+120}, 830 ${hz+40}, 860 ${hz+10} Z" fill="#05071C"/>
<g transform="translate(${hx} ${hy-26})"><rect x="-46" y="-60" width="92" height="60" fill="#0D1035"/><path d="M-56 -60 L0 -100 L56 -60 Z" fill="#0D1035"/><rect x="-14" y="-44" width="28" height="24" fill="#FFF3E0"/><rect x="-1" y="-44" width="2" height="24" fill="#E0B48C"/></g>
<circle class="br" cx="${hx}" cy="${hy-58}" r="120" fill="url(#warm)" opacity=".8"/>
${colRefl(lx,hz+6,hz+150,24,'#FFE2C2',.55)}
</svg>`}
const scenes={lighthouse,window:windowCity,pier,popsky,herofx,dawn,parcel,beamhome};
document.querySelectorAll('[data-scene]').forEach(e=>{e.innerHTML=scenes[e.dataset.scene]()});
})();
