import os,sys
OUT=sys.argv[1]; BASE=sys.argv[2] if len(sys.argv)>2 else '/ashah-world'
G=lambda t:f'<span class="gap">[{t}]</span>'
IG=('https://www.instagram.com/ashah.world/','<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/>')
HEAD=lambda title,extra='':f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>{title}</title><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#070A1C"><link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{BASE}/home/base.css"><style>{CSS}{extra}</style></head><body>'''
CSS='''
.gap{color:#0B0E22;background:var(--peach);border-radius:4px;padding:0 6px;font-style:normal;font-family:'DM Sans',sans-serif;font-size:.8em}
.mk{position:fixed;top:22px;left:56px;z-index:20;font-size:12px;letter-spacing:.3em;color:#C9CFEA}
h1,h2,h3{font-weight:400}
.aurb{display:inline-block;border-radius:999px;padding:18px 34px;font-size:13px;letter-spacing:.24em;text-transform:uppercase;font-weight:600;color:#06081A;background:linear-gradient(90deg,#8FB3F6,#9EA1FB 50%,#A498FE 75%,#B49AE9);box-shadow:0 0 30px rgba(127,216,240,.6),0 0 80px rgba(169,150,255,.4);animation:br 4.5s ease-in-out infinite}
@keyframes br{50%{box-shadow:0 0 40px rgba(127,216,240,.75),0 0 110px rgba(169,150,255,.5)}}
.free{display:inline-block;margin-bottom:22px;padding:8px 16px 8px 18px;border-radius:999px;font-size:14px;font-weight:500;letter-spacing:.34em;text-transform:uppercase;color:#fff;background:linear-gradient(100deg,rgba(127,216,240,.22),rgba(169,150,255,.22));box-shadow:inset 0 0 0 1px rgba(207,230,255,.45),0 0 24px rgba(127,216,240,.28);text-shadow:0 0 12px rgba(207,230,255,.8)}
.hero{position:relative;height:920px;overflow:hidden}
.hero .bg,.hero .bg svg{position:absolute;inset:0;width:100%;height:100%}
.hero .fade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,10,28,.3) 0,rgba(7,10,28,0) 20%,rgba(7,10,28,0) 70%,var(--bg) 100%);pointer-events:none}
.hero .txt{position:absolute;left:96px;bottom:150px;z-index:2;max-width:900px}
.hero h1{font-size:88px;line-height:.98;margin-bottom:26px;text-shadow:0 2px 30px rgba(7,10,28,.6)}
h1 em,h2 em{background:linear-gradient(90deg,#7FD8F0,#8FB4F6 45%,#A996FF);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{font-size:20px;line-height:1.6;color:#DCE1F5;max-width:560px;margin-bottom:34px;text-shadow:0 1px 16px rgba(7,10,28,.8)}
.sec{padding:120px 96px;position:relative}
.sec h2{font-size:54px;line-height:1.05;margin-bottom:22px}
.sec p.lead{font-size:19px;line-height:1.65;color:#D9DDF0;max-width:640px}
.fab{position:fixed;left:50%;bottom:28px;transform:translate(-50%,40px);opacity:0;pointer-events:none;z-index:30;transition:opacity .45s,transform .45s}
.fab.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
.end{text-align:center;padding:160px 24px 180px;position:relative;overflow:hidden}
.end:before{content:'';position:absolute;left:50%;top:40%;width:900px;height:500px;transform:translate(-50%,-50%);background:radial-gradient(ellipse,rgba(169,150,255,.22),transparent 60%);filter:blur(10px)}
.end h2{font-size:72px;line-height:1.02;margin-bottom:24px;position:relative}.end p{position:relative;color:#C9CFEA;font-size:18px;margin-bottom:38px}
.end .aurb{position:relative}
.foot{display:flex;justify-content:center;gap:22px;padding:0 0 56px}
.foot a{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;color:#C9CFEA;border:1px solid var(--line)}.foot svg{width:19px;height:19px}
@media (max-width:600px){.mk{left:18px}.hero{height:940px}.hero .txt{left:18px;right:18px;bottom:90px}.hero h1{font-size:56px}.hero p{font-size:17px}.sec{padding:80px 18px}.sec h2{font-size:38px}.end h2{font-size:46px}.aurb{padding:16px 26px;font-size:12px}}
'''
FAB_JS='''<script>(function(){var f=document.querySelector('.fab'),h=document.querySelector('.hero'),e=document.querySelector('.end');if(!f)return;var top=true,bot=false;function u(){f.classList.toggle('on',!top&&!bot)}
new IntersectionObserver(function(x){top=x[0].isIntersecting;u()},{threshold:.15}).observe(h);new IntersectionObserver(function(x){bot=x[0].isIntersecting;u()},{threshold:.05}).observe(e)})();</script>'''
SOC=[('Instagram','https://www.instagram.com/ashah.world/','<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/>'),('LinkedIn','https://www.linkedin.com/in/ashahpeters/','<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V17M8 7.2v.1M11.5 17v-6.5M11.5 13.2c0-1.6 1.2-2.7 2.6-2.7s2.4 1 2.4 2.7V17"/>')]
FOOT='<div class="foot">'+''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{k}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{s}</svg></a>' for k,u,s in SOC)+'</div>'
APPLY=f'{BASE}/session/apply/'
HERO=f'''<a class="mk" href="{BASE}/">A·M·W</a><section class="hero"><div class="bg" data-scene="lighthouse"></div><div class="fade"></div><div class="txt"><span class="free">Free</span><h1 class="ser">Bring me your brand.<br><em>I'll show you its world.</em></h1><p>One Brand Strategy Session. 45 minutes, one on one. We find where your brand is, where it should be going, and the one move that closes the gap.</p><a class="aurb" href="{APPLY}">Apply now</a></div></section>'''
END=f'''<section class="end"><h2 class="ser">The light's on.<br><em>Come up to the door.</em></h2><p>I open the door ten times a month. One Session per brand. All I ask back is honest feedback.</p><a class="aurb" href="{APPLY}">Apply now</a></section>'''+FOOT
TAIL=f'''<a class="aurb fab" href="{APPLY}">Apply now</a><script src="{BASE}/home/scenes.js"></script><script>if(innerWidth<600)document.querySelectorAll('[data-scene="lighthouse"] svg').forEach(v=>{{v.setAttribute("viewBox","880 150 540 940");v.setAttribute("preserveAspectRatio","xMidYMin slice")}})</script>{FAB_JS}</body></html>'''
PILLARS=['Identity','Storytelling','Product','Ecosystem','Continuity','Campaigns']
PCOL={'Identity':'#F2CF9A','Storytelling':'#B9A4FF','Product':'#F2A47A','Ecosystem':'#5FE3D0','Continuity':'#E88C96','Campaigns':'#5BE38E'} # each workbook's own colour (Ashah 19 Nov)
PC=lambda p:f' style="color:{PCOL[p]};text-shadow:0 0 18px {PCOL[p]}66"><i class="orb" style="background:{PCOL[p]};box-shadow:0 0 10px 2px {PCOL[p]}99,0 0 26px 6px {PCOL[p]}44"></i'
WB={'Identity':'identity','Storytelling':'storytelling','Product':'product','Ecosystem':'ecosystem','Continuity':'continuity','Campaigns':'campaigns'}
THREE=[('Where you are','We read your brand across six pillars, and find what’s carrying it and what’s holding it back.'),('Where it’s going','The world your brand could be. What people would step into, and the gap between here and there.'),('The one move','The single change that closes the gap first, and exactly how to make it.')]
STEPS=[('Apply','Eight minutes. Tell me about your brand and where you want it to go.'),('You’re in','I read every application myself. Within three days, your yes lands with a private link to book.'),('Pick a time','45 minutes, booked at least three days ahead. Ten a month, so the early ones go first.'),('Prep','The moment you book, a five-minute form opens on your day, so we go straight to depth.'),('The Session','One on one on Cal Video, recorded so your pack is made properly. Bring the one thing you most want to move.'),('Your pack','The next day, your Session Pack lands in your inbox.')]
WHO='For founders building a brand with culture at its centre. Labels, studios, venues, artists. People don’t just buy from you, they want to belong to what you’re making. You’re ready to make that world as strong as the product.'
LEAVE='The next day, your Session Pack lands in your inbox. I rewatch our call and build it around your brand alone: the read across all six pillars, where your brand should be going, and the one move, laid out step by step so you can start that week.'
AFTER='Then the path is yours. Walk it on your own with the pack, or with me, month by month.'  # 23 Nov 2026: the Season offer is retired

