<div align="center">
  <a href="[YOUTUBE_URL]">
    <img src="https://img.youtube.com/vi/[YOUTUBE_ID]/0.jpg" alt="[YOUTUBE_TITLE]">
  </a>
  <h3>📺 <a href="[YOUTUBE_URL]">Watch the full tutorial on YouTube</a></h3>
</div>

# 🧠 Intern Decision Structured AI Agent

> High-speed multimodal structured decision engine fine-tuned from Qwen3.5, scoring complex decision schemas in a single forward pass with zero text generation overhead.

| Step 1: Input | Step 2: AI Action | Step 3: Result |
|---|---|---|
| Multimodal input document (images) & schema questions in `inputs/triage_batch.json` | Masked single-token forward pass across candidate logits | Calibrated JSON probability distribution & instant decision routing |

## ⚡ Features

- 🎯 **Single-Pass Prediction**: Scores all schema questions in one causal forward pass without free-form text generation.
- ⚡ **Ultra-Low Latency**: End-to-end inference in 33ms–44ms on GPU, up to 3x faster than standard generation.
- 📐 **Calibrated Confidence**: Pre-tuned temperature calibration delivers accurate probability distributions and Brier scores.
- 🖼️ **GGUF On-Device Support**: Evaluates structured multimodal schema inputs using local GGUF quantizations (`models/intern-decision-0.8b-fp16.gguf`).

## 📥 Model Download

Download the official GGUF checkpoint into the `models/` directory:

```powershell
mkdir -Force models
Invoke-WebRequest -Uri "https://huggingface.co/bombdefuser-124/Intern-Decision-0.8B-GGUF/resolve/main/intern-decision-0.8b-fp16.gguf?download=true" -OutFile "models/intern-decision-0.8b-fp16.gguf"
```

## 🚀 Quick Start (Multimodal Document Triage)

1. **Prepare Inputs**: Mixed invoices, receipts, tax forms, and screenshots are defined in `inputs/triage_batch.json`.
2. **Run Inference**: Execute the single-pass document triage pipeline.

```powershell
python main.py
```
*(Alternatively, run the visualizer version `python assets/test_main.py`)*

3. **View Dashboard**: Check `outputs/outputs.md` to see the generated probability bars, final routing decisions, and the aggregate dashboard showing how many documents were automatically processed.

## 📂 Project Structure

```text
├── assets/
│   ├── intern-decision_overview.html
│   ├── intern-decision_overview.md
│   └── test_main.py
├── inputs/
│   └── triage_batch.json
├── models/
│   └── intern-decision-0.8b-fp16.gguf
├── outputs/
│   └── outputs.md
├── main.py
└── README.md
```

## 💡 Real-World Use Cases

1. **Multimodal Document-Triage**: Instantly classifies document type, urgency, needs-OCR, suspicious flags, and team routing in one pass.
2. **PC Automation & Computer Use**: Selects exact UI click/key actions from screen screenshots without chat parsing delays.
3. **Customer Support Routing**: Instantly classifies ticket category, urgency score, and refund intent in one single query.
4. **Autonomous Agent Guardrails**: Evaluates safety, policy, and tool selection choices with calibrated confidence levels.
5. **Real-Time Game State Decision**: Picks tactical moves and strategy scores directly from video game screen state.

---
**Keywords**: Multimodal AI, Intern-Decision, Qwen3.5, Document Triage, Structured Decision Engine, Logit Scoring, Local LLM, GGUF, Ollama, Machine Learning, Computer Vision
