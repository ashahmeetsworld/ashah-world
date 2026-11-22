#!/usr/bin/env python3
"""Session prep form (23 Nov 2026). Ashah picked B (one question a screen): it is the real form at /session/prep/,
sending to the same place as the Apply form. Cal.com sends people here after they book and adds ?startTime=&attendeeName=&email=
to the link, so the form knows the day ("See you Thursday") and skips the email step.
The two looks he tried stay as hidden previews that send nothing: /session/prep-b/ and /session/prep-c/.
python3 src/session/prep.py src/session"""
import os, sys, json, re
OUT = sys.argv[1] if len(sys.argv) > 1 else 'src/session'
apply = open(os.path.join(OUT, 'apply.html')).read()
# the Apply form's inbox endpoint only, so answers land in the same inbox. Its Control Room /apply route is for applications, not prep answers.
EP_REAL = [u for u in json.loads(re.search(r',E=(\[.*?\]);', apply).group(1)) if 'formsubmit.co' in u]
HEAD = open(os.path.join(OUT, 'apply-head.html')).read()  # same head, fonts and form styles as the Apply form (v1.1 snapshot)
HEAD = HEAD.replace('<title>Apply for a Session · Ashah Meets World</title>', '<title>Before we meet · Ashah Meets World</title><meta name="robots" content="noindex">')

OBJ = 'What’s the one thing you want from our 45 minutes?'
Q = [('price', 'What does your main piece sell for?', ['Under $100', '$100 to $250', '$250 to $500', '$500+'], 1),
     ('drops', 'How many drops a year?', ['None yet', '1 to 2', '3 to 4', '5+'], 1),
     ('last', 'How did your last drop go?', ['Sold out', 'Sold most', 'Sold some', 'Slow', 'No drop yet'], 1),
     ('found', 'Where do most buyers first find you?', ['Instagram', 'TikTok', 'Word of mouth', 'Stockists', 'Events', 'Other'], 2),
     ('list', 'How big is your email list?', ['Under 500', '500 to 2,000', '2,000 to 10,000', '10,000+'], 1),
     ('ig', 'And your Instagram?', ['Under 2,000', '2,000 to 10,000', '10,000 to 50,000', '50,000+'], 1)]

def chips(k, opts, mx):
    t = 'checkbox' if mx > 1 else 'radio'
    return '<div class="opts">' + ''.join(f'<label><input type="{t}" name="{k}" value="{o}"><span>{o}</span></label>' for o in opts) + '</div>'

