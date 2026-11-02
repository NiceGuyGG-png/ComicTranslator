// Helper gọi Backend API

const DEFAULT_BASE_URL = "http://localhost:8000";

export async function translatePanel(imageBlob, options = {}) {
  const form = new FormData();
  form.append("image", imageBlob, "panel.png");
  form.append("source_lang", options.sourceLang || "zh");
  form.append("target_lang", options.targetLang || "vi");

  const res = await fetch(`${DEFAULT_BASE_URL}/api/v1/translate/panel`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}