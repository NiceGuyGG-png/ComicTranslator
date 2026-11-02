// Background service worker – xử lý message giữa content script và backend

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "TRANSLATE_PANEL") {
    // TODO: gọi backend API
    console.log("[ComicTranslator] Nhận request translate panel", message);
    sendResponse({ status: "received", message: "Backend call chưa implement" });
  }
  return true; // keep channel open for async
});

console.log("[ComicTranslator] Background service worker loaded");