
(()=>{
const P=n=>document.querySelector('.plate[data-l="'+n+'"]');
const all=()=>document.querySelectorAll('.plate');
const title=document.getElementById('stTitle'),foot=document.getElementById('stFoot'),spark=document.getElementById('spark'),msgs=document.getElementById('msgs'),btn=document.getElementById('lessonNext'),beatsEl=document.getElementById('beats');
function set(t,f){title.style.opacity=0;setTimeout(()=>{title.textContent=t;title.style.opacity=1},250);foot.textContent=f}
function stage(on,seen,extra){all().forEach(p=>{p.className='plate';const l=+p.dataset.l;if(on.includes(l))p.classList.add('on');else if(seen.includes(l))p.classList.add('seen')});spark.classList.remove('run');extra&&extra()}
const B=[
 {go(){stage([],[]);set('Four layers, one at a time.','Lesson · the kitchen')},
  say:[['m','Today: how a system like this holds together. Picture a restaurant kitchen. Four layers, and we build it from the floor up.']]},
 {go(){stage([1],[]);set('Layer 1: Skills','Layer 1 of 4 · Skills')},
  say:[['m','First, the recipe cards. Each one says exactly how a dish is made, so any cook can make it the same way twice. Those are <b>Skills</b>: written instructions for one job.'],['u','So a skill is the how.'],['m','Exactly. The how, written down once.']]},
 {go(){stage([2],[1]);set('Layer 2: Memory','Layer 2 of 4 · Memory')},
  say:[['m','Next to the pass sits the order book. Every table, every allergy, every regular. Close the kitchen tonight and tomorrow\'s crew still knows. That is <b>Memory</b>.'],['m','<span class="tag">Recall</span><br>Quick one before we climb: which layer tells a cook <i>how</i> to make the dish?'],['u','The recipe cards. Skills.'],['m','Good. Holding the first layer while we add the second is the whole trick.']]},
 {go(){stage([3],[1,2]);set('Layer 3: Routines','Layer 3 of 4 · Routines')},
  say:[['m','Now the prep clock. At four o\'clock the stock goes on, whether anyone remembers or not. <b>Routines</b> are the work that runs on a schedule, on its own.']]},
 {go(){stage([4],[1,2,3],()=>spark.classList.add('run'));set('Layer 4: Apps','Layer 4 of 4 · Apps')},
  say:[['m','Last, the service window, where plates meet the room. <b>Apps</b> are where the work reaches people. Watch the light: every plate travels up through all four layers before it leaves.']]},
 {go(){stage([],[1,3,4]);P(2).classList.add('gone');setTimeout(()=>{P(3).classList.add('shaky');P(4).classList.add('shaky')},500);set('What if the order book vanished?','Thought experiment')},
  say:[['m','<span class="tag">Thought experiment</span><br>Tear out the order book. Recipes still work, the clock still ticks. What breaks first?'],['u','Nobody knows which table ordered what. The food is right but it goes to the wrong place.'],['m','Yes. Skills without Memory make the right dish for the wrong table. That is why every seat reads memory before it starts.']]},
 {go(){stage([1,2,3,4],[]);set('Check your understanding.','Understanding check')},
  say:[['m','<span class="tag">Check</span><br>A routine runs at 9am and needs to know last week\'s results. Which layer does it lean on?<div class="opts"><button>Skills</button><button data-ok>Memory</button><button>Apps</button></div>']]},
 {go(){stage([1,2,3,4],[],()=>spark.classList.add('run'));set('Lesson logged to your path.','Next time · how layers talk to each other')},
  say:[['m','That is the lesson. I have logged it to your path, with the one idea to carry: <i>the how, the memory, the clock, the window.</i> Next time, how the layers talk to each other.']]}
];
B.forEach(()=>beatsEl.appendChild(document.createElement('i')));
let i=-1,busy=false,auto=null;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function bubble(k,h){const d=document.createElement('div');d.className='b '+k;d.innerHTML=(k==='m'?'<div class="who">Mentor</div>':'')+h;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;
 d.querySelectorAll('.opts button').forEach(b=>b.onclick=()=>{d.querySelectorAll('.opts button').forEach(x=>x.disabled=true);b.classList.add(b.hasAttribute('data-ok')?'right':'wrong');d.querySelector('[data-ok]').classList.add('right');
  setTimeout(()=>bubble('m',b.hasAttribute('data-ok')?'Right. The routine is the clock, but it reads the order book to know what happened.':'Close, but the routine needs what happened last week, and that lives in Memory.'),500)});
 return d}
async function next(){if(busy)return;busy=true;i=(i+1)%B.length;if(i===0)msgs.innerHTML='';
 beatsEl.querySelectorAll('i').forEach((e,n)=>e.classList.toggle('on',n<=i));B[i].go();
 for(const [k,h] of B[i].say){if(k==='m'){const t=bubble('typing','<span></span><span></span><span></span>');await sleep(900);t.remove()}else await sleep(500);bubble(k,h);await sleep(k==='m'?1300:700)}
 btn.textContent=i===B.length-1?'Replay the lesson':'Next';busy=false}
btn.onclick=()=>{clearTimeout(auto);next()};
const io=new IntersectionObserver(es=>{if(es[0].isIntersecting&&i<0){next();io.disconnect()}},{threshold:.4});io.observe(document.getElementById('lesson'));
})();


