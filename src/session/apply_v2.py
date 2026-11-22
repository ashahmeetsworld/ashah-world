#!/usr/bin/env python3
"""Apply for a Session v2.0 (23 Nov 2026): Ashah asked for the Apply form reworked top to bottom, borrowing from prep look C,
to fit the free Brand Strategy Session offer, the flywheel (referrals count, so a friend gets credit) and the prep form that
follows a booking (Apply asks about fit; the prep form asks for the numbers, so nothing is asked twice).
A hidden preview at /session/apply-v2/ until he says swap. APPLY_V2_ENDPOINTS (comma-separated) sets where answers go;
empty = preview mode, nothing is sent. The live form is still /session/apply/ (build.py).
python3 src/session/apply_v2.py src/session"""
import os, sys, json
OUT = sys.argv[1] if len(sys.argv) > 1 else 'src/session'
EP = [u for u in os.environ.get('APPLY_V2_ENDPOINTS', '').split(',') if u.strip()]
apply = open(os.path.join(OUT, 'apply.html')).read()
HEAD = apply.split('</style>')[0].replace('<title>Apply for a Session · Ashah Meets World</title>',
                                         '<title>Apply for a Session · Ashah Meets World</title><meta name="robots" content="noindex">')
PILLARS = ['Identity', 'Storytelling', 'Product', 'Campaigns', 'Ecosystem', 'Continuity']  # the Session scorecard's order

CSS = '''
.aw{max-width:900px;margin:0 auto;padding:150px 24px 120px;position:relative}
.aw:before{content:'';position:fixed;left:50%;top:-200px;width:1100px;height:700px;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(127,216,240,.13),rgba(169,150,255,.08) 40%,transparent 70%);pointer-events:none;z-index:-1}
.hero2{text-align:center;margin-bottom:90px}.hero2 h1{font-size:68px;line-height:1.02;margin-bottom:32px}
.hero2 textarea{width:100%;min-height:140px;background:rgba(246,241,231,.05);border:1px solid #9EDCF2;box-shadow:0 0 0 4px rgba(127,216,240,.12),0 0 60px rgba(127,216,240,.15);border-radius:14px;padding:20px 22px;color:var(--ink);font:italic 24px/1.4 'Cormorant Garamond',serif;outline:none;resize:vertical}
.hero2 p{color:#AEB6D6;font-size:16px;line-height:1.6;margin:18px auto 0;max-width:560px}
.blk{margin-bottom:84px}.blk>h2{font-size:40px;text-align:center;margin-bottom:6px}.blk>p{text-align:center;color:#8F97BC;margin-bottom:30px;font-size:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.card{background:rgba(246,241,231,.035);border:1px solid rgba(246,241,231,.1);border-radius:14px;padding:20px 20px 22px}
.card .l{display:block;font-size:15px;color:#E6E9F7;margin-bottom:12px;line-height:1.45}.card small{display:block;color:#8F97BC;font-size:12px;margin:-6px 0 10px}.card .opts{gap:8px}.card .opts span{padding:9px 14px;font-size:13px}
.card.wide{grid-column:1/-1}
.sentby{margin-top:12px}.sentby[hidden]{display:none}
.card input[type=text],.card input[type=email],.card textarea{width:100%;background:rgba(246,241,231,.05);border:1px solid rgba(246,241,231,.22);border-radius:10px;padding:13px 14px;color:var(--ink);font:15px 'DM Sans',sans-serif;outline:none;transition:border-color .3s,box-shadow .3s}
.card textarea{min-height:96px;resize:vertical;line-height:1.55}
.card input:focus,.card textarea:focus{border-color:#9EDCF2;box-shadow:0 0 0 3px rgba(127,216,240,.15)}
.words{display:flex;flex-direction:column;gap:14px}
.deal{max-width:560px;margin:0 auto;text-align:center;padding:30px 28px;border-radius:16px;border:1px solid rgba(158,220,242,.35);background:linear-gradient(180deg,rgba(127,216,240,.07),rgba(169,150,255,.04));box-shadow:0 0 60px rgba(127,216,240,.08)}
.deal h3{font-family:'Cormorant Garamond';font-style:italic;font-size:30px;line-height:1.2;margin-bottom:18px}
.deal .opts{justify-content:center}.deal .opts span{padding:11px 26px;font-size:15px}
.send{text-align:center;margin-top:44px}.send button{border:0;cursor:pointer;font-family:'DM Sans'}.send button:disabled{opacity:.6}
.send .fine{color:#8F97BC;font-size:13px;margin:18px auto 0;max-width:460px;line-height:1.6}
.err{color:#F2B48C;text-align:center;margin-top:14px}.pv{color:#8F97BC;font-size:12px;text-align:center;margin-top:22px;letter-spacing:.04em}
.thanks{display:none;text-align:center;padding:200px 24px 0}.thanks h1{font-size:64px;line-height:1.02;margin-bottom:22px}.thanks p{font-size:18px;line-height:1.65;color:#D9DDF0;margin:0 auto 40px;max-width:560px}
body.sent form{display:none}body.sent .thanks{display:block}
@media (max-width:700px){.hero2 h1 br{display:none}.grid{grid-template-columns:1fr}.hero2 h1{font-size:44px}.aw{padding:110px 18px 80px}.blk>h2{font-size:34px}.hero2{margin-bottom:70px}.blk{margin-bottom:70px}}
'''