# ---------- A: The path ----------
A_CSS='''
.path{position:relative;padding:60px 96px 40px}
.path:before{content:'';position:absolute;left:111px;top:0;bottom:0;width:0;border-left:2px dotted rgba(255,226,194,.55);filter:drop-shadow(0 0 6px rgba(242,180,140,.6))}
.stop{position:relative;padding:0 0 120px 80px;max-width:900px}
.stop:before{content:'';position:absolute;left:4px;top:18px;width:24px;height:24px;border-radius:50%;background:#FFF3E0;box-shadow:0 0 14px 4px rgba(255,226,194,.85),0 0 60px 18px rgba(242,180,140,.4)}
.stop h2{font-size:54px;line-height:1.05;margin-bottom:22px}
.stop p{font-size:19px;line-height:1.65;color:#D9DDF0;max-width:640px}
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:40px;max-width:1000px}
.trio b{display:block;font-family:'Cormorant Garamond';font-style:italic;font-weight:400;font-size:30px;margin-bottom:10px;color:#F7F5F0}
.trio p{font-size:16px!important;color:#C9CFEA!important}
.pills{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:16px 34px;margin-top:30px}.pills span{font-family:'Cormorant Garamond';font-style:italic;font-size:22px;color:#E6E9F7}
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:30px;margin-top:40px;max-width:1100px}
.steps b{display:block;font-family:'Cormorant Garamond';font-style:italic;font-weight:400;font-size:28px;margin-bottom:8px}.steps p{font-size:15px!important;color:#C9CFEA!important}
@media (max-width:600px){.pills{grid-template-columns:repeat(2,150px)}.path{padding:40px 18px}.path:before{left:29px}.stop{padding:0 0 80px 46px}.stop:before{left:0}.stop h2{font-size:38px}.trio,.steps{grid-template-columns:1fr;gap:22px}}
'''
def A():
  s=HERO+'<div class="path">'
  s+=f'<div class="stop"><h2 class="ser">Who it’s for.</h2><p>{WHO}</p></div>'
  s+='<div class="stop"><h2 class="ser">45 minutes, three turns of the beam.</h2><div class="trio">'+''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a,b in THREE)+'</div></div>'
  s+='<div class="stop"><h2 class="ser">Six pillars, one read.</h2><p>Every brand that lasts is built on the same six. We read all six, so you see the whole picture.</p><div class="pills">'+''.join(f'<span{PC(p)}>{p}</span>' for p in PILLARS)+'</div></div>'
  s+=f'<div class="stop"><h2 class="ser">What you leave with.</h2><p>{LEAVE}</p><p style="margin-top:18px">{AFTER}</p></div>'
  s+='<div class="stop" style="padding-bottom:40px"><h2 class="ser">How you get in.</h2><div class="steps">'+''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a,b in STEPS)+'</div></div>'
  s+='</div>'+END+TAIL
  return HEAD('The Session · Ashah Meets World',A_CSS)+s