# shared send script: reads the Cal.com link (?attendeeName=&email=&startTime=), so they never type their email twice
# and the form can say which day they booked
SEND = '''<script>(function(){var E=__EP__,f=document.querySelector('form.prep'),P=new URLSearchParams(location.search);
var V={name:P.get('attendeeName')||P.get('name'),email:P.get('email'),brand:P.get('brand')};
['name','email','brand'].forEach(function(k){var v=V[k],i=f.querySelector('[name="'+k+'"]');if(v&&i){i.value=v;var w=i.closest('.who');if(w&&k==='email')w.classList.add('known')}});
var st=P.get('startTime'),t=st?new Date(st):null;if(t&&!isNaN(t)){var day=t.toLocaleDateString('en-AU',{weekday:'long'}),dm=t.toLocaleDateString('en-AU',{day:'numeric',month:'long'}),h=t.getHours(),m=t.getMinutes(),tm=(h%12||12)+(m?':'+('0'+m).slice(-2):'')+(h<12?'am':'pm'),lab=day+' '+dm+', '+tm;
f.querySelector('[name="booked"]').value=lab;document.querySelectorAll('.when').forEach(function(w){w.querySelector('b').textContent=lab;w.hidden=false});document.querySelectorAll('.seeday').forEach(function(w){w.textContent='See you '+day+'.'})}
f.querySelectorAll('input[type=checkbox]').forEach(function(c){c.addEventListener('change',function(){var g=f.querySelectorAll('input[name="'+c.name+'"]:checked');if(g.length>2)c.checked=false})});
window.prepSend=async function(){var d={},fd=new FormData(f);fd.forEach(function(v,k){if(v)d[k]=d[k]?d[k]+', '+v:v});d._subject='Session prep: '+(d.brand||d.name||d.email||'');d._template='table';d._captcha='false';
var b=f.querySelector('.go');if(b){b.disabled=true;b.textContent='Sending…'}
try{if(E.length){var rs=await Promise.allSettled(E.map(function(u){return fetch(u,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0})}));if(!rs.some(function(x){return x.status==='fulfilled'}))throw 0}
document.body.classList.add('sent');scrollTo(0,0)}catch(x){if(b){b.disabled=false;b.textContent='Send'}var m=f.querySelector('.err')||f.appendChild(document.createElement('p'));m.className='err';m.textContent='That didn’t send. Try once more in a moment.'}};
f.addEventListener('submit',function(e){e.preventDefault();prepSend()})})();</script>'''
HID = '<input type="hidden" name="name"><input type="hidden" name="brand"><input type="hidden" name="booked">'
WHEN = '<p class="when" hidden>You’re booked for <b></b>.</p>'
THANKS = '''<div class="thanks" role="status" aria-live="polite"><h1 class="ser">That’s everything.<br><em class="seeday">See you soon.</em></h1><p>I’ll read this before we meet, so we start where it matters.</p><a class="aurb" href="__BASE__/">Back to the world</a></div>'''
BASECSS = '''
.thanks{display:none;text-align:center;padding:200px 24px 0}.thanks h1{font-size:64px;line-height:1.02;margin-bottom:22px}.thanks p{font-size:18px;line-height:1.65;color:#D9DDF0;margin:0 auto 40px;max-width:520px}
body.sent form,body.sent .stage{display:none}body.sent .thanks{display:block}
.err{color:#F2B48C;text-align:center;margin-top:16px}.pv{color:#8F97BC;font-size:12px;text-align:center;margin-top:26px;letter-spacing:.04em}
.go{border:0;cursor:pointer;font-family:'DM Sans'}.go:disabled{opacity:.6}
.who.known{display:none}
.when{color:#AEB6D6;font-size:15px;margin-bottom:18px}.when b{color:#F6F1E7;font-weight:500}
'''

# ---------------- B: one question a screen ----------------
B_CSS = BASECSS + '''
.stage{min-height:100vh;display:flex;align-items:flex-start;justify-content:center;padding:max(120px,16vh) 20px 160px;position:relative}
.stage:before{content:'';position:fixed;left:50%;top:-220px;width:1000px;height:720px;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(127,216,240,.14),rgba(169,150,255,.08) 40%,transparent 70%);pointer-events:none;z-index:-1}
.dots{position:fixed;top:64px;left:0;right:0;display:flex;justify-content:center;gap:9px;z-index:5}.dots i{width:7px;height:7px;border-radius:50%;background:rgba(246,241,231,.2);transition:all .4s}.dots i.on{background:#9EDCF2;box-shadow:0 0 10px #7FD8F0}
.step{display:none;width:100%;max-width:520px}.step.on{display:block;animation:in .45s ease}
@keyframes in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.step h2{font-size:52px;line-height:1.05;margin-bottom:30px}
.step .opts{flex-direction:column}.step .opts label{display:block}.step .opts span{display:block;text-align:center;padding:16px;font-size:16px}
.step textarea,.step input[type=email]{width:100%;background:rgba(246,241,231,.05);border:1px solid rgba(246,241,231,.22);border-radius:12px;padding:18px;color:var(--ink);font:18px 'DM Sans',sans-serif;outline:none}
.step textarea{min-height:140px;resize:none;line-height:1.5}.step textarea:focus,.step input:focus{border-color:#9EDCF2;box-shadow:0 0 0 3px rgba(127,216,240,.15)}
.step small{display:block;color:#8F97BC;font-size:13px;margin:-16px 0 18px}
.bar{position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:center;padding:40px max(20px,calc(50% - 260px)) 30px;color:#8F97BC;font-size:14px;z-index:5;background:linear-gradient(180deg,rgba(7,10,28,0),#070A1C 45%)}
.bar button.back{background:none;border:0;color:#8F97BC;font:14px 'DM Sans';cursor:pointer;padding:10px 0}.bar .back[hidden]{visibility:hidden;display:block}
.bar .aurb{padding:14px 30px;font-size:12px}
body.sent .dots,body.sent .bar{display:none}
@media (max-width:600px){.step h2{font-size:40px;margin-bottom:24px}.dots{top:58px}.stage{padding-top:110px}.step .opts span{padding:14px}}
'''
steps = [('obj', f'{WHEN}<h2 class="ser">What’s the one thing you want from our <em>45 minutes?</em></h2><textarea name="objective" placeholder="One line is plenty."></textarea>', 'next')]
for k, l, o, mx in Q:
    words = l.rsplit(' ', 2)
    h = f'{words[0]} <em>{" ".join(words[1:])}</em>'
    steps.append((k, f'<h2 class="ser">{h}</h2>' + ('<small>Pick up to two.</small>' if mx > 1 else '') + chips(k, o, mx), 'next' if mx > 1 else 'tap'))
