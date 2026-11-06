# Auto Tag Generator API

FastAPI service for the CNN tag model. Deploy this folder on [Render](https://render.com) as a Web Service.

`/api/predict` accepts a browser call only when the `Origin` header is in `ALLOWED_ORIGINS`. Every other origin receives `403`. CORS headers are issued for that same list, so a page on an unlisted host cannot read the response.

## Render

1. New **Web Service**, connect this repository.
2. **Root Directory:** `backend`
3. **Runtime:** Python 3.12 (`runtime.txt` pins 3.12.7)
4. **Build command:** `pip install -r requirements.txt`
5. **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`  
   Render also reads the `Procfile` in this folder.
6. **Environment variable**

   ```text
   ALLOWED_ORIGINS=https://your-app.vercel.app
   ```

   Separate extra origins with commas. Do not add a trailing slash. If this variable is missing, only local Vite origins are allowed.

7. Use an instance with **at least 2 GB RAM**. TensorFlow does not stay up on a 512 MB instance.

Health check path: `/health`

## Local

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --port 8000
```

```bash
curl -X POST http://localhost:8000/api/predict ^
  -H "Origin: http://localhost:5173" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"How do I forecast monthly sales with ARIMA in R?\"}"
```

A request without a listed `Origin` is rejected, including plain `curl` with no origin header.