# ---------- B: The briefing ----------
B_CSS='''
.split{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
.time{margin-top:10px;border-top:1px solid var(--line)}
.time .row{display:grid;grid-template-columns:150px 1fr;gap:30px;padding:30px 0;border-bottom:1px solid var(--line)}
.time .m{font-family:'Cormorant Garamond';font-style:italic;font-size:30px;color:#9EDCF2}
.time b{display:block;font-family:'Cormorant Garamond';font-style:italic;font-weight:400;font-size:32px;margin-bottom:8px}.time p{color:#C9CFEA;font-size:16px;line-height:1.6}
.grid6{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:44px}
.grid6 div{aspect-ratio:16/9;border-radius:6px;border:1px solid var(--line);background:center/cover;position:relative;overflow:hidden}
.grid6 span{position:absolute;left:0;right:0;bottom:0;padding:40px 14px 14px;background:linear-gradient(transparent,rgba(7,10,28,.9));font-family:'Cormorant Garamond';font-style:italic;font-size:22px}
.leave{border-radius:10px;padding:56px;background:linear-gradient(160deg,#141A44,#0C1030);border:1px solid rgba(242,180,140,.35);box-shadow:0 0 80px rgba(242,180,140,.12)}
.leave h2{font-size:46px}
.steps4{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-top:44px}
.steps4 div{padding:30px;border-radius:8px;border:1px solid var(--line);background:rgba(246,241,231,.03)}
.steps4 b{display:block;font-family:'Cormorant Garamond';font-style:italic;font-weight:400;font-size:28px;margin-bottom:10px}.steps4 p{color:#C9CFEA;font-size:15px;line-height:1.6}
.faq{max-width:860px}.faq details{border-bottom:1px solid var(--line);padding:26px 0}.faq summary{cursor:pointer;list-style:none;font-family:'Cormorant Garamond';font-style:italic;font-size:28px;display:flex;justify-content:space-between}.faq summary:after{content:'+';color:var(--peach)}.faq details[open] summary:after{content:'−'}.faq p{margin-top:14px;color:#C9CFEA;font-size:16px;line-height:1.65;max-width:700px}
@media (max-width:600px){.split{grid-template-columns:1fr;gap:30px}.time .row{grid-template-columns:1fr;gap:6px}.grid6{grid-template-columns:1fr}.leave{padding:30px 22px}.leave h2{font-size:34px}.steps4{grid-template-columns:1fr}.faq summary{font-size:23px}}
'''
FAQ=[('Is it really free?','Yes. 45 minutes, one on one, and the Session Pack is yours to keep. All I ask back is honest feedback.'),('What do I need to bring?','Your brand, open. Your site, your socials, and the thing you’re stuck on. The form covers the rest.'),('Why do I have to apply?','Because I only open the door ten times a month, and I want every one to count. The form tells me where to point the beam.'),('Can I come back?','One Session per brand. Once a year has passed, the door opens again.'),('What happens after?',AFTER)]
def B():
  s=HERO
  s+=f'<section class="sec"><div class="split"><h2 class="ser">Who it’s for.</h2><p class="lead">{WHO}</p></div></section>'
  s+='<section class="sec" style="padding-top:40px"><h2 class="ser">How the 45 minutes run.</h2><div class="time">'+''.join(f'<div class="row"><span class="m">{m}</span><div><b>{a}</b><p>{b}</p></div></div>' for m,(a,b) in zip(['0 to 15','15 to 30','30 to 45'],THREE))+'</div></section>'
  s+='<section class="sec" style="padding-top:40px"><h2 class="ser">Read across six pillars.</h2><p class="lead">The same six every brand that lasts is built on. The free workbooks go deep on each one. The Session reads all six at once.</p><div class="grid6">'+''.join(f'<a href="{BASE}/resources/{WB[p]}/" style="display:block"><div style="background-image:url({BASE}/home/wb-{WB[p]}.webp)"></div></a>' for p in PILLARS)+'</div></section>'
  s+=f'<section class="sec" style="padding-top:40px"><div class="leave"><h2 class="ser">What you leave with.</h2><p class="lead">{LEAVE}</p></div></section>'
  s+='<section class="sec" style="padding-top:40px"><h2 class="ser">How you get in.</h2><div class="steps4">'+''.join(f'<div><b>{a}</b><p>{b}</p></div>' for a,b in STEPS)+'</div></section>'
  s+='<section class="sec" style="padding-top:40px"><h2 class="ser">Questions.</h2><div class="faq">'+''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(FAQ))+'</div></section>'
  s+=END+TAIL
  return HEAD('The Session · Ashah Meets World',B_CSS)+s

