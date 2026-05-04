(function () {
  if (window.top !== window.self) {
    return;
  }

  const canRegisterServiceWorker = (
    "serviceWorker" in navigator &&
    (window.location.protocol === "https:" ||
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1")
  );

  if (!canRegisterServiceWorker) {
    return;
  }

  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/service-worker.js", { scope: "/" })
      .catch(function (err) {
        console.warn("Lute service worker registration failed", err);
      });
  });
}());
