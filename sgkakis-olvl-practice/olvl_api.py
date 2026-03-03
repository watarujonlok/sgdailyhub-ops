#!/usr/bin/env python3
import json, random, uuid
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SUBJECTS = ["english","emath","amath","combsci","purechem","purephys","purebio","humanities","poa"]
LAST_SIGNATURE = {}
RECENT_QUESTIONS = {}  # subject -> recent question stems across papers


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
              ["This is bad.", "This issue deserves balanced policy reform with measurable outcomes.", "I don’t like this.", "Everyone says this matters."], 1, points=["thesis", "academic tone"]),
        q_text("english", "short", f"State one assumption in this claim: '{topic.title()} should be reduced in schools.'", 4,
               points=["assumption", "evidence", "context"]),
        q_text("english", "structured", f"In 5-7 sentences, evaluate one benefit and one limitation of policies on {topic} in Singapore.", 6,
               points=["benefit", "limitation", "evidence", "evaluation"])])


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
              points=["cross-reference", "provenance"]),
        q_text("humanities", "short", f"State one impact of {issue} on Singapore society/economy.", 4,
               points=["impact", "example", "Singapore context"]),
        q_text("humanities", "structured", f"Evaluate the statement: '{issue.title()} policy outcomes are fully fair.' Give one support and one challenge.", 6,
               points=["support", "challenge", "evidence", "evaluation"])])


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


def gen_paper(subject='integrated', count=20):
    target = int(count)
    out = []
    seen = set()
    concept_count = {}
    max_per_concept = 2 if subject == 'integrated' else 1
    recent = set(RECENT_QUESTIONS.get(subject, []))

    def add(q):
        stem = q['question'].split(' [Set ')[0].strip()
        sig = (q['subject'], q['type'], stem)
        concept = q.get('concept', 'general')
        ckey = (q['subject'], concept)

        if sig in seen:
            return False
        if stem in recent:
            return False
        if concept != 'general' and concept_count.get(ckey, 0) >= max_per_concept:
            return False

        seen.add(sig)
        if concept != 'general':
            concept_count[ckey] = concept_count.get(ckey, 0) + 1
        out.append(q)
        return True

    # bounded generation loops to avoid hangs
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

    # fallback ensures completion while preserving non-identical display
    nonce = 1
    while len(out) < target:
        s = random.choice(SUBJECTS) if subject == 'integrated' else subject
        q = gen_one(s)
        q['question'] = f"{q['question']} [Set {nonce}]"
        # fallback bypasses recent/concept locks but still avoids exact duplicates
        stem = q['question'].split(' [Set ')[0].strip()
        sig = (q['subject'], q['type'], stem, nonce)
        if sig not in seen:
            seen.add(sig)
            out.append(q)
        nonce += 1

    random.shuffle(out)

    # save recent stems (rolling window)
    stems = [x['question'].split(' [Set ')[0].strip() for x in out]
    prev = RECENT_QUESTIONS.get(subject, [])
    RECENT_QUESTIONS[subject] = (stems + prev)[:120]

    return out[:target]


def norm(s):
    return (s or '').lower().strip()


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

        return self._send(404, {"error": "not found"})


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', 8788), H).serve_forever()