# ---------- C: Night scenes ----------
C_CSS='''
.orb{display:inline-block;flex:none;width:11px;height:11px;border-radius:50%;margin-right:16px}.ring span,.pills span{display:inline-flex;align-items:center}
.scene{position:relative;min-height:760px;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 24px;overflow:hidden}.scene .sb,.scene .sb svg{position:absolute;inset:0;width:100%;height:100%}.scene .glow{position:absolute;left:50%;top:50%;width:1000px;height:600px;transform:translate(-50%,-50%);background:radial-gradient(ellipse,rgba(127,216,240,.12),rgba(169,150,255,.08) 40%,transparent 70%)}
.scene:before{content:'';position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,var(--bg) 0,rgba(7,10,28,.55) 22%,rgba(7,10,28,.55) 78%,var(--bg) 100%)}
.scene .in{position:relative;z-index:2;max-width:900px}
.scene h2{font-size:64px;line-height:1.02;margin-bottom:24px;text-shadow:0 2px 30px rgba(7,10,28,.7)}
.scene p{font-size:19px;line-height:1.65;color:#E2E6F6;text-shadow:0 1px 16px rgba(7,10,28,.9)}
.beam3{display:flex;justify-content:center;gap:56px;margin-top:44px;position:relative}
.beam3:before{content:'';position:absolute;left:12%;right:12%;top:7px;height:1px;background:linear-gradient(90deg,#FFE2C2,#7FD8F0,#A996FF);box-shadow:0 0 10px #7FD8F0}
.beam3 div{position:relative;padding-top:30px;width:200px}.beam3 i{position:absolute;left:50%;top:0;width:15px;height:15px;margin-left:-7px;border-radius:50%;background:#FFF3E0;box-shadow:0 0 12px 3px rgba(255,226,194,.8),0 0 40px 10px rgba(242,180,140,.45)}
.beam3 b{display:block;font-family:'Cormorant Garamond';font-style:italic;font-weight:400;font-size:26px;margin-bottom:8px}.beam3 span{font-size:14px;color:#C9CFEA;line-height:1.55;display:block}
.ring{display:grid;grid-template-columns:repeat(3,max-content);justify-content:center;justify-items:start;gap:18px 72px;margin-top:34px;font-family:'Cormorant Garamond';font-style:italic;font-size:30px;color:#F7F5F0}

@media (max-width:600px){.scene{min-height:640px;padding:90px 18px}.scene h2{font-size:42px}.beam3{flex-direction:column;gap:26px;align-items:center}.beam3:before{display:none}.ring{font-size:24px}}
'''
def C():
  sc=lambda img,h,body:f'<section class="scene">'+(f'<div class="sb" data-scene="{img}"></div>' if img else '<div class="glow"></div>')+f'<div class="in"><h2 class="ser">{h}</h2>{body}</div></section>'
  s=HERO
  s+=sc('window','Who it’s for.',f'<p>{WHO}</p>')
  s+=sc('popsky','45 minutes.<br><em>Three turns of the beam.</em>','<div class="beam3">'+''.join(f'<div><i></i><b>{a}</b><span>{b}</span></div>' for a,b in THREE)+'</div>')
  s+=sc('','Six pillars, <em>one read.</em>','<p>Every brand that lasts is built on the same six. We read all six, so you see the whole picture.</p><div class="ring">'+''.join(f'<span{PC(p)}>{p}</span>' for p in PILLARS)+'</div>')
  s+=sc('','What you leave with.',f'<p>{LEAVE}</p><p style="margin-top:16px">{AFTER}</p>')
  s+=sc('','How you get in.','<div class="beam3" style="gap:24px">'+''.join(f'<div style="width:180px"><i></i><b>{a}</b><span>{b}</span></div>' for a,b in STEPS)+'</div>')
  s+=END+TAIL
  return HEAD('The Session · Ashah Meets World',C_CSS)+s