def chips(k, opts, multi=False, req=False):
    t = 'checkbox' if multi else 'radio'
    return '<div class="opts">' + ''.join(f'<label><input type="{t}" name="{k}" value="{o}"{" required" if req else ""}><span>{o}</span></label>' for o in opts) + '</div>'
def card(label, field, hint='', cls='card'):
    return f'<div class="{cls}"><span class="l">{label}</span>' + (f'<small>{hint}</small>' if hint else '') + field + '</div>'
def inp(n, t='text', ph='', req=True):
    return f'<input type="{t}" name="{n}" placeholder="{ph}"{" required" if req else ""}>'
def ta(n, ph=''):
    return f'<textarea name="{n}" placeholder="{ph}"></textarea>'

TAPS = [
    ('Your role', chips('role', ['Founder', 'Co-founder', 'Creative director', 'Other']), ''),
    ('What kind of brand is it?', chips('kind', ['A fashion label with its own designs', 'Music, art or lifestyle', 'Something else']), ''),
    ('How long has it been running?', chips('age', ['Not launched yet', 'Under 1 year', '1 to 3 years', '3+ years']), ''),
    ('What goes into the brand each month?', chips('budget', ['Under $500', '$500 to $1,500', '$1,500 to $4,000', '$4,000+']), 'Shoots, samples, design. It stays between us.'),
    ('Which pillars feel weakest?', chips('pillars', PILLARS, True), 'Pick up to two.'),
    ('Is a drop or launch coming up?', chips('drop', ['In the next 3 months', 'Later this year', 'Not planned yet']), ''),
    ('Once the Session shows the way, would you rather', chips('walk', ['Walk it on my own', 'Walk it with help', 'Not sure yet']), ''),
    ('How did you find me?', chips('src', ['An email from me', 'Instagram', 'LinkedIn', 'YouTube', 'A workbook', 'A friend sent me', 'Other'])
     + '<div class="sentby" hidden><input type="text" name="sentby" placeholder="Who sent you? Their brand is plenty."></div>', ''),
]

s = '<a class="mk" href="__BASE__/session/">A·M·W</a><form class="apply" novalidate><div class="aw">'
s += ('<div class="hero2"><h1 class="ser">What’s holding your brand <br><em>back right now?</em></h1>'
      '<textarea name="stuck" placeholder="Be specific. This is where we start." required></textarea>'
      '<p>A free 45-minute Brand Strategy Session, five a month. About eight minutes to apply. I read every one myself and reply within three days.</p></div>')
