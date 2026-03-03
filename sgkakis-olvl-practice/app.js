const PASSWORD = 'eva';
const SESSION_KEY = 'sg_exam_unlocked';

const SUBJECTS = [
  { id: 'english', label: 'English' },
  { id: 'emath', label: 'E-Math' },
  { id: 'amath', label: 'A-Math' },
  { id: 'combsci', label: 'Combined Science' },
  { id: 'purechem', label: 'Pure Chemistry' },
  { id: 'purephys', label: 'Pure Physics' },
  { id: 'purebio', label: 'Pure Biology' },
  { id: 'humanities', label: 'Humanities (SS/Hist/Geog)' },
  { id: 'poa', label: 'POA' }
];

const BANK = {
  english: [
    { type: 'mcq', marks: 2, q: 'Choose the strongest thesis sentence for an argumentative essay on device use in schools.', choices: ['Phones are bad.', 'Schools should enforce structured phone-free periods to improve focus and sleep hygiene.', 'I think phones maybe should be less.', 'Everyone knows phones are distracting.'], answer: 1 },
    { type: 'short', marks: 4, q: 'Write one assumption in: “Homework should be reduced because many students already attend tuition.”', keywords: ['tuition', 'effective', 'same learning', 'enough support'] },
    { type: 'structured', marks: 6, q: 'In 4–6 sentences, evaluate whether school-based support can reduce tuition dependence in Singapore. Give one argument and one limitation.', keywords: ['support', 'access', 'equity', 'limitation', 'resource', 'teacher'] }
  ],
  emath: [
    { type: 'mcq', marks: 2, q: 'Solve: 3(2x−5)=2(x+7)−9', choices: ['x=5', 'x=4', 'x=3', 'x=2'], answer: 2 },
    { type: 'short', marks: 4, q: 'A jacket is sold at $120 after a 20% discount. Find original price.', keywords: ['150'] },
    { type: 'structured', marks: 6, q: 'A line passes through (2,-1) and (6,7). Find gradient and equation in y=mx+c form with full working.', keywords: ['2', 'y=2x-5', 'm=2'] }
  ],
  amath: [
    { type: 'mcq', marks: 2, q: 'Differentiate y=3x²−4x+7', choices: ['6x−4', '3x−4', '6x+4', '2x−4'], answer: 0 },
    { type: 'short', marks: 4, q: 'Solve 2^x=16', keywords: ['4'] },
    { type: 'structured', marks: 6, q: 'Solve x²−7x+10=0 and explain briefly how factorisation confirms both roots.', keywords: ['2', '5', 'factor', '(x-2)(x-5)'] }
  ],
  combsci: [
    { type: 'mcq', marks: 2, q: 'In collision theory, reaction rate increases when...', choices: ['fewer particles collide', 'activation energy increases', 'frequency of successful collisions increases', 'temperature decreases'], answer: 2 },
    { type: 'short', marks: 4, q: 'A car travels 150m in 12s. Calculate speed (m/s).', keywords: ['12.5'] },
    { type: 'structured', marks: 6, q: 'Explain why powdered CaCO3 reacts faster than marble chips with same HCl volume/concentration. Include one controlled variable.', keywords: ['surface area', 'collision', 'successful', 'temperature', 'concentration'] }
  ],
  purechem: [
    { type: 'mcq', marks: 2, q: 'Acid + base reaction is called', choices: ['combustion', 'neutralisation', 'displacement', 'decomposition'], answer: 1 },
    { type: 'short', marks: 4, q: '25.0 cm3 of 0.200 mol/dm3 HCl reacts with NaOH. Find moles of HCl.', keywords: ['0.005', '5.00x10^-3'] },
    { type: 'structured', marks: 6, q: 'Describe and explain observations when magnesium is added to dilute hydrochloric acid. Include balanced symbol equation.', keywords: ['effervescence', 'hydrogen', 'Mg + 2HCl', 'MgCl2', 'exothermic'] }
  ],
  purephys: [
    { type: 'mcq', marks: 2, q: 'Resultant force when object moves at constant velocity is', choices: ['maximum', 'zero', 'increasing', 'unknown'], answer: 1 },
    { type: 'short', marks: 4, q: 'If mass=900kg and acceleration=2m/s², find resultant force.', keywords: ['1800'] },
    { type: 'structured', marks: 6, q: 'A wave has frequency 5Hz. Calculate period and explain one real-world factor that can affect wave speed.', keywords: ['0.2', 'medium', 'density', 'temperature'] }
  ],
  purebio: [
    { type: 'mcq', marks: 2, q: 'Main function of red blood cells is to transport', choices: ['antibodies', 'oxygen', 'hormones', 'enzymes'], answer: 1 },
    { type: 'short', marks: 4, q: 'State two differences between diffusion and osmosis.', keywords: ['particles', 'water', 'partially permeable', 'concentration gradient'] },
    { type: 'structured', marks: 6, q: 'Explain how enzyme activity is affected by temperature, including denaturation.', keywords: ['optimum', 'kinetic', 'collision', 'denature', 'active site'] }
  ],
  humanities: [
    { type: 'mcq', marks: 2, q: 'A strong SBQ reliability paragraph should include', choices: ['writer age only', 'provenance and cross-reference', 'long quotes only', 'own opinion only'], answer: 1 },
    { type: 'short', marks: 4, q: 'Give one impact of urban heat island effect in Singapore.', keywords: ['higher temperature', 'energy demand', 'health', 'discomfort'] },
    { type: 'structured', marks: 6, q: '“Meritocracy is fully fair in practice.” Evaluate this statement with one support and one challenge (PEEL style).', keywords: ['opportunity', 'mobility', 'advantage', 'inequality', 'policy'] }
  ],
  poa: [
    { type: 'mcq', marks: 2, q: 'Accounting equation is', choices: ['Assets = Liabilities + Capital', 'Capital = Assets + Liabilities', 'Profit = Assets - Liabilities', 'Cash = Revenue - Expenses'], answer: 0 },
    { type: 'short', marks: 4, q: 'If sales=$8000 and cost of sales=$5000, find gross profit.', keywords: ['3000'] },
    { type: 'structured', marks: 6, q: 'Explain why bank reconciliation is needed and give two common reconciling items.', keywords: ['timing', 'cheque', 'deposit in transit', 'bank charges', 'errors'] }
  ]
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
let lastSetSignature = '';

function populateSubjects() {
  const integrated = document.createElement('option');
  integrated.value = 'integrated';
  integrated.textContent = 'Integrated Hard Paper (All Subjects)';
  subjectSelect.appendChild(integrated);
  SUBJECTS.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.id;
    opt.textContent = `${s.label} (Hard)`;
    subjectSelect.appendChild(opt);
  });
}

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