# ---------- Apply form ----------
F_CSS='''
.thanks{display:none;text-align:center;padding-top:60px}.thanks p{font-size:18px;line-height:1.65;color:#D9DDF0;margin:0 auto 40px;max-width:560px}body.sent form,body.sent .fwrap>h1,body.sent .fwrap>p{display:none}body.sent .thanks{display:block}.send .err{color:#F2B48C}
.fwrap{max-width:760px;margin:0 auto;padding:150px 24px 120px;position:relative}
.fwrap:before{content:'';position:fixed;left:50%;top:-200px;width:1100px;height:700px;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(127,216,240,.13),rgba(169,150,255,.08) 40%,transparent 70%);pointer-events:none;z-index:-1}
.fwrap h1{font-size:72px;line-height:1;margin-bottom:20px}.fwrap>p{font-size:18px;line-height:1.65;color:#D9DDF0;margin-bottom:60px}
fieldset{border:0;margin:0 0 70px}legend{font-family:'Cormorant Garamond';font-style:italic;font-size:36px;margin-bottom:26px;color:#F7F5F0}
.q{margin-bottom:30px}.q label,.q .l{display:block;font-size:16px;color:#E6E9F7;margin-bottom:10px;line-height:1.5}.q small{display:block;color:#8F97BC;font-size:13px;margin:-4px 0 10px}
.q input[type=text],.q input[type=email],.q input[type=url],.q textarea,.q select{width:100%;background:rgba(246,241,231,.05);border:1px solid rgba(246,241,231,.22);border-radius:8px;padding:15px 16px;color:var(--ink);font:16px 'DM Sans',sans-serif;outline:none;transition:border-color .3s,box-shadow .3s}
.q textarea{min-height:120px;resize:vertical;line-height:1.55}
.q input:focus,.q textarea:focus,.q select:focus{border-color:#9EDCF2;box-shadow:0 0 0 3px rgba(127,216,240,.15)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.opts{display:flex;flex-wrap:wrap;gap:10px}.opts label{margin:0;cursor:pointer}.opts input{position:absolute;opacity:0}.opts span{display:inline-block;padding:11px 18px;border-radius:999px;border:1px solid rgba(246,241,231,.25);font-size:14px;color:#D9DDF0;transition:all .25s}
.opts input:checked+span{border-color:#9EDCF2;color:#06081A;background:linear-gradient(90deg,#8FB3F6,#A498FE);box-shadow:0 0 20px rgba(127,216,240,.45)}
.send{text-align:center;margin-top:20px}.send button{border:0;cursor:pointer;font-family:'DM Sans'}
.send p{color:#8F97BC;font-size:13px;margin-top:18px}
@media (max-width:600px){.fwrap{padding:110px 18px 80px}.fwrap h1{font-size:46px}.two{grid-template-columns:1fr}legend{font-size:30px}}
'''
def opts(name,items,multi=False):
  t='checkbox' if multi else 'radio'
  return '<div class="opts">'+''.join(f'<label><input type="{t}" name="{name}" value="{i}"><span>{i}</span></label>' for i in items)+'</div>'