steps.append(('who', '<h2 class="ser">Last one. <em>Your email?</em></h2><input type="email" name="email" placeholder="So I can match this to your booking">', 'send'))
N = len(steps)
b = f'<a class="mk" href="__BASE__/">A·M·W</a><div class="dots">' + ''.join('<i></i>' for _ in range(N)) + '</div>'
b += '<form class="prep" novalidate>' + HID + '<div class="stage">'
for i, (k, inner, mode) in enumerate(steps):
    b += f'<div class="step{" who" if k=="who" else ""}" data-mode="{mode}">{inner}</div>'
b += '</div><div class="bar"><button type="button" class="back">Back</button><span class="count"></span><button type="button" class="aurb go">Next</button></div>' + '__NOTE__</form>' + THANKS
B_JS = '''<script>(function(){var f=document.querySelector('form.prep'),S=[].slice.call(f.querySelectorAll('.step')),D=[].slice.call(document.querySelectorAll('.dots i')),bk=f.querySelector('.back'),go=f.querySelector('.go'),ct=f.querySelector('.count'),i=0;
function live(){return S.filter(function(s){return !s.classList.contains('known')})}
function show(){var L=live();L.forEach(function(s,j){s.classList.toggle('on',j===i)});D.forEach(function(d,j){d.style.display=j<L.length?'':'none';d.classList.toggle('on',j<=i)});
var last=i===L.length-1,m=last?'next':L[i].dataset.mode;bk.hidden=i===0;ct.textContent=(i+1)+' of '+L.length+(m==='tap'?' · tap to go on':'');go.style.visibility=m==='tap'?'hidden':'visible';go.textContent=i===L.length-1?'Send':'Next';var t=L[i].querySelector('textarea,input[type=email]');if(t&&innerWidth>600)setTimeout(function(){t.focus()},300)}
function next(){var L=live();if(i<L.length-1){i++;show()}else prepSend()}
go.addEventListener('click',next);bk.addEventListener('click',function(){if(i>0){i--;show()}});
S.forEach(function(s){if(s.dataset.mode==='tap')s.querySelectorAll('input').forEach(function(x){x.addEventListener('change',function(){var L=live();if(L.indexOf(s)<L.length-1)setTimeout(next,260)})})});
f.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.tagName!=='TEXTAREA'){e.preventDefault();next()}});
setTimeout(show,0)})();</script>'''
def page(css, body, ep, js=''):
    note = '' if ep else '<p class="pv">Preview. Answers aren’t sent anywhere yet.</p>'
    return HEAD + css + '</style></head><body>' + body.replace('__NOTE__', note) + SEND.replace('__EP__', json.dumps(ep)) + js + '</body></html>'
