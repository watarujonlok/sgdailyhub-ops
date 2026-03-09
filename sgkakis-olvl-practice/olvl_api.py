#!/usr/bin/env python3
import json, random, uuid, os
from urllib.parse import urlparse
from urllib import request, parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SUBJECTS = ["english","emath","amath","combsci","purechem","purephys","purebio","humanities","poa"]
LAST_SIGNATURE = {}
RECENT_QUESTIONS = {}  # subject -> recent question stems across papers
RECENT_PAPERS = {}     # subject -> list[list[stem]] last N papers


def semantic_signature(q):
    """Light semantic dedupe key for language-heavy subjects.
    Prevent near-identical prompts that differ only by audience words.
    """
    import re
    s = (q.get('question') or '').lower().strip()
    # normalize numbers/placeholders
    s = re.sub(r"\d+(?:\.\d+)?", "<n>", s)
    # normalize audience slot for common english prompt templates
    s = re.sub(r"to\s+.+?\s+on whether", "to <audience> on whether", s)
    s = re.sub(r"to\s+.+?\s+against the statement", "to <audience> against the statement", s)
    # remove common audience tokens that can create superficial variation
    s = re.sub(r"\b(parents?|students?|school leaders?|moe officers?|a principal|teachers' committee|school board|education policy panel)\b", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return f"{q.get('subject','')}|{q.get('type','')}|{s}"

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', '').strip()
TG_CHAT_ID = os.environ.get('TG_CHAT_ID', '').strip()



def q_mcq(subject, q, choices, answer, marks=2, points=None, concept=None):
    return {
        "subject": subject,
        "type": "mcq",
        "marks": marks,
        "question": q,
        "choices": choices,
        "answer": answer,
        "keywords": points or [],
        "concept": concept or "general"
    }


def q_text(subject, qtype, q, marks=4, points=None, concept=None):
    return {
        "subject": subject,
        "type": qtype,
        "marks": marks,
        "question": q,
        "keywords": points or [],
        "concept": concept or "general"
    }


def gen_english():
    topic = random.choice(["social media use", "device-free recess", "homework load", "tuition dependence", "sleep hygiene"])
    return random.choice([
        q_mcq("english", f"Choose the strongest thesis sentence for an essay on {topic}.",
              ["This is bad.", "This issue deserves balanced policy reform with measurable outcomes.", "I don’t like this.", "Everyone says this matters."], 1, points=["thesis", "academic tone"], concept="thesis-mcq"),
        q_text("english", "short", f"State one assumption in this claim: '{topic.title()} should be reduced in schools.'", 4,
               points=["assumption", "evidence", "context"], concept="assumption-short"),
        q_text("english", "structured", f"In 5-7 sentences, evaluate one benefit and one limitation of policies on {topic} in Singapore.", 6,
               points=["benefit", "limitation", "evidence", "evaluation"], concept="policy-eval-structured")])


def gen_emath():
    a = random.randint(2, 7); b = random.randint(1, 9); c = random.randint(2, 6)
    x = random.randint(2, 9)
    y = a * x + b
    return random.choice([
        q_mcq("emath", f"Solve: {a}(x-{b}) = {c}(x+{b})", ["x=1", f"x={x}", "x=0", f"x={x+1}"], 1, points=[str(x)]),
        q_text("emath", "short", f"A price is discounted by {random.choice([15,20,25,30])}% to $ {y*10}. Find original price.", 4, points=["percentage", "original price"]),
        q_text("emath", "structured", f"Line passes through ({x},{b}) and ({x+4},{b+8}). Find gradient and equation in y=mx+c.", 6,
               points=["gradient", "equation", "working"])])


def gen_amath():
    n = random.randint(2, 6)
    return random.choice([
        q_mcq("amath", f"Differentiate y={n}x^3-4x^2+2", [f"{3*n}x^2-8x", f"{n}x^2-8x", f"{3*n}x-8", "None"], 0,
              points=["differentiate"]),
        q_text("amath", "short", f"Solve 2^x = {2**random.randint(3,7)}", 4, points=["log", "power"]),
        q_text("amath", "structured", f"Solve x^2-{random.randint(7,12)}x+{random.randint(18,35)}=0 and show method.", 6,
               points=["factorise", "roots", "check"])])


def gen_combsci():
    return random.choice([
        q_mcq("combsci", "Higher reaction rate is mainly due to...",
              ["fewer collisions", "more frequent successful collisions", "lower concentration", "decrease in particles"], 1,
              points=["collision theory"]),
        q_text("combsci", "short", f"A runner travels {random.choice([120,150,180,210])} m in {random.choice([10,12,15,18])} s. Find speed.", 4,
               points=["speed", "distance/time"]),
        q_text("combsci", "structured", "Explain why powdered carbonate reacts faster than chips with same acid. Include one controlled variable.", 6,
               points=["surface area", "successful collisions", "control variable"])])


def gen_purechem():
    mol = random.choice([0.20, 0.25, 0.40]); vol = random.choice([20.0, 25.0, 30.0])
    return random.choice([
        q_mcq("purechem", "Acid + carbonate produces", ["salt+water", "salt+water+CO2", "salt+H2", "salt only"], 1,
              points=["co2", "salt", "water"], concept="reaction-products"),
        q_text("purechem", "short", f"Find moles in {vol} cm3 of {mol:.2f} mol/dm3 NaOH.", 4, points=["moles", "convert cm3 to dm3"], concept="mole-calculation"),
        q_text("purechem", "structured", "Describe observations and write balanced equation for magnesium + dilute hydrochloric acid.", 6,
               points=["effervescence", "hydrogen", "balanced equation"], concept="acid-metal-reaction")])


def gen_purephys():
    m = random.choice([800, 900, 1200]); a = random.choice([1.5, 2.0, 2.5])
    return random.choice([
        q_mcq("purephys", "If velocity is constant, resultant force is", ["positive", "negative", "zero", "maximum"], 2,
              points=["newton first law"]),
        q_text("purephys", "short", f"Calculate force when mass={m} kg and acceleration={a} m/s^2.", 4,
               points=["F=ma"]),
        q_text("purephys", "structured", f"A wave has frequency {random.choice([4,5,8,10])} Hz. Find period and explain one factor affecting wave speed.", 6,
               points=["period", "medium", "speed factor"])])


def gen_purebio():
    return random.choice([
        q_mcq("purebio", "Osmosis is movement of", ["any molecules", "water through partially permeable membrane", "ions only", "oxygen"], 1,
              points=["water", "partially permeable membrane"]),
        q_text("purebio", "short", "State two differences between arteries and veins.", 4,
               points=["thick walls", "valves", "pressure", "lumen"]),
        q_text("purebio", "structured", "Explain effect of temperature on enzyme activity, including denaturation.", 6,
               points=["optimum", "kinetic energy", "active site", "denature"])])


def gen_humanities():
    issue = random.choice(["meritocracy", "globalisation", "urban heat island", "social mobility"])
    return random.choice([
        q_mcq("humanities", "Best SBQ reliability method is", ["quote length", "cross-reference + provenance", "author age", "emotive words only"], 1,
              points=["cross-reference", "provenance"], concept="sbq-mcq"),
        q_text("humanities", "short", f"State one impact of {issue} on Singapore society/economy.", 4,
               points=["impact", "example", "Singapore context"], concept="impact-short"),
        q_text("humanities", "structured", f"Evaluate the statement: '{issue.title()} policy outcomes are fully fair.' Give one support and one challenge.", 6,
               points=["support", "challenge", "evidence", "evaluation"], concept="policy-eval-structured")])


def gen_poa():
    rev = random.choice([8500, 9200, 9500]); exp = random.choice([5400, 6200, 7100])
    return random.choice([
        q_mcq("poa", "Accounting equation is", ["Assets=Liabilities+Capital", "Capital=Assets+Liabilities", "Profit=Assets-Liabilities", "Cash=Revenue-Expenses"], 0,
              points=["accounting equation"]),
        q_text("poa", "short", f"If revenue=${rev} and expenses=${exp}, find profit.", 4,
               points=["profit", "revenue-expenses"]),
        q_text("poa", "structured", "Explain why trial balance may still balance despite errors. Give two examples.", 6,
               points=["omission", "commission", "principle", "compensating errors"])])


def gen_one(subject):
    return {
        "english": gen_english,
        "emath": gen_emath,
        "amath": gen_amath,
        "combsci": gen_combsci,
        "purechem": gen_purechem,
        "purephys": gen_purephys,
        "purebio": gen_purebio,
        "humanities": gen_humanities,
        "poa": gen_poa,
    }.get(subject, gen_english)()


def synthesize_variant(subject, nonce, force_type=None):
    """Create extra unique questions when normal pool is exhausted.
    Avoid fake '[Set X]' suffix duplicates by generating true wording/number variants.
    """
    if subject == 'purechem':
        if force_type == 'mcq':
            mode = random.choice(['products-mcq', 'electrolysis-mcq'])
        elif force_type == 'structured':
            mode = random.choice(['reaction-structured', 'rate-structured'])
        elif force_type == 'short':
            mode = 'mole-short'
        else:
            mode = random.choice(['mole-short', 'reaction-structured', 'products-mcq', 'electrolysis-mcq', 'rate-structured'])
        if mode == 'mole-short':
            vol = random.choice([15.0, 18.0, 22.5, 27.5, 32.0, 35.0, 40.0])
            mol = random.choice([0.10, 0.12, 0.15, 0.18, 0.22, 0.28, 0.30, 0.35, 0.45])
            return q_text('purechem', 'short', f"A technician prepares NaOH at {mol:.2f} mol/dm3. Calculate moles in {vol:.1f} cm3.", 4, points=["convert cm3 to dm3", "moles = concentration × volume"], concept='mole-calculation-variant')
        if mode == 'products-mcq':
            metal = random.choice(['magnesium', 'zinc', 'iron'])
            return q_mcq('purechem', f'Acid + {metal} gives', ['salt + hydrogen', 'salt + water', 'salt + carbon dioxide', 'base only'], 0, points=['salt', 'hydrogen'], concept='reaction-products-variant')
        if mode == 'electrolysis-mcq':
            comp, anode_product = random.choice([
                ('molten lead(II) bromide', 'bromine'),
                ('molten sodium chloride', 'chlorine'),
                ('acidified water', 'oxygen')
            ])
            return q_mcq('purechem', f'In electrolysis of {comp}, {anode_product} forms at the', ['cathode', 'anode', 'electrolyte surface', 'power supply'], 1, points=['anode', 'oxidation'], concept='electrolysis-variant')
        if mode == 'rate-structured':
            solid = random.choice(['CaCO3 chips', 'marble chips', 'zinc granules'])
            acid = random.choice(['HCl', 'H2SO4'])
            return q_text('purechem', 'structured', f'Explain two ways to increase reaction rate for {solid} with dilute {acid}, using collision theory.', 6, points=['surface area', 'temperature or concentration', 'successful collisions'], concept='rate-variant')
        metal, acid, eq = random.choice([
            ('zinc', 'dilute sulfuric acid', 'Zn + H2SO4 -> ZnSO4 + H2'),
            ('magnesium', 'dilute hydrochloric acid', 'Mg + 2HCl -> MgCl2 + H2'),
            ('iron', 'dilute hydrochloric acid', 'Fe + 2HCl -> FeCl2 + H2')
        ])
        return q_text('purechem', 'structured', f'A student reacts {metal} with {acid}. Describe observations and write a balanced symbol equation.', 6, points=['effervescence', 'hydrogen', eq], concept='acid-metal-reaction-variant')

    if subject == 'emath':
        p = random.choice([12, 18, 22, 28, 35])
        final = random.choice([96, 128, 144, 180, 224, 252, 320])
        return q_text('emath', 'short', f"A price after a {p}% discount is ${final}. Find the original price.", 4, points=['percentage', 'reverse percentage'], concept='discount-variant')

    if subject == 'amath':
        a = random.randint(2, 8)
        b = random.randint(5, 16)
        c = random.randint(6, 40)
        return q_text('amath', 'structured', f"Solve x^2 - {b}x + {c} = 0 and verify your roots by substitution.", 6, points=['factorisation or formula', 'roots', 'verification'], concept='quadratic-variant')

    if subject == 'purephys':
        f = random.choice([3, 4, 5, 6, 8, 10, 12])
        v = random.choice([12, 15, 18, 20, 24, 30])
        return q_text('purephys', 'structured', f"A wave travels at {v} m/s with frequency {f} Hz. Calculate wavelength and state one condition that changes wave speed.", 6, points=['wavelength = speed/frequency', 'medium/property'], concept='wave-variant')

    if subject == 'combsci':
        d = random.choice([96, 132, 168, 216, 250])
        t = random.choice([8, 11, 12, 14, 16, 20])
        return q_text('combsci', 'short', f"A moving object covers {d} m in {t} s. Calculate average speed and state the formula used.", 4, points=['speed', 'distance/time'], concept='speed-variant')

    if subject == 'purebio':
        prompt = random.choice([
            'Describe two adaptations of alveoli for efficient gas exchange and explain why each matters.',
            'Explain why enzyme activity increases first with temperature and then drops sharply beyond optimum.',
            'Compare arteries and veins using structure and pressure in one concise paragraph.'
        ])
        return q_text('purebio', 'structured', prompt, 6, points=['structure', 'function', 'explanation'], concept='bio-variant')

    if subject == 'humanities':
        issue = random.choice(['cost of living', 'social mobility', 'urban heat mitigation', 'ageing population'])
        district = random.choice(['Tampines', 'Jurong', 'Woodlands', 'Pasir Ris', 'Ang Mo Kio', 'Punggol'])
        return q_text('humanities', 'structured', f"A town-level pilot in {district} targets {issue}. Assess one policy benefit and one trade-off, then end with a justified judgement.", 6, points=['benefit', 'trade-off', 'judgement'], concept='policy-variant')

    if subject == 'poa':
        rev = random.choice([10200, 11400, 12800, 13600, 14900])
        exp = random.choice([7300, 8100, 9200, 10100, 11300])
        return q_text('poa', 'short', f"Revenue is ${rev} and expenses are ${exp}. Compute net profit and show the formula.", 4, points=['profit = revenue - expenses'], concept='profit-variant')

    # english default: diversify task forms to avoid near-duplicate prompts
    topic = random.choice(['AI drafting tools', 'school attendance policy', 'screen-time limits', 'project-based assessment'])
    audience = random.choice(['parents', 'school leaders', 'students', 'MOE officers', 'a principal', 'a teachers\' committee', 'a school board', 'an education policy panel'])
    mode = random.choice(['argument', 'counter', 'editing', 'evidence', 'rebuttal'])

    if mode == 'counter':
        return q_text('english', 'structured', f"Construct a counter-argument to this claim: '{topic} should be strictly enforced in all schools.' Then refute your own counter in 2 sentences.", 6, points=['counter-argument', 'refutation', 'logic'], concept='counter-variant')
    if mode == 'editing':
        return q_text('english', 'short', f"Rewrite this claim into formal academic tone: '{topic} rules are kinda too much'.", 4, points=['formal tone', 'clarity', 'precision'], concept='editing-variant')
    if mode == 'evidence':
        return q_text('english', 'short', f"Give one measurable indicator schools can track to evaluate whether tighter {topic} policy works.", 4, points=['metric', 'measurable', 'outcome'], concept='evidence-variant')
    if mode == 'rebuttal':
        return q_text('english', 'structured', f"Write a rebuttal paragraph to {audience} against the statement: 'Tightening {topic} always harms student creativity.'", 6, points=['rebuttal', 'evidence', 'balance'], concept='rebuttal-variant')

    return q_text('english', 'structured', f"Write a 6-8 sentence argument to {audience} on whether schools should tighten {topic}. Include one practical safeguard and one measurable outcome.", 6, points=['argument', 'evidence', 'safeguard'], concept='argument-variant')


def gen_paper(subject='integrated', count=20):
    target = int(count)
    out = []
    seen = set()
    seen_semantic = set()
    concept_count = {}
    # Integrated papers should be broad; single-subject papers can repeat, but not dominate one concept.
    max_per_concept = 2 if subject == 'integrated' else 3

    # recent stems from last ~3 papers
    recent = set(RECENT_QUESTIONS.get(subject, []))

    def add(q):
        stem = q['question'].split(' [Set ')[0].strip()
        sig = (q['subject'], q['type'], stem)
        sem = semantic_signature(q)
        concept = q.get('concept', 'general')
        ckey = (q['subject'], concept)

        if sig in seen:
            return False
        # apply semantic dedupe mainly where wording variation can be superficial
        if q.get('subject') in ('english', 'humanities') and sem in seen_semantic:
            return False
        if stem in recent:
            return False
        if concept != 'general' and concept_count.get(ckey, 0) >= max_per_concept:
            return False

        seen.add(sig)
        if q.get('subject') in ('english', 'humanities'):
            seen_semantic.add(sem)
        if concept != 'general':
            concept_count[ckey] = concept_count.get(ckey, 0) + 1
        out.append(q)
        return True

    max_attempts = max(500, target * 70)
    attempts = 0

    if subject == 'integrated':
        for s in SUBJECTS:
            tries = 0
            while tries < 60 and len([x for x in out if x['subject'] == s]) < 2 and attempts < max_attempts:
                add(gen_one(s))
                tries += 1
                attempts += 1
        while len(out) < target and attempts < max_attempts:
            add(gen_one(random.choice(SUBJECTS)))
            attempts += 1
    else:
        while len(out) < target and attempts < max_attempts:
            add(gen_one(subject))
            attempts += 1

    # fallback (only if needed): synthesize true variants, no fake [Set X] suffix clones
    nonce = 1
    fallback_attempts = 0
    while len(out) < target and fallback_attempts < target * 80:
        s = random.choice(SUBJECTS) if subject == 'integrated' else subject
        q = synthesize_variant(s, nonce)
        added = add(q)

        # Escape hatch: if pool constraints are too tight, allow unique synthesized stems
        # without recent/concept checks so we still deliver a full 20-question paper.
        if not added and fallback_attempts > target * 20:
            stem = q['question'].strip()
            sig = (q['subject'], q['type'], stem)
            if sig not in seen:
                seen.add(sig)
                out.append(q)

        nonce += 1
        fallback_attempts += 1

    # Type rebalance for single-subject papers (avoid one-type-heavy sets)
    if subject != 'integrated' and len(out) >= target:
        from collections import Counter
        type_counts = Counter([q['type'] for q in out])
        desired_min = {'mcq': 4, 'short': 4, 'structured': 4}

        def pick_replace_index(prefer_type):
            # replace from most overrepresented type first
            over = sorted(type_counts.items(), key=lambda kv: kv[1], reverse=True)
            for t, _ in over:
                if t != prefer_type and type_counts[t] > desired_min.get(t, 0):
                    for idx, q in enumerate(out):
                        if q['type'] == t:
                            return idx
            return None

        nonce2 = 1000
        for t, min_needed in desired_min.items():
            guard = 0
            while type_counts.get(t, 0) < min_needed and guard < 120:
                idx = pick_replace_index(t)
                if idx is None:
                    break
                q = synthesize_variant(subject, nonce2, force_type=t)
                sig = (q['subject'], q['type'], q['question'].strip())
                existing = {(x['subject'], x['type'], x['question'].strip()) for x in out}
                if sig not in existing:
                    old_t = out[idx]['type']
                    out[idx] = q
                    type_counts[old_t] -= 1
                    type_counts[t] += 1
                nonce2 += 1
                guard += 1

    random.shuffle(out)
    out = out[:target]

    # Persist recent stems across last 3 papers
    stems = [x['question'].split(' [Set ')[0].strip() for x in out]
    papers = RECENT_PAPERS.get(subject, [])
    papers = [stems] + papers[:2]
    RECENT_PAPERS[subject] = papers
    RECENT_QUESTIONS[subject] = [s for paper in papers for s in paper]

    return out


def norm(s):
    return (s or '').lower().strip()


def send_claim_to_telegram(text):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return {"sent": False, "reason": "telegram_not_configured"}
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        payload = parse.urlencode({
            "chat_id": TG_CHAT_ID,
            "text": text,
            "disable_web_page_preview": "true"
        }).encode()
        req = request.Request(url, data=payload)
        with request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        return {"sent": bool(data.get('ok')), "reason": "ok" if data.get('ok') else "telegram_api_error"}
    except Exception as e:
        return {"sent": False, "reason": f"send_failed:{e}"}


def mark(paper, answers):
    total = 0
    got = 0
    detail = []
    for i, q in enumerate(paper):
        total += q.get('marks', 0)
        a = answers.get(str(i), '')
        if q['type'] == 'mcq':
            ok = str(a) == str(q.get('answer'))
            sc = q['marks'] if ok else 0
            got += sc
            idx = int(q.get('answer', 0))
            correct = (q.get('choices') or [''])[idx] if q.get('choices') else ''
            picked = ''
            if str(a).isdigit() and q.get('choices') and int(a) < len(q['choices']):
                picked = q['choices'][int(a)]
            detail.append({
                "q": i + 1,
                "score": sc,
                "max": q['marks'],
                "feedback": "Correct" if ok else "Incorrect",
                "reason": ("Matches answer key." if ok else "Does not match answer key.") + (f" You chose: {picked}." if picked else ""),
                "correctAnswer": correct
            })
        else:
            txt = norm(a)
            keys = [norm(k) for k in q.get('keywords', [])]
            hits = [k for k in keys if k and k in txt]
            miss = [k for k in keys if k and k not in txt]
            ratio = len(hits) / max(1, len(keys))
            sc = max(0, min(q['marks'], round((ratio + (0.15 if len(txt) > 120 else 0)) * q['marks'])))
            got += sc
            reason = f"Matched {len(hits)}/{len(keys)} key points"
            if miss:
                reason += f". Missing: {', '.join(miss[:4])}"
            detail.append({
                "q": i + 1,
                "score": sc,
                "max": q['marks'],
                "feedback": f"Matched {len(hits)}/{len(keys)} key points",
                "reason": reason,
                "correctAnswer": "Key points: " + ", ".join(keys[:5]) if keys else "Model answer not available"
            })

    return {"score": got, "total": total, "percent": round(100 * got / max(1, total)), "details": detail}


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST,GET,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/health':
            return self._send(200, {"ok": True})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        n = int(self.headers.get('Content-Length', '0'))
        body = json.loads(self.rfile.read(n) or b'{}') if n else {}

        if path in ('/api/generate-paper', '/generate-paper'):
            subject = body.get('subject', 'integrated')
            count = int(body.get('count', 20))
            paper = gen_paper(subject, count)
            sig = '|'.join([f"{x.get('subject')}::{x.get('type')}::{x.get('question')}" for x in paper])
            tries = 0
            while LAST_SIGNATURE.get(subject) == sig and tries < 6:
                paper = gen_paper(subject, count)
                sig = '|'.join([f"{x.get('subject')}::{x.get('type')}::{x.get('question')}" for x in paper])
                tries += 1
            LAST_SIGNATURE[subject] = sig
            return self._send(200, {"paper": paper, "paperId": str(uuid.uuid4()), "engine": "dynamic-generator"})

        if path in ('/api/mark-paper', '/mark-paper'):
            paper = body.get('paper', [])
            answers = body.get('answers', {})
            return self._send(200, {"result": mark(paper, answers), "engine": "realtime-rubric"})

        if path in ('/api/claim', '/claim'):
            handle = (body.get('handle') or '').strip()
            subject = (body.get('subject') or 'Unknown subject').strip()
            paper_id = (body.get('paperId') or '').strip()
            pct = body.get('percent')
            if not handle.startswith('@'):
                return self._send(400, {"ok": False, "error": "invalid_handle"})

            msg = f"🏆 Gift claim submission\nHandle: {handle}\nSubject: {subject}\nScore: {pct}%\nPaper: {paper_id or 'N/A'}\nStatus: Pending manual processing (gift not yet given)."
            sent = send_claim_to_telegram(msg)
            return self._send(200, {"ok": True, "forwarded": sent.get('sent', False), "status": "pending_manual_processing"})

        return self._send(404, {"error": "not found"})


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', 8788), H).serve_forever()