def q(label,field,hint=''):
  return f'<div class="q"><span class="l">{label}</span>{"<small>"+hint+"</small>" if hint else ""}{field}</div>'
def inp(n,t='text',ph=''): return f'<input type="{t}" name="{n}" placeholder="{ph}" required>'
def ta(n,ph=''): return f'<textarea name="{n}" placeholder="{ph}"></textarea>'
APPLY_ENDPOINTS=[u for u in os.environ.get('APPLY_ENDPOINTS','').split(',') if u]
F_JS="""<script>(function(){var f=document.querySelector('form.apply'),E=%s;f.addEventListener('submit',async function(e){e.preventDefault();var d={},fd=new FormData(f);fd.forEach(function(v,k){d[k]=d[k]?d[k]+', '+v:v});d._subject='Session application: '+(d.brand||d.name||'');d._template='table';d._captcha='false';var b=f.querySelector('button');b.disabled=true;b.textContent='Sending…';try{if(E.length){var rs=await Promise.allSettled(E.map(function(u){return fetch(u,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0})}));if(!rs.some(function(x){return x.status==='fulfilled'}))throw 0}document.body.classList.add('sent');scrollTo(0,0)}catch(x){b.disabled=false;b.textContent='Send my application';var m=f.querySelector('.err')||f.querySelector('.send').appendChild(document.createElement('p'));m.className='err';m.textContent='That didn’t send. Try once more in a moment.'}})})();</script>"""%(__import__('json').dumps(APPLY_ENDPOINTS))
def F():
  s=f'<a class="mk" href="{BASE}/session/">A·M·W</a><div class="fwrap"><h1 class="ser">Apply for <em>a Session.</em></h1><p>About ten minutes. The more you tell me, the more we get done in the 45. I read every application myself, and you hear back within three days.</p><form class="apply">'
  s+='<fieldset><legend>You</legend><div class="two">'+q('Your name',inp('name'))+q('Email',inp('email','email'))+'</div>'+q('Your role',opts('role',['Founder','Co-founder','Creative director','Other']))+q('Where are you based?',inp('city','text','City, country'))+'</fieldset>'
  s+='<fieldset><legend>Your brand</legend>'+'<div class="two">'+q('Brand name',inp('brand'))+q('Website or Instagram',inp('link','url','https://'))+'</div>'+q('What do you make, in one line?',inp('oneline'))+q('How long has it been running?',opts('age',['Not launched yet','Under 1 year','1 to 3 years','3+ years']))+q('What monthly budget have you set aside for your brand?',opts('budget',['Under $1,500','$1,500 to $2,500','$2,500 to $4,000','$4,000+']),'It stays between us.')+q('Who works on it?',opts('team',['Just me','2 to 5','6 to 15','16+']))+'</fieldset>'
  s+='<fieldset><legend>Where it’s stuck</legend>'+q('What’s the one thing holding your brand back right now?',ta('stuck','Be specific. This is where we start.'))+q('What have you already tried?',ta('tried'))+q('Which pillars feel weakest?',opts('pillars',PILLARS,True),'Pick up to two.')+'</fieldset>'
  s+='<fieldset><legend>What’s next</legend>'+q('What would make the next three months a win?',ta('win'))+q('Is a drop or launch coming up?',opts('drop',['Yes, in the next 3 months','Yes, later this year','Not planned yet']))+q('When the Session shows the path, how soon do you want to build it?',opts('ready',['Straight away','In the next few months','Just exploring for now']))+q('How did you find me?',opts('src',['Instagram','LinkedIn','X','The letters','A friend','Other']))+q('Anything else I should know?',ta('else'))+'</fieldset>'
  s+='<div class="send"><button class="aurb" type="submit">Send my application</button></div></form><div class="thanks" role="status" aria-live="polite"><h1 class="ser">It’s in. <em>Thank you.</em></h1><p>I read every application myself. You’ll hear back within three days, and if it’s a yes, your email holds the link to book your 45 minutes.</p><a class="aurb" href="'+BASE+'/">Back to the world</a></div></div>'
  s+=F_JS+'</body></html>' 
  return HEAD('Apply for a Session · Ashah Meets World',F_CSS)+s
