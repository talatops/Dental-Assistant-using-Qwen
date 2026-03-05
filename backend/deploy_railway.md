## Deploying the Backend to Railway

This document describes how to deploy the FastAPI backend (with local Qwen model) to Railway.

### 1. Prerequisites
- Railway account.
- GitHub repository containing this project.
- A CPU-friendly, quantized Qwen model available in `models/qwen/` or mounted via Railway persistent storage.

### 2. Create a New Railway Project
1. Push your code to GitHub.
2. In Railway, create a new project and select **Deploy from GitHub repo**.
3. Choose this repository and the `main` branch.

### 3. Configure the Service
- Railway should detect the `backend/Dockerfile` automatically. If not:
  - Set the service to use a Dockerfile.
  - Specify the Dockerfile path as `backend/Dockerfile`.
- Set the exposed port to `8000` (matches `BACKEND_PORT` in the Dockerfile).

### 4. Environment Variables
Set any environment variables you need (for example, if you want to override the WebSocket URL or model paths). For a simple deployment, the defaults in `backend/config.py` are sufficient, as long as the model files exist at the expected locations in the container.

### 5. Build and Deploy
1. Trigger a deployment in Railway.
2. Wait for the image to build and the service to start.
3. Once running, note the public URL of your service, for example:
   - `https://your-railway-app.up.railway.app`
4. The WebSocket endpoint will be:
   - `wss://your-railway-app.up.railway.app/ws/chat`

### 6. Connect the Frontend
- In the Vercel frontend, set the `VITE_BACKEND_WS_URL` environment variable (or update `frontend/vercel.json`) to point to the Railway WebSocket URL, for example:
  - `wss://your-railway-app.up.railway.app/ws/chat`

This setup keeps all LLM inference inside your Railway container and does not use any external LLM APIs, satisfying the fully-local inference requirement of the assignment.

