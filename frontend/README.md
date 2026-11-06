# Auto Tag Generator

Vite + React page for the tagging API. Deploy this folder on [Vercel](https://vercel.com).

The page calls `VITE_API_URL/api/predict` from the browser. That URL is read when the site is built, so set it in Vercel before the first production build. Changing it later needs a redeploy.

## Vercel

1. Import this repository.
2. **Root Directory:** `frontend`
3. Framework preset: **Vite**
4. Build command: `npm run build`
5. Output directory: `dist`
6. Environment variable

   ```text
   VITE_API_URL=https://your-service.onrender.com
   ```

   No trailing slash.

7. After the first deploy, copy the Vercel URL (for example `https://your-app.vercel.app`) into the backend `ALLOWED_ORIGINS` variable on Render, then redeploy the API if it is already live.

Preview deployments use a different host each time. Add each preview origin to `ALLOWED_ORIGINS`, or the API will answer `403`.

## Local

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

The dev server runs at `http://localhost:5173`, which the API allows when `ALLOWED_ORIGINS` is unset.