# ---------- v1.1 LIVE: C on desktop, A on phone, same words ----------
D_CSS=A_CSS+C_CSS+'.mob{display:none}@media (max-width:600px){.dsk{display:none}.mob{display:block}}'
SEAM_CSS='@media (min-width:601px){.hero{height:100vh;height:100svh;min-height:680px}.hero .fade{background:linear-gradient(180deg,rgba(7,10,28,.3) 0,rgba(7,10,28,0) 20%,rgba(7,10,28,0) 66%,rgba(34,40,104,.55) 86%,rgb(34,40,104) 100%)}.dsk>.scene:first-child:before{background:linear-gradient(180deg,rgb(34,40,104) 0,rgba(34,40,104,.5) 10%,rgba(34,40,104,0) 28%,rgba(7,10,28,.55) 40%,rgba(7,10,28,.55) 78%,var(--bg) 100%)}}' # Ashah 20 Nov: hero fills the screen on desktop; ocean runs straight into the next sky, no dark band
LEAVE_CSS='.scene.leave{min-height:980px;align-items:flex-start;padding-top:120px}.scene.leave .in{max-width:780px}.scene.leave:before{background:linear-gradient(180deg,var(--bg) 0,rgba(7,10,28,.75) 14%,rgba(7,10,28,.55) 32%,rgba(7,10,28,0) 52%,rgba(7,10,28,0) 80%,var(--bg) 100%)}'
END_CSS='.end .amb{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:1}.end .amb .ff{position:absolute;border-radius:50%;animation:ffly var(--d) ease-in-out infinite alternate,ffb var(--b) ease-in-out infinite;animation-delay:var(--dl)}@keyframes ffly{to{transform:translate(var(--x),var(--y))}}@keyframes ffb{0%,100%{opacity:.15}50%{opacity:1}}.end h2,.end p,.end .aurb{z-index:2}'
END_JS='(function(){var sec=document.querySelector(\'.end\');if(!sec)return;var a=document.createElement(\'div\');a.className=\'amb\';sec.prepend(a);var R=Math.random,ph=innerWidth<600,h=\'\',cols=[\'#F2B48C\',\'#FFD9B0\',\'#7FD8F0\',\'#C9DCF7\'];for(var i=0;i<(ph?16:30);i++){var s=(3+R()*4).toFixed(1),c=cols[i%cols.length];h+=\'<i class="ff" style="left:\'+(R()*100)+\'%;top:\'+(15+R()*80)+\'%;width:\'+s+\'px;height:\'+s+\'px;background:\'+c+\';box-shadow:0 0 8px 2px \'+c+\'88,0 0 22px 6px \'+c+\'33;--d:\'+(10+R()*12)+\'s;--b:\'+(3+R()*4)+\'s;--dl:-\'+(R()*10)+\'s;--x:\'+(R()*80-40)+\'px;--y:\'+(-30-R()*70)+\'px"></i>\'}a.innerHTML=h})();'
LEAVE_JS='(function(){var sec=document.querySelector(\'.scene.leave\');if(!sec)return;var s=sec.querySelector(\'.sb svg\');if(!s)return;var v=sec.dataset.v||\'a\';var h=s.innerHTML;var night=\'<linearGradient id="skN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070A22"/><stop offset=".4" stop-color="#121A55"/><stop offset=".7" stop-color="#1E2466"/><stop offset=".88" stop-color="#2E2C7A"/><stop offset="1" stop-color="#46489C"/></linearGradient><radialGradient id="hzN" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#8FB4F6" stop-opacity=".4"/><stop offset=".5" stop-color="#A996FF" stop-opacity=".15"/><stop offset="1" stop-color="#A996FF" stop-opacity="0"/></radialGradient>\';if(v!==\'b\'){h=night+h.replace(/url\\(#sk\\)/g,\'url(#skN)\').replace(/url\\(#hz\\)/g,\'url(#hzN)\')}s.innerHTML=h;var br=s.querySelector(\'circle.br\');if(v===\'a\'&&br)br.setAttribute(\'opacity\',\'.35\');if(v===\'b\'&&br)br.setAttribute(\'opacity\',\'.3\');if(v===\'c\'){if(br)br.setAttribute(\'opacity\',\'.5\');s.setAttribute(\'preserveAspectRatio\',\'xMidYMax slice\')}})();'
def D():
  a=A(); c=C()
  mid=lambda h:h.split(HERO,1)[1].split(END,1)[0]
  m=mid(c); i=m.index('<h2 class="ser">What you leave with.</h2>'); j=m.rindex('<section class="scene"><div class="glow"></div>',0,i)
  # v1.4 (Ashah 19 Nov 11:13pm, picked A of three new scenes): the next morning, first light on the sea, words in the clear sky
  m=m[:j]+'<section class="scene leave" data-v="n"><div class="sb" data-scene="dawn"></div>'+m[j+len('<section class="scene"><div class="glow"></div>'):]
  return HEAD('The Session · Ashah Meets World',D_CSS+LEAVE_CSS+END_CSS+SEAM_CSS)+HERO+'<div class="dsk">'+m+'</div><div class="mob">'+mid(a)+'</div>'+END+TAIL.replace('</body>','<script>'+LEAVE_JS+END_JS+'</script></body>')
os.makedirs(OUT,exist_ok=True)
open(f'{OUT}/session.html','w').write(D())
# apply.html is written by apply_v2.py since 23 Nov 2026 (the v2 form went live); F() above is the old v1.1 form, kept for reference
