const PASSWORD = 'eva';
const SESSION_KEY = 'sg_exam_unlocked';

const BANK = {
  english: {
    label: 'English (O-Level)',
    questions: [
      {q:'Choose the grammatically correct sentence.', c:['Neither of the boys were ready.','Neither of the boys was ready.','Neither boys was ready.','Neither of boys were ready.'], a:1},
      {q:'Best replacement: "She insisted ____ paying for dinner."', c:['on','to','for','at'], a:0},
      {q:'Tone of phrase "a cautiously optimistic outlook" is...', c:['angry','hopeful but careful','sarcastic','indifferent'], a:1},
      {q:'Most suitable thesis sentence for formal writing:', c:['I kinda think school is stressful.','School stress can be reduced through structured rest and planning.','School is bad lol.','Everybody knows stress is everywhere.'], a:1},
      {q:'Correct punctuation:', c:['The principal said "Work hard, rest well."','The principal said, "Work hard, rest well."','The principal, said "Work hard, rest well".','The principal said "Work hard rest well."'], a:1},
      {q:'Best concluding phrase in argumentative writing:', c:['Whatever lah, that is all.','In conclusion, the policy should be reviewed with measurable safeguards.','So yeah, done.','Thanks for reading my rant.'], a:1},
    ]
  },
  emath: {
    label: 'E-Math (O-Level)',
    questions: [
      {q:'Solve 3(2x−5)=2(x+7)−9', c:['x=5','x=4','x=3','x=2'], a:2},
      {q:'Roots of x²−7x+10=0 are', c:['2 and 5','-2 and -5','1 and 10','3 and 4'], a:0},
      {q:'20% discount gives price $120. Original price?', c:['$130','$144','$150','$160'], a:2},
      {q:'Mean of 4,7,7,9,13', c:['7','8','8.2','9'], a:2},
      {q:'Gradient through (2,-1) and (6,7)', c:['1','2','-2','4'], a:1},
      {q:'If y=2x+3 and x=5, y=?', c:['10','11','12','13'], a:3},
    ]
  },
  amath: {
    label: 'A-Math (O-Level)',
    questions: [
      {q:'Differentiate y=3x²−4x+7', c:['6x−4','3x−4','6x+4','2x−4'], a:0},
      {q:'Solve 2^x = 16', c:['2','3','4','8'], a:2},
      {q:'Factor x²+5x+6', c:['(x+2)(x+3)','(x-2)(x-3)','(x+1)(x+6)','Prime'], a:0},
      {q:'sin 30° =', c:['1','1/2','√3/2','0'], a:1},
      {q:'If log10 a = 2, then a =', c:['10','20','100','1000'], a:2},
      {q:'Integrate 4x dx', c:['2x² + C','4x + C','x⁴ + C','8x + C'], a:0},
    ]
  },
  combsci: {
    label: 'Combined Science (O-Level)',
    questions: [
      {q:'Magnesium + hydrochloric acid forms...', c:['MgCl + H₂','MgCl₂ + H₂','MgOH + Cl₂','Mg + HCl₂'], a:1},
      {q:'Higher reaction rate is mainly due to...', c:['fewer collisions','lower temperature','more frequent successful collisions','larger particle mass only'], a:2},
      {q:'Speed formula is', c:['distance × time','distance / time','time / distance','force / mass'], a:1},
      {q:'Osmosis involves movement of...', c:['solute from high to low','water through partially permeable membrane','gas through stomata','ions through metal'], a:1},
      {q:'pH 2 solution is', c:['alkali','neutral','acidic','salt only'], a:2},
      {q:'F = ma. If m=900kg, a=2m/s², F=?', c:['450N','902N','1800N','900N'], a:2},
    ]
  },
  purechem: {
    label: 'Pure Chemistry (O-Level)',
    questions: [
      {q:'Mole concept: moles =', c:['mass × Mr','mass / Mr','Mr / mass','mass + Mr'], a:1},
      {q:'Acid + base reaction is called', c:['combustion','neutralisation','displacement','decomposition'], a:1},
      {q:'Electrolysis of molten lead(II) bromide gives bromine at...', c:['cathode','anode','both','none'], a:1},
      {q:'More reactive metal displaces less reactive metal from...', c:['water only','salt solution','air','alkali only'], a:1},
      {q:'Catalyst function is to', c:['increase yield only','lower activation energy','raise activation energy','be consumed completely'], a:1},
      {q:'Empirical formula is', c:['actual atom count','simplest whole-number ratio','molar mass','ionic charge'], a:1},
    ]
  },
  purephys: {
    label: 'Pure Physics (O-Level)',
    questions: [
      {q:'Unit of force is', c:['J','N','W','Pa'], a:1},
      {q:'Power =', c:['work/time','force×distance only','mass×acceleration','energy×time'], a:0},
      {q:'Wave with frequency 5Hz has period', c:['5s','0.5s','0.2s','2s'], a:2},
      {q:'Current is measured in', c:['V','A','Ω','C'], a:1},
      {q:'Object at constant velocity has resultant force', c:['maximum','zero','infinite','unknown always'], a:1},
      {q:'Density =', c:['mass/volume','volume/mass','mass×volume','weight/volume'], a:0},
    ]
  },
  purebio: {
    label: 'Pure Biology (O-Level)',
    questions: [
      {q:'Main site of aerobic respiration in cells', c:['nucleus','ribosome','mitochondrion','vacuole'], a:2},
      {q:'Enzymes are mostly', c:['lipids','proteins','carbohydrates','DNA'], a:1},
      {q:'Xylem transports mainly', c:['sugars','water and minerals','oxygen','amino acids only'], a:1},
      {q:'Natural selection favors organisms that', c:['never mutate','best survive and reproduce','are largest only','have shortest lifespan'], a:1},
      {q:'Photosynthesis requires', c:['chlorophyll, light, CO₂, water','oxygen and glucose only','nitrogen only','heat only'], a:0},
      {q:'Red blood cells primarily carry', c:['hormones','oxygen','antibodies','enzymes'], a:1},
    ]
  },
  humanities: {
    label: 'SS/History/Geography (O-Level)',
    questions: [
      {q:'In SBQ, reliability is judged by', c:['font size','provenance + cross-reference','source length','writer’s age only'], a:1},
      {q:'Urban heat island effect means', c:['cities colder than rural','cities warmer than rural','equal temperatures','only at noon'], a:1},
      {q:'Globalisation can affect local jobs by', c:['reducing all jobs','shifting demand for skills','ending trade','removing technology'], a:1},
      {q:'A balanced SRQ paragraph uses', c:['PEEL','random facts','one sentence','rhetorical questions only'], a:0},
      {q:'Multicultural harmony in SG often supported by', c:['segregation','shared norms and policies','no laws','single language only'], a:1},
      {q:'Best evidence for claim strength is', c:['personal guess','specific example/data','all caps statement','repetition'], a:1},
    ]
  },
  poa: {
    label: 'POA (O-Level)',
    questions: [
      {q:'Assets =', c:['Liabilities + Capital','Capital - Liabilities','Income - Expenses','Cash only'], a:0},
      {q:'Credit sale entry affects', c:['Sales and Accounts Receivable','Purchases and Cash','Bank and Wages','Inventory only'], a:0},
      {q:'Trial balance checks mainly', c:['profit correctness','arithmetical accuracy','cash flow only','ethics'], a:1},
      {q:'Depreciation is', c:['increase in asset value','allocation of asset cost over useful life','cash payment only','fraud adjustment'], a:1},
      {q:'Gross profit =', c:['Sales - Cost of Sales','Revenue - Expenses','Cash - Bank','Assets - Liabilities'], a:0},
      {q:'Bank reconciliation helps detect', c:['weather changes','timing differences/errors','tax rates only','inventory loss only'], a:1},
    ]
  }
};

const lockScreen = document.getElementById('lockScreen');
const examScreen = document.getElementById('examScreen');
const passwordInput = document.getElementById('passwordInput');
const unlockBtn = document.getElementById('unlockBtn');
const lockMsg = document.getElementById('lockMsg');
const logoutBtn = document.getElementById('logoutBtn');
const subjectSelect = document.getElementById('subjectSelect');
const startBtn = document.getElementById('startBtn');
const questionForm = document.getElementById('questionForm');
const loading = document.getElementById('loading');
const resultCard = document.getElementById('resultCard');
const scoreText = document.getElementById('scoreText');
const okInput = document.getElementById('okInput');
const okBtn = document.getElementById('okBtn');

let currentSet = [];
let currentSubject = 'english';

Object.entries(BANK).forEach(([k,v])=>{
  const opt = document.createElement('option');
  opt.value = k; opt.textContent = v.label;
  subjectSelect.appendChild(opt);
});

function showExam() { lockScreen.classList.add('hidden'); examScreen.classList.remove('hidden'); }
function showLock() { examScreen.classList.add('hidden'); lockScreen.classList.remove('hidden'); }

unlockBtn.onclick = () => {
  if (passwordInput.value === PASSWORD) {
    localStorage.setItem(SESSION_KEY, '1');
    lockMsg.textContent = '';
    showExam();
  } else lockMsg.textContent = 'Wrong password';
};

logoutBtn.onclick = () => { localStorage.removeItem(SESSION_KEY); showLock(); };

function sample(arr, n=6){
  const copy = [...arr].sort(()=>Math.random()-0.5);
  return copy.slice(0, Math.min(n, arr.length));
}

function renderQuestions(){
  questionForm.innerHTML = '';
  currentSet.forEach((item, idx)=>{
    const box = document.createElement('div');
    box.className = 'q';
    box.innerHTML = `<h4>Q${idx+1}. ${item.q}</h4>` + item.c.map((ch, i)=>
      `<label class="choice"><input type="radio" name="q${idx}" value="${i}" required> ${String.fromCharCode(65+i)}. ${ch}</label>`).join('');
    questionForm.appendChild(box);
  });
  const row = document.createElement('div');
  row.className = 'submitRow';
  row.innerHTML = `<button type="submit">Mark Now</button><span class="muted">MCQ style · instant marking</span>`;
  questionForm.appendChild(row);
}

function generateSet(){
  currentSubject = subjectSelect.value;
  loading.classList.remove('hidden');
  questionForm.classList.add('hidden');
  resultCard.classList.add('hidden');
  setTimeout(()=>{
    currentSet = sample(BANK[currentSubject].questions, 6);
    renderQuestions();
    loading.classList.add('hidden');
    questionForm.classList.remove('hidden');
  }, 900);
}

startBtn.onclick = generateSet;

questionForm.onsubmit = (e)=>{
  e.preventDefault();
  const data = new FormData(questionForm);
  let score = 0;
  currentSet.forEach((q, i)=>{
    const pick = Number(data.get(`q${i}`));
    if (pick === q.a) score++;
  });
  scoreText.textContent = `Score: ${score}/${currentSet.length}`;
  resultCard.classList.remove('hidden');
};

okBtn.onclick = ()=>{
  if (okInput.value.trim().toLowerCase() === 'ok') {
    okInput.value = '';
    generateSet();
  }
};

if (localStorage.getItem(SESSION_KEY) === '1') showExam();
