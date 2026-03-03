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

function setLoading(msg) {
  if (loading) loading.textContent = msg || 'Please wait...';
}
const resultCard = document.getElementById('resultCard');
const scoreText = document.getElementById('scoreText');
const okInput = document.getElementById('okInput');
const okBtn = document.getElementById('okBtn');
const apiStatus = document.getElementById('apiStatus');
const giftModal = document.getElementById('giftModal');
const giftHandle = document.getElementById('giftHandle');
const giftSubmit = document.getElementById('giftSubmit');
const giftCancel = document.getElementById('giftCancel');
const giftMsg = document.getElementById('giftMsg');
let paperMeta = '';

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

async function refreshApiStatus() {
  if (!apiStatus) return;
  try {
    const r = await fetch(`/olvl-api/health?t=${Date.now()}`, { cache: 'no-store' });
    if (!r.ok) throw new Error('down');
    apiStatus.textContent = 'Real-time AI marker: online';
    apiStatus.style.color = '#45c16d';
  } catch (_) {
    apiStatus.textContent = 'Real-time AI marker: offline';
    apiStatus.style.color = '#ff6b6b';
  }
}

function openGiftModal() {
  if (!giftModal) return;
  giftModal.classList.remove('hidden');
  giftHandle.value = '';
  giftMsg.textContent = '';
  setTimeout(() => giftHandle.focus(), 50);
}

function closeGiftModal() {
  if (!giftModal) return;
  giftModal.classList.add('hidden');
}

if (giftCancel) giftCancel.onclick = closeGiftModal;
if (giftSubmit) giftSubmit.onclick = async () => {
  const h = (giftHandle.value || '').trim();
  if (!h || !h.startsWith('@')) {
    giftMsg.textContent = 'Please enter a valid Telegram handle (e.g. @username).';
    giftMsg.style.color = '#ff6b6b';
    return;
  }
  const subjText = subjectSelect.options[subjectSelect.selectedIndex]?.text || 'Selected subject';
  giftMsg.textContent = 'Submitting claim...';
  giftMsg.style.color = '#9aa5b5';
  try {
    const r = await fetch('/olvl-api/claim', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ handle: h, subject: subjText, paperId: lastPaperId, percent: 100 })
    });
    if (!r.ok) throw new Error('claim failed');
    giftMsg.textContent = 'submitted / pending manual processing (if gift not given yet)';
    giftMsg.style.color = '#45c16d';
  } catch (e) {
    giftMsg.textContent = 'Claim saved locally, but auto-forward failed. Please send your @username in this chat manually.';
    giftMsg.style.color = '#ff6b6b';
  }
};

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

function mapFromApi(p) {
  const subjectLabel = SUBJECTS.find(s => s.id === p.subject)?.label || p.subject;
  if (p.type === 'mcq') {
    return {
      subject: subjectLabel,
      type: 'mcq',
      marks: p.marks,
      q: p.question,
      choices: p.choices,
      answer: p.answer,
      keywords: p.keywords || []
    };
  }
  return {
    subject: subjectLabel,
    type: p.type,
    marks: p.marks,
    q: p.question,
    keywords: p.keywords || []
  };
}

let lastPaperId = '';

async function fetchPaper(key) {
  const res = await fetch(`/olvl-api/generate-paper?t=${Date.now()}`, {
    method: 'POST',
    cache: 'no-store',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ subject: key, count: 20 })
  });
  if (!res.ok) throw new Error('generate failed');
  const data = await res.json();
  return { paper: (data.paper || []).map(mapFromApi), paperId: data.paperId || '' };
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
  row.innerHTML = `<button type="submit">Mark Now</button><span class="muted">Total: ${totalMarks} marks · SG style hard practice${paperMeta}</span>`;
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

async function generateSet() {
  setLoading('Generating new paper...');
  loading.classList.remove('hidden');
  questionForm.classList.add('hidden');
  resultCard.classList.add('hidden');
  try {
    let fetched = await fetchPaper(subjectSelect.value);
    let candidate = fetched.paper;
    let pid = fetched.paperId;
    let tries = 0;
    while ((signatureOf(candidate) === lastSetSignature || (pid && pid === lastPaperId)) && tries < 5) {
      fetched = await fetchPaper(subjectSelect.value);
      candidate = fetched.paper;
      pid = fetched.paperId;
      tries++;
    }
    currentSet = candidate;
    lastSetSignature = signatureOf(currentSet);
    lastPaperId = pid;
    paperMeta = pid ? ` · Paper ID: ${pid.slice(0,8)}` : '';
    renderQuestions();
    questionForm.classList.remove('hidden');
  } catch (e) {
    alert('Failed to generate paper. Please try again.');
  } finally {
    loading.classList.add('hidden');
  }
}

startBtn.onclick = generateSet;

questionForm.onsubmit = async (e) => {
  e.preventDefault();
  const data = new FormData(questionForm);
  const answers = {};
  currentSet.forEach((_, i) => {
    const v = data.get(`q${i}`);
    answers[String(i)] = v == null ? '' : String(v);
  });

  setLoading('Marking answers...');
  loading.classList.remove('hidden');
  try {
    const res = await fetch('/olvl-api/mark-paper', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paper: currentSet.map((q)=>({
        subject: (SUBJECTS.find(s=>s.label===q.subject)?.id || q.subject || '').toLowerCase().replace(/[^a-z]/g,''),
        type: q.type,
        marks: q.marks,
        question: q.q,
        choices: q.choices,
        answer: q.answer,
        keywords: q.keywords || []
      })), answers })
    });
    if (!res.ok) throw new Error('mark failed');
    const out = await res.json();
    const r = out.result;

    scoreText.textContent = `Score: ${r.score}/${r.total} (${r.percent}%)`;

    const oldPrize = document.getElementById('prizeNotice');
    if (oldPrize) oldPrize.remove();
    if (r.percent === 100) {
      openGiftModal();
    }

    const old = document.getElementById('feedbackList');
    if (old) old.remove();
    const p = document.createElement('pre');
    p.id = 'feedbackList';
    p.style.whiteSpace = 'pre-wrap';
    p.style.fontSize = '13px';
    p.textContent = (r.details || []).map(d => {
      const base = `Q${d.q}: ${d.score}/${d.max} (${d.feedback})`;
      const reason = d.reason ? `\n  Reason: ${d.reason}` : '';
      const correct = d.correctAnswer ? `\n  Correct answer: ${d.correctAnswer}` : '';
      return `${base}${reason}${correct}`;
    }).join('\n');
    resultCard.appendChild(p);

    resultCard.classList.remove('hidden');
  } catch (err) {
    alert('Failed to mark paper. Please retry.');
  } finally {
    loading.classList.add('hidden');
  }
};

okBtn.onclick = () => {
  if (okInput.value.trim().toLowerCase() === 'ok') {
    okInput.value = '';
    generateSet();
  }
};

populateSubjects();
refreshApiStatus();
setInterval(refreshApiStatus, 15000);
if (localStorage.getItem(SESSION_KEY) === '1') showExam();