(()=>{/* board meeting */
const SEATS=['Vitality','Growth','Love','Aliveness','Expression','Contribution','Freedom'];
const tbl=document.getElementById('mtable'),beams=document.getElementById('beams'),q=document.getElementById('mq'),foot=document.getElementById('mfoot'),msgs=document.getElementById('mmsgs'),btn=document.getElementById('mNext'),beatsEl=document.getElementById('mbeats');
const pos=SEATS.map((s,i)=>{const a=Math.PI*(.1+i*.8/6);return [280-250*Math.cos(a),215-175*Math.sin(a)]});
const chairPos=[280,300];
SEATS.forEach((s,i)=>{const e=document.createElement('div');e.className='seat';e.dataset.s=i;e.style.left=pos[i][0]/5.6+'%';e.style.top=pos[i][1]/3.3+'%';e.innerHTML='<i></i><b>'+s+'</b>';tbl.appendChild(e)});
const ch=document.createElement('div');ch.className='seat chair';ch.dataset.s='c';ch.style.left='50%';ch.style.top=chairPos[1]/3.3+'%';ch.innerHTML='<i></i><b>The Chair · the mission</b>';tbl.appendChild(ch);
const seat=i=>tbl.querySelector('[data-s="'+i+'"]');
function light(on,done){tbl.querySelectorAll('.seat').forEach(e=>{e.classList.remove('on');const k=e.dataset.s;if(on.includes(k==='c'?'c':+k))e.classList.add('on');else if(done.includes(k==='c'?'c':+k))e.classList.add('done')})}
function beam(pairs){beams.innerHTML=pairs.map(([a,b])=>{const p=a==='c'?chairPos:pos[a],r=b==='c'?chairPos:pos[b];return '<line class="beam" x1="'+p[0]+'" y1="'+p[1]+'" x2="'+r[0]+'" y2="'+r[1]+'"/>'}).join('')}
const B=[
 {go(){light([],[]);beam([]);q.textContent='"Take a paid side project that pauses the content batch for two weeks?"';foot.textContent='The question is tabled'},
  say:[['u','A call for the board: a paid side project has come up. It pays well, but it would pause the content batch for two weeks.'],['ch','The board will hear it. Each value speaks once, then I rule against the mission.']]},
 {go(){light([1],[]);beam([]);foot.textContent='Growth speaks'},say:[['m','Growth','New client, new kind of work, new reference for the portfolio. That counts for something.']]},
 {go(){light([6],[1]);beam([]);foot.textContent='Freedom speaks'},say:[['m','Freedom','Money buys runway. Runway buys the right to say no later.']]},
 {go(){light([5],[1,6]);beam([]);foot.textContent='Contribution speaks'},say:[['m','Contribution','The audience notices two quiet weeks. Consistency is a promise already made.']]},
 {go(){light([3],[1,5,6]);beam([]);foot.textContent='Aliveness speaks'},say:[['m','Aliveness','Does the project itself excite? If it drains, it costs more than two weeks.']]},
 {go(){light([5,6],[1,3]);beam([[5,6]]);foot.textContent='The tension is named'},say:[['m','The board','<span class="tag">Tension</span><br>Freedom against Contribution: runway now, or the promise of showing up.']]},
 {go(){light(['c'],[1,3,5,6]);beam([['c',5],['c',6]]);foot.textContent='The Chair rules'},say:[['ch','Take it, and keep the promise. Pre-schedule the two weeks from the Drafts already made, so the batch never goes dark.<br><br><span class="tag">Next step</span><br>Content Producer schedules the gap before the project starts.']]},
 {go(){light([],[0,1,2,3,4,5,6,'c']);beam([]);foot.textContent='Logged to Decisions'},say:[['ch','Ruling logged to Decisions. The next step has been handed to Content Producer.']]}
];
B.forEach(()=>beatsEl.appendChild(document.createElement('i')));
let i=-1,busy=false;const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function bubble(k,who,h){const d=document.createElement('div');d.className='b '+k;d.innerHTML=(k==='m'?'<div class="who">'+who+'</div>':k==='ch'?'<div class="who">The Chair</div>':'')+h;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;return d}
async function next(){if(busy)return;busy=true;i=(i+1)%B.length;if(i===0)msgs.innerHTML='';
 beatsEl.querySelectorAll('i').forEach((e,n)=>e.classList.toggle('on',n<=i));B[i].go();
 for(const s of B[i].say){const k=s[0],who=s.length>2?s[1]:'',h=s[s.length-1];if(k!=='u'){const t=bubble('m typing','','<span></span><span></span><span></span>');t.querySelector('.who')?.remove();await sleep(800);t.remove()}else await sleep(400);bubble(k,who,h);await sleep(k==='u'?600:1100)}
 btn.textContent=i===B.length-1?'Replay the meeting':'Next';busy=false}
btn.onclick=next;
const io=new IntersectionObserver(es=>{if(es[0].isIntersecting&&i<0){next();io.disconnect()}},{threshold:.4});io.observe(document.getElementById('mtg'));
})();

