// Content script – chạy trên trang truyện

console.log("[ComicTranslator] Content script injected");

// Placeholder: sau này sẽ detect panel / bubble text
function captureSelectedRegion() {
  // TODO: implement region selection + capture
  return null;
}

// Lắng nghe message từ popup / background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "START_CAPTURE") {
    console.log("[ComicTranslator] Start capture mode");
    sendResponse({ ok: true });
  }
});