open(os.path.join(OUT, 'prep.html'), 'w').write(page(B_CSS, b, EP_REAL, B_JS))   # the real one (Ashah's pick, 23 Nov 2026)
open(os.path.join(OUT, 'prep-b.html'), 'w').write(page(B_CSS, b, [], B_JS))      # preview, sends nothing

# ---------------- C: aim first, then six taps ----------------
C_CSS = BASECSS + '''
.cw{max-width:900px;margin:0 auto;padding:150px 24px 120px;position:relative}
.cw:before{content:'';position:fixed;left:50%;top:-200px;width:1100px;height:700px;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(127,216,240,.13),rgba(169,150,255,.08) 40%,transparent 70%);pointer-events:none;z-index:-1}
.hero2{text-align:center;margin-bottom:80px}.hero2 h1{font-size:68px;line-height:1.02;margin-bottom:32px}
.hero2 textarea{width:100%;min-height:130px;background:rgba(246,241,231,.05);border:1px solid #9EDCF2;box-shadow:0 0 0 4px rgba(127,216,240,.12),0 0 60px rgba(127,216,240,.15);border-radius:14px;padding:20px 22px;color:var(--ink);font:italic 24px/1.4 'Cormorant Garamond',serif;outline:none;resize:vertical}
.hero2 p{color:#8F97BC;font-size:14px;margin-top:14px}
.taps h2{font-size:36px;text-align:center;margin-bottom:6px}.taps>p{text-align:center;color:#8F97BC;margin-bottom:30px;font-size:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{background:rgba(246,241,231,.035);border:1px solid rgba(246,241,231,.1);border-radius:14px;padding:20px 20px 22px}
.card .l{display:block;font-size:15px;color:#E6E9F7;margin-bottom:12px}.card small{display:block;color:#8F97BC;font-size:12px;margin:-6px 0 10px}.card .opts span{padding:9px 14px;font-size:13px}
.who2{max-width:440px;margin:40px auto 0}.who2 .l{display:block;text-align:center;font-size:15px;color:#E6E9F7;margin-bottom:10px}
.who2 input{width:100%;background:rgba(246,241,231,.05);border:1px solid rgba(246,241,231,.22);border-radius:10px;padding:15px 16px;color:var(--ink);font:16px 'DM Sans',sans-serif;outline:none;text-align:center}
.who2 input:focus{border-color:#9EDCF2}
.sendc{text-align:center;margin-top:44px}
@media (max-width:700px){.grid{grid-template-columns:1fr}.hero2 h1{font-size:44px}.cw{padding:110px 18px 80px}}
'''
c = '<a class="mk" href="__BASE__/">A·M·W</a><form class="prep" novalidate>' + HID + '<div class="cw stage">'
c += f'<div class="hero2">{WHEN}<h1 class="ser">What do you want<br><em>from our 45 minutes?</em></h1><textarea name="objective" placeholder="One line is plenty."></textarea><p>This is where we start.</p></div>'
c += '<div class="taps"><h2 class="ser">Six quick taps</h2><p>Ranges are fine.</p><div class="grid">'
for k, l, o, mx in Q:
    c += f'<div class="card"><span class="l">{l}</span>' + ('<small>Pick up to two.</small>' if mx > 1 else '') + chips(k, o, mx) + '</div>'
c += '</div></div><div class="who who2"><span class="l">Your email, so I can match this to your booking</span><input type="email" name="email"></div>'
c += '<div class="sendc"><button type="submit" class="aurb go">Send, see you soon</button></div>' + '__NOTE__</div></form>' + THANKS
open(os.path.join(OUT, 'prep-c.html'), 'w').write(page(C_CSS, c, []))           # preview, sends nothing
print('prep.html (sends to', len(EP_REAL), 'endpoint), prep-b.html + prep-c.html (previews)')
