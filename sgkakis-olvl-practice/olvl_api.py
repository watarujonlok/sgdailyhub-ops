#!/usr/bin/env python3
import json, random, uuid
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

SUBJECTS = ["english","emath","amath","combsci","purechem","purephys","purebio","humanities","poa"]

BANK = {
  "english": [
    ("mcq",2,"Choose the sentence with the most formal academic tone.",["I kinda disagree with this view.","This perspective warrants closer scrutiny due to unequal outcomes.","This is obviously wrong.","People always say this."],1,["formal tone"]),
    ("short",4,"State one assumption in: 'Tuition is necessary for success.'",None,None,["tuition","necessary","school support","success"]),
    ("structured",6,"In 5-7 sentences, evaluate if device-free school policies improve outcomes in Singapore. Give one support and one limitation.",None,None,["focus","sleep","equity","enforcement","limitation"])
  ],
  "emath": [
    ("mcq",2,"Solve: 5(2x-3)=3(x+4)+7",["x=2","x=3","x=4","x=5"],1,["3"]),
    ("short",4,"A bag costs $168 after a 30% discount. Find the original price.",None,None,["240"]),
    ("structured",6,"Line passes through (-2,3) and (4,15). Find gradient and equation in y=mx+c with full working.",None,None,["2","y=2x+7","m=2"])
  ],
  "amath": [
    ("mcq",2,"Differentiate y=4x^3-6x^2+2",["12x^2-12x","4x^2-12x","12x-12","12x^2-6x"],0,["12x^2-12x"]),
    ("short",4,"Solve 3^x = 81",None,None,["4"]),
    ("structured",6,"Solve x^2-9x+20=0 and explain how factorisation verifies both roots.",None,None,["4","5","(x-4)(x-5)"])
  ],
  "combsci": [
    ("mcq",2,"Higher concentration increases rate mainly because...",["lower activation energy always","more frequent successful collisions","fewer collisions","temperature drops"],1,["collisions"]),
    ("short",4,"A runner travels 180m in 15s. Find speed.",None,None,["12"]),
    ("structured",6,"Explain why powdered zinc reacts faster than zinc granules with same HCl. Include one controlled variable.",None,None,["surface area","collision","temperature","concentration"])
  ],
  "purechem": [
    ("mcq",2,"Acid + carbonate produces",["salt+water","salt+water+CO2","salt+H2","salt only"],1,["co2"]),
    ("short",4,"Find moles in 25.0 cm3 of 0.40 mol/dm3 NaOH.",None,None,["0.01"]),
    ("structured",6,"Describe observations and equation when calcium carbonate reacts with hydrochloric acid.",None,None,["effervescence","co2","cacl2","h2o"])
  ],
  "purephys": [
    ("mcq",2,"If velocity is constant, resultant force is",["positive","negative","zero","maximum"],2,["zero"]),
    ("short",4,"Calculate force when m=1200kg, a=1.5m/s^2",None,None,["1800"]),
    ("structured",6,"A wave has frequency 8Hz. Find period and explain one factor affecting wave speed.",None,None,["0.125","medium","temperature","density"])
  ],
  "purebio": [
    ("mcq",2,"Osmosis is movement of",["any molecules","water through partially permeable membrane","ions from low to high","oxygen into blood"],1,["water"]),
    ("short",4,"State two differences between arteries and veins.",None,None,["thick wall","pressure","valves","lumen"]),
    ("structured",6,"Explain effect of pH on enzyme activity including denaturation.",None,None,["optimum","active site","denature","rate"])
  ],
  "humanities": [
    ("mcq",2,"Best SBQ reliability method is",["quote length","cross-reference + provenance","author age","emotive words only"],1,["provenance"]),
    ("short",4,"State one impact of globalisation on local employment.",None,None,["skills","competition","wages","outsourcing"]),
    ("structured",6,"'Meritocracy is fully fair in practice.' Evaluate with one support and one challenge.",None,None,["opportunity","mobility","inequality","advantage"])
  ],
  "poa": [
    ("mcq",2,"Accounting equation",["Assets=Liabilities+Capital","Capital=Assets+Liabilities","Profit=Assets-Liabilities","Cash=Revenue-Expenses"],0,["assets"]),
    ("short",4,"If revenue=9500 and expenses=6200, find profit.",None,None,["3300"]),
    ("structured",6,"Explain why trial balance may still balance despite errors. Give two examples.",None,None,["compensating","omission","principle","commission"])
  ]
}


def gen_paper(subject='integrated', count=20):
    # Build a unique pool first (no duplicate question text within same paper)
    if subject == 'integrated':
      pool = []
      for s in SUBJECTS:
        for p in BANK[s]:
          pool.append(to_q(s, p))
    else:
      pool = [to_q(subject, p) for p in BANK.get(subject, BANK['english'])]

    # Deduplicate by (subject, question, type)
    seen = set()
    uniq = []
    for q in pool:
      sig = (q['subject'], q['question'], q['type'])
      if sig in seen:
        continue
      seen.add(sig)
      uniq.append(q)

    if not uniq:
      return []

    # If request > unique pool size, cap at pool size (avoid repeats in one paper)
    n = min(int(count), len(uniq))
    paper = random.sample(uniq, n)
    random.shuffle(paper)
    return paper


def to_q(subject, tpl):
  qtype, marks, q, choices, ans, keywords = tpl
  base = {"subject": subject, "type": qtype, "marks": marks, "question": q, "keywords": keywords}
  if qtype == 'mcq':
    base.update({"choices": choices, "answer": ans})
  return base


def norm(s):
  return (s or '').lower().strip()


def mark(paper, answers):
  total = 0
  got = 0
  detail = []
  for i,q in enumerate(paper):
    total += q.get('marks',0)
    a = answers.get(str(i), '')
    if q['type']=='mcq':
      ok = str(a)==str(q.get('answer'))
      sc = q['marks'] if ok else 0
      got += sc
      detail.append({"q":i+1,"score":sc,"max":q['marks'],"feedback":"Correct" if ok else "Incorrect"})
    else:
      txt = norm(a)
      keys = [norm(k) for k in q.get('keywords',[])]
      hits = sum(1 for k in keys if k and k in txt)
      ratio = hits / max(1, len(keys))
      sc = max(0, min(q['marks'], round((ratio + (0.15 if len(txt)>120 else 0))*q['marks'])))
      got += sc
      detail.append({"q":i+1,"score":sc,"max":q['marks'],"feedback":f"Matched {hits}/{len(keys)} key points"})
  return {"score": got, "total": total, "percent": round(100*got/max(1,total)), "details": detail}

class H(BaseHTTPRequestHandler):
  def _send(self, code, obj):
    b = json.dumps(obj).encode()
    self.send_response(code)
    self.send_header('Content-Type','application/json')
    self.send_header('Content-Length', str(len(b)))
    self.send_header('Access-Control-Allow-Origin','*')
    self.end_headers()
    self.wfile.write(b)

  def do_OPTIONS(self):
    self.send_response(204)
    self.send_header('Access-Control-Allow-Origin','*')
    self.send_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
    self.send_header('Access-Control-Allow-Headers','Content-Type')
    self.end_headers()

  def do_GET(self):
    path = urlparse(self.path).path
    if path == '/health':
      return self._send(200, {"ok": True})
    self._send(404, {"error":"not found"})

  def do_POST(self):
    path = urlparse(self.path).path
    n = int(self.headers.get('Content-Length','0'))
    body = json.loads(self.rfile.read(n) or b'{}') if n else {}
    if path in ('/api/generate-paper','/generate-paper'):
      subject = body.get('subject','integrated')
      count = int(body.get('count',20))
      paper = gen_paper(subject, count)
      return self._send(200, {"paper": paper, "paperId": str(uuid.uuid4()), "engine":"realtime-generator"})
    if path in ('/api/mark-paper','/mark-paper'):
      paper = body.get('paper',[])
      answers = body.get('answers',{})
      return self._send(200, {"result": mark(paper, answers), "engine":"realtime-rubric"})
    return self._send(404, {"error":"not found"})

if __name__ == '__main__':
  HTTPServer(('0.0.0.0', 8788), H).serve_forever()
