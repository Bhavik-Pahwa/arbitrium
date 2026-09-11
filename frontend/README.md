# Arbitrium Frontend

React + TypeScript + Tailwind prototype for Arbitrium.

```bash
npm install
npm run dev
```

Open `http://127.0.0.1:5173/`.

By default the app runs in quiet demo mode so it works without the FastAPI backend. To call the backend, start the API on `http://localhost:8000` and run:

```powershell
$env:VITE_API_ENABLED="true"
$env:VITE_API_BASE_URL="http://localhost:8000"
npm run dev
```
