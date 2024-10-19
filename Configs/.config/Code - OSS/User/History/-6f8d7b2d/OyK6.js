chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
      return { redirectUrl: "http://localhost:5000" };
    },
    { urls: ["*://discipline4.everyone/*"] },
    ["blocking"]
  );
  