function shuffle(arr){ return [...arr].sort(()=>Math.random()-0.5); }

function signatureOf(set) {
  return set.map(q => `${q.subject}|${q.type}|${q.q}`).join('||');
}

function buildPaper(key) {
  if (key === 'integrated') {
    let core = [];
    let leftovers = [];

    SUBJECTS.forEach(s => {
      const pool = shuffle(BANK[s.id]);
      const tagged = pool.map(q => ({ ...q, subject: s.label }));
      core.push(...tagged.slice(0, 2));           // 18 core questions
      leftovers.push(...tagged.slice(2));         // remaining candidates
    });

    // top up to 20 questions
    const extra = shuffle(leftovers).slice(0, 2);
    return shuffle([...core, ...extra]);
  }

  // single-subject hard paper -> exactly 20 questions via shuffled repeats/variants from bank
  const base = BANK[key].map(q => ({ ...q, subject: SUBJECTS.find(s => s.id === key)?.label || key }));
  const out = [];
  while (out.length < 20) {
    out.push(...shuffle(base).map(x => ({ ...x })));
  }
  return shuffle(out.slice(0, 20));
}

function renderQuestions() {
  questionForm.innerHTML = '';
  let totalMarks = 0;
  currentSet.forEach((item, idx) => {
    totalMarks += item.marks;
    const box = document.createElement('div');
    box.className = 'q';
    const typeLabel = item.type === 'mcq' ? 'MCQ' : (item.type === 'short' ? 'Short Response' : 'Structured Response');
    let body = '';
    if (item.type === 'mcq') {
      body = item.choices.map((ch, i) => `<label class="choice"><input type="radio" name="q${idx}" value="${i}" required> ${String.fromCharCode(65+i)}. ${ch}</label>`).join('');
    } else {
      body = `<textarea name="q${idx}" rows="${item.type === 'short' ? 3 : 5}" style="width:100%;margin-top:8px;background:#0f141c;color:#eef2f7;border:1px solid #2b3240;border-radius:10px;padding:10px" placeholder="Write your answer..."></textarea>`;
    }
    box.innerHTML = `<h4>Q${idx+1}. [${item.subject}] ${item.q}</h4><div class="muted">${typeLabel} · ${item.marks} marks</div>${body}`;
    questionForm.appendChild(box);
  });
  const row = document.createElement('div');
  row.className = 'submitRow';
  row.innerHTML = `<button type="submit">Mark Now</button><span class="muted">Total: ${totalMarks} marks · SG style hard practice</span>`;
  questionForm.appendChild(row);
}

function normalize(s){ return (s||'').toLowerCase().replace(/\s+/g,' ').trim(); }

function markText(answer, keywords, maxMarks) {
  const a = normalize(answer);
  if (!a) return { got: 0, note: 'No answer provided.' };
  let hits = 0;
  keywords.forEach(k => {
    const kk = normalize(k);
    if (kk && a.includes(kk)) hits++;
  });
  const ratio = Math.min(1, hits / Math.max(2, keywords.length));
  const lenBonus = a.length > 140 ? 0.15 : 0;
  const score = Math.min(maxMarks, Math.max(1, Math.round((ratio + lenBonus) * maxMarks)));
  return { got: score, note: `Matched ${hits}/${keywords.length} key points.` };
}

function generateSet() {
  loading.classList.remove('hidden');
  questionForm.classList.add('hidden');
  resultCard.classList.add('hidden');
  setTimeout(() => {
    let candidate = buildPaper(subjectSelect.value);
    let tries = 0;
    while (signatureOf(candidate) === lastSetSignature && tries < 8) {
      candidate = buildPaper(subjectSelect.value);
      tries++;
    }
    currentSet = candidate;
    lastSetSignature = signatureOf(currentSet);
    renderQuestions();
    loading.classList.add('hidden');
    questionForm.classList.remove('hidden');
  }, 1100);
}

startBtn.onclick = generateSet;

questionForm.onsubmit = (e) => {
  e.preventDefault();
  const data = new FormData(questionForm);
  let scored = 0;
  let total = 0;
  const feedback = [];

  currentSet.forEach((q, i) => {
    total += q.marks;
    if (q.type === 'mcq') {
      const pick = Number(data.get(`q${i}`));
      const got = pick === q.answer ? q.marks : 0;
      scored += got;
      feedback.push(`Q${i+1}: ${got}/${q.marks} (${got ? 'Correct' : 'Incorrect'})`);
    } else {
      const ans = data.get(`q${i}`) || '';
      const r = markText(ans, q.keywords, q.marks);
      scored += r.got;
      feedback.push(`Q${i+1}: ${r.got}/${q.marks} (${r.note})`);
    }
  });

  const pct = Math.round((scored/Math.max(1,total))*100);
  scoreText.textContent = `Score: ${scored}/${total} (${pct}%)`;

  const old = document.getElementById('feedbackList');
  if (old) old.remove();
  const p = document.createElement('pre');
  p.id = 'feedbackList';
  p.style.whiteSpace = 'pre-wrap';
  p.style.fontSize = '13px';
  p.textContent = feedback.join('\n');
  resultCard.appendChild(p);

  resultCard.classList.remove('hidden');
};

okBtn.onclick = () => {
  if (okInput.value.trim().toLowerCase() === 'ok') {
    okInput.value = '';
    generateSet();
  }
};

populateSubjects();
if (localStorage.getItem(SESSION_KEY) === '1') showExam();