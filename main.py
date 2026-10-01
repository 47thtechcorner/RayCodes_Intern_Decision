"""
Intern-Decision Multimodal Document Triage Engine
"""
import json, os, time, base64, requests

class Engine:
    def __init__(self):
        print("[Init] Multimodal Engine Targeting Local Ollama")

    def _bar(self, p):
        f = int(round(p * 15))
        return "█" * f + "░" * (15 - f)

    def eval(self, path, schema):
        t0 = time.time()
        name = os.path.basename(path)
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        
        sys_msg = "Output JSON ONLY. For each key, give 'decision' and 'probabilities' mapping."
        try:
            resp = requests.post("http://localhost:11434/api/generate", json={
                "model": "intern-decision", "system": sys_msg, 
                "prompt": json.dumps({"schema": schema}), "images": [b64], 
                "stream": False, "format": "json"
            }, timeout=30)
            out = json.loads(resp.json().get("response", "{}"))
        except:
            out = {}

        ans = {}
        for k, opts in schema.items():
            q = out.get(k, {})
            ans[k] = {
                "decision": q.get("decision", "unknown"),
                "probs": q.get("probabilities", {o: 1.0/len(opts) for o in opts} if opts else {"unknown": 1.0})
            }
            
        return {"id": name.split('.')[0].upper(), "name": name, "ms": round((time.time()-t0)*1000, 2), "ans": ans}

def main():
    print("="*60, "\n Intern-Decision Multimodal Triage\n" + "="*60)
    
    # 🎯 Drastically simplified schema: Just questions and allowed options
    schema = {
        "doc_type": ["invoice", "receipt", "tax_form", "ui_screenshot"],
        "urgency": ["Low", "Standard", "Urgent"],
        "needs_ocr": ["yes", "no"],
        "suspicious_flag": ["yes", "no"],
        "route_to_team": ["accounts_payable", "hr_payroll", "tier2_support", "fraud_prevention"]
    }

    files = [f for f in os.listdir("inputs") if f.lower().endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists("inputs") else []
    if not files: return print("No images in 'inputs/'.")
    
    eng, res = Engine(), []
    for f in files:
        r = eng.eval(f"inputs/{f}", schema)
        res.append(r)
        print(f"  > Processed {r['id']} in {r['ms']}ms | Route: {r['ans']['route_to_team']['decision']}")

    auto = sum(1 for r in res if r["ans"]["suspicious_flag"]["decision"] == "no")
    
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/outputs.md", "w", encoding="utf-8") as f:
        f.write(f"# 📑 Triage Dashboard\n\n| Processed | Auto-Routed | Flagged | Avg Latency |\n|---|---|---|---|\n")
        f.write(f"| {len(res)} | {auto} | {len(res)-auto} | {sum(r['ms'] for r in res)/len(res):.1f}ms |\n\n")
        
        for r in res:
            ans = r["ans"]
            f.write(f"### 📂 {r['id']} — `{r['name']}`\n")
            f.write(f"- Route: `{ans['route_to_team']['decision'].upper()}` | Type: `{ans['doc_type']['decision']}` | OCR: `{ans['needs_ocr']['decision'].upper()}`\n\n")
            f.write("```text\n[Doc Type Probabilities]\n")
            for k, p in ans["doc_type"]["probs"].items(): f.write(f"  {k:<16} [{eng._bar(p)}] {p*100:5.1f}%\n")
            f.write("\n[Route Target Probabilities]\n")
            for k, p in ans["route_to_team"]["probs"].items(): f.write(f"  {k:<16} [{eng._bar(p)}] {p*100:5.1f}%\n")
            f.write("```\n---\n")
            
    print(f"\n[Success] Dashboard output successfully written to outputs/outputs.md")

if __name__ == "__main__":
    main()
