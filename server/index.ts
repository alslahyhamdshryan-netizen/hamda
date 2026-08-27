import express from "express";
import { createServer } from "http";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const server = createServer(app);
  const djangoUrl = process.env.DJANGO_API_URL || "http://127.0.0.1:8000";

  // Keep the browser on one origin while Django owns authentication and data.
  app.use("/api", express.raw({ type: "application/json" }));
  app.all("/api/*", async (req, res) => {
    try {
      const upstream = await fetch(`${djangoUrl}${req.originalUrl}`, {
        method: req.method,
        headers: {
          "content-type": req.headers["content-type"] || "application/json",
          ...(req.headers.cookie ? { cookie: req.headers.cookie } : {}),
          ...(req.headers["x-csrftoken"] ? { "x-csrftoken": req.headers["x-csrftoken"] as string } : {}),
        },
        body: req.method === "GET" || req.method === "HEAD" ? undefined : req.body,
      });
      const setCookie = upstream.headers.get("set-cookie");
      if (setCookie) res.setHeader("set-cookie", setCookie);
      res.status(upstream.status).set("content-type", upstream.headers.get("content-type") || "application/json").send(Buffer.from(await upstream.arrayBuffer()));
    } catch (error) {
      console.error("Django API proxy error", error);
      res.status(502).json({ error: "تعذر الاتصال بخادم Django" });
    }
  });

  // Serve static files from dist/public in production
  const staticPath =
    process.env.NODE_ENV === "production"
      ? path.resolve(__dirname, "public")
      : path.resolve(__dirname, "..", "dist", "public");

  app.use(express.static(staticPath));

  // Handle client-side routing - serve index.html for all routes
  app.get("*", (_req, res) => {
    res.sendFile(path.join(staticPath, "index.html"));
  });

  const port = process.env.PORT || 3000;

  server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}/`);
  });
}

startServer().catch(console.error);
