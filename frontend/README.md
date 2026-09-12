# Arbitrium Frontend

React + TypeScript + Vite frontend for Arbitrium.

## Setup

```powershell
npm install
```

## Run

```powershell
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173/
```

The frontend calls the backend at `http://localhost:8000` by default.

To use a different backend URL:

```powershell
$env:VITE_API_BASE_URL="http://127.0.0.1:8000"
npm run dev -- --host 127.0.0.1 --port 5173
```

## Build

```powershell
npm run build
```
