document.getElementById("btn-capture").addEventListener("click", async () => {
  const status = document.getElementById("status");
  status.textContent = "Đang kích hoạt chế độ chọn vùng...";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab?.id) {
    chrome.tabs.sendMessage(tab.id, { type: "START_CAPTURE" }, (res) => {
      status.textContent = res?.ok ? "Chế độ chọn vùng đã bật" : "Lỗi gửi message";
    });
  }
});

document.getElementById("btn-auto").addEventListener("click", () => {
  document.getElementById("status").textContent = "Tính năng auto sẽ implement sau";
});