 
# 🎥 Video Management System (VMS) with AI Integration

This is a lightweight, scalable Video Management System that:

- Handles 10+ simultaneous video streams
- Integrates AI models for real-time or batch inference
- Includes a React-based dashboard for stream monitoring
- Supports object detection and classification (e.g., defects, missing parts)

---

## 📁 Project Structure

```
vms-ai-system/
├── backend/
│   ├── main.py
│   ├── streams/
│   │   └── stream_handler.py
│   ├── ai_models/
│   │   └── yolo_model.py (or dummy model)
│   └── outputs/
├──inputs/
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── Dashboard.jsx
│   ├── index.html
│   └── package.json
└── README.md
```

---

## 🚀 Features

- 🔟 **Multi-stream support** — Handle 10+ video inputs in parallel
- 🧠 **AI integration** — Object detection + classification per frame
- 📊 **Dashboard** — Live stream status, model results, and alerts
- 📁 **Output management** — Save results and frames locally
- 🌐 **FastAPI** backend + React frontend

---

## 🛠️ Setup Instructions

### 1. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend Setup (React + Vite)

```bash
cd ../frontend
npm install
npm run dev
```

---

## 🔍 API Endpoints

| Method | Route            | Description                  |
|--------|------------------|------------------------------|
| GET    | `/ping`          | Test API status              |
| POST   | `/start-streams` | Start all video streams      |     |
| GET    | `/get-results`   | Get AI predictions per frame |
| GET    | `/static/...`    | Serve latest frame images    |

---

## 🧪 Sample Test Flow

1. 🎬 Add at least 10 video files to `backend/inputs/sample_videos/video1.mp4` to `video10.mp4`
2. ▶️ Start backend server: `uvicorn main:app --reload`
3. ▶️ Start frontend: `npm run dev`
4. 📈 Go to `http://localhost:5173` (React UI)
5. ✅ Click **"Start Streams"** or refresh page
6. 🎯 View detections and alerts in real time

---

## 🖥️ Dashboard Preview

- Shows **Active Streams**
- Lists **Latest Frames**
- Displays **Detections**
- Highlights **Defective Items** like `MISSING_HEAD`, `RUSTY`, `DEFECT`
- Optionally shows detected object name like `toothbrush`, `bolt`

---

## 🧠 AI Pipeline (Simplified)

1. Load frame every 30th frame
2. Run object detection (YOLO/dummy)
3. Run classification on each detection
4. Save:
   - Annotated frame
   - JSON result
5. Serve via API to frontend

---

## 💾 Output Management

- All frames and results stored in `/backend/outputs/stream_<id>/`
- Results available via API: `/get-results`
- Can be extended to support file uploads, S3, etc.

---

## 📸 Sample Output

```json
{
  "frame": 510,
  "results": [
    {
      "detection": {
        "label": "toothbrush",
        "confidence": 0.79,
        "box": [197.76, 159.43, 289.74, 439.48]
      },
      "classification": {
        "class": "DEFECT",
        "confidence": 0.86
      }
    }
  ]
}
```

---

## 📌 Tech Stack

- **Backend:** FastAPI, OpenCV, Python
- **Frontend:** React.js, Axios, CSS Grid
- **AI:** Dummy/Yolo detection + classification module
- **Server:** Uvicorn (ASGI)

---

## 📎 To-Dos (Optional Enhancements)

- [ ] Replace dummy inference with real AI model
- [ ] Add websocket/live updates
- [ ] Add charts for defect trends
- [ ] Add user login and API key access

---

## 👨‍💻 Author

> Built by Mayank Chauhan as part of an internship assignment.

---