s += f'<div class="blk"><h2 class="ser">{["Six","Seven","Eight","Nine"][len(TAPS)-6]} quick taps</h2><p>Ranges are fine.</p><div class="grid">'
s += ''.join(card(l, f, h) for l, f, h in TAPS) + '</div></div>'
s += ('<div class="blk"><h2 class="ser">In your words</h2><p>A line or two each.</p><div class="words">'
      + card('What have you already tried?', ta('tried'))
      + card('What would make the next three months a win?', ta('win'))
      + card('Anything else I should know?', ta('else'), 'Optional.') + '</div></div>')
s += ('<div class="blk"><h2 class="ser">Last, you and your brand</h2><p>So I know who I’m meeting.</p><div class="grid">'
      + card('Your name', inp('name')) + card('Email', inp('email', 'email'))
      + card('Brand name', inp('brand')) + card('Website or Instagram', inp('link', 'text', 'A link or @handle'))
      + card('What do you make, in one line?', inp('oneline', req=False)) + card('Where are you based?', inp('city', 'text', 'City, country', req=False))
      + '</div></div>')
s += ('<div class="deal"><h3>The Session is free.<br>All I ask back is honest feedback.</h3>' + chips('deal', ['Deal.'], True) + '</div>'
      '<div class="send"><button class="aurb go" type="submit">Send my application</button>'
      '<p class="fine">I record every Session so your pack is made properly. I’ll check that’s OK when we start.</p></div>'
      + ('' if EP else '<p class="pv">Preview. Nothing is sent from this page.</p>') + '</div></form>')
s += ('<div class="thanks" role="status" aria-live="polite"><h1 class="ser">It’s in.<br><em>Thank you.</em></h1>'
      '<p>I read every application myself, and you’ll hear back within three days. If it’s a yes, the email holds your link to pick a time. '
      'Once you’ve booked, a 5-minute prep form follows, so we go straight to depth.</p><a class="aurb" href="__BASE__/">Back to the world</a></div>')

JS = '''<script>(function(){var f=document.querySelector('form.apply'),E=__EP__;
f.querySelectorAll('input[name=pillars]').forEach(function(c){c.addEventListener('change',function(){if(f.querySelectorAll('input[name=pillars]:checked').length>2)c.checked=false})});
var sb=f.querySelector('.sentby');f.querySelectorAll('input[name=src]').forEach(function(r){r.addEventListener('change',function(){sb.hidden=r.value!=='A friend sent me'||!r.checked;if(!sb.hidden)sb.querySelector('input').focus()})});
function say(t){var m=f.querySelector('.err')||f.querySelector('.send').appendChild(document.createElement('p'));m.className='err';m.textContent=t}
f.addEventListener('submit',async function(e){e.preventDefault();
var bad=[].slice.call(f.querySelectorAll('[required]')).filter(function(i){return i.type!=='checkbox'&&!i.value.trim()})[0];
if(bad){bad.focus();bad.scrollIntoView({block:'center',behavior:'smooth'});say('One more: '+(bad.closest('.card,.hero2').querySelector('.l,h1').innerText.replace(/\\s+/g,' ').trim()));return}
if(!f.querySelector('input[name=deal]').checked){f.querySelector('.deal').scrollIntoView({block:'center',behavior:'smooth'});say('Tick “Deal.” and it’s on its way.');return}
var d={},fd=new FormData(f);fd.forEach(function(v,k){if(v)d[k]=d[k]?d[k]+', '+v:v});d._subject='Session application: '+(d.brand||d.name||'');d._template='table';d._captcha='false';
var b=f.querySelector('.go');b.disabled=true;b.textContent='Sending…';
try{if(E.length){var rs=await Promise.allSettled(E.map(function(u){return fetch(u,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(d)}).then(function(r){if(!r.ok)throw 0})}));if(!rs.some(function(x){return x.status==='fulfilled'}))throw 0}
document.body.classList.add('sent');scrollTo(0,0)}catch(x){b.disabled=false;b.textContent='Send my application';say('That didn’t send. Try once more in a moment.')}})})();</script>'''.replace('__EP__', json.dumps(EP))

open(os.path.join(OUT, 'apply-v2.html'), 'w').write(HEAD + CSS + '</style></head><body>' + s + JS + '</body></html>')
print('apply-v2.html', 'sends' if EP else 'preview')