document.querySelectorAll(".dt").forEach(b=>b.onclick=()=>{document.querySelectorAll(".dt").forEach(x=>x.classList.toggle("on",x===b));document.querySelectorAll("[data-panel]").forEach(p=>p.hidden=p.dataset.panel!==b.dataset.show);});

(()=>{const hs=[...document.querySelectorAll('.hp[data-h]')];let auto=null,stopped=false;const run=()=>{if(auto||stopped)return;auto=setInterval(()=>{const i=hs.findIndex(h=>h.classList.contains('on'));pick(hs[(i+1)%hs.length])},3800);};new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)run();else{clearInterval(auto);auto=null;if(!stopped)pick(hs[0]);}}),{threshold:.4}).observe(document.querySelector('.crew'));
function pick(b){hs.forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('[data-room]').forEach(im=>im.hidden=im.dataset.room!==b.dataset.h);}
hs.forEach(b=>b.onclick=()=>{stopped=true;clearInterval(auto);pick(b);});

const fl=document.getElementById('float'),hero=document.querySelector('.o-hero'),close=document.getElementById('close');let past=false,at=false,reading=false;const set=()=>fl.classList.toggle('on',past&&!at&&!reading);
// Phones: the button tucks away while you scroll down to read, and comes back when you scroll up.
const phone=matchMedia('(max-width:860px)');let ly=scrollY;addEventListener('scroll',()=>{const y=scrollY,d=y-ly;if(Math.abs(d)<6)return;reading=phone.matches&&d>0;ly=y;set();},{passive:true});
new IntersectionObserver(([e])=>{past=!e.isIntersecting;set()}).observe(hero);new IntersectionObserver(([e])=>{at=e.isIntersecting;set()}).observe(close);
})();


(()=>{const fr=document.getElementById('liveHub'),box=document.getElementById('lf'),shot=box.parentElement;
fr.src=window.ORBIT_HUB;
const fit=()=>{fr.style.transform='scale('+(box.clientWidth/1280)+')'};fit();new ResizeObserver(fit).observe(box);
const CAP=["Your Front Desk. What's waiting on you, and what's coming this week.","Your helpers, on one wheel. Tap one to step into their room.","Each room is a pipeline. Every step, at a glance.","One tap moves work on. It checks with you first.","Only what's urgent or timely. Never noise.","What ran, and what it cost. Right now, $0.","Your Council. Two doors, away from the work.","The Mentor's garden. One lesson at a time.","Recos. It suggests its own upgrades.","That's your world. Yours arrives with your names in it."];
const btn=document.getElementById('guideBtn'),lab=btn.querySelector('span'),cap=document.getElementById('gcap'),dots=document.getElementById('gdots');
dots.innerHTML=CAP.map(()=>'<i></i>').join('');let i=-1,t=null;
const show=n=>{i=n;fr.contentWindow.postMessage({tour:n},'*');cap.style.opacity=0;setTimeout(()=>{cap.textContent=CAP[n];cap.style.opacity=1},250);[...dots.children].forEach((d,k)=>d.classList.toggle('on',k===n));};
const stop=()=>{clearInterval(t);t=null;shot.classList.remove('touring');lab.textContent=i>=CAP.length-1?'Play it again':'Keep going';};
btn.onclick=()=>{if(t){stop();return;}shot.classList.add('touring');lab.textContent='Pause';if(i>=CAP.length-1)i=-1;show(i+1);t=setInterval(()=>{if(i>=CAP.length-1){stop();return;}show(i+1);},4300);};
dots.onclick=e=>{const k=[...dots.children].indexOf(e.target);if(k>=0){show(k);}};
})();

/* Orbit v1.1: Customer / Community / Client switch under the Customer Experience room */
(function(){var B=(window.ORBIT_HUB||'').replace(/orbit\/hub-demo\.html$/,'');var V={customer:['Customer Experience','First order, delivery, the next buy, loyalty','c768620e99.jpg'],community:['Community Engagement','From first look to inner circle','cx-community.jpg'],client:['Client Success','From yes to a glowing wrap-up','cx-client.jpg']};
var sw=document.querySelector('.cxsw');var btn=document.querySelector('.hp[data-h="cs"]');var img=document.querySelector('img[data-room="cs"]');if(!sw||!btn||!img)return;
sw.addEventListener('click',function(e){var b=e.target.closest('button[data-cx]');if(!b)return;var v=V[b.dataset.cx];sw.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-selected',x===b)});
btn.querySelector('b').textContent=v[0];btn.querySelector('span').textContent=v[1];img.src=B+'orbit/'+v[2];img.alt=v[0]+' room';});})();
