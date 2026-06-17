function getParam(name, fallback = "") {
  const params = new URLSearchParams(window.location.search);
  return params.get(name) || fallback;
}

function withFallback(preferred, aliases, fallback = "-") {
  if (preferred) return preferred;
  for (const alias of aliases) {
    const value = getParam(alias);
    if (value) return value;
  }
  return fallback;
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

const end = withFallback(getParam("end"), ["endDate"]);
const total = withFallback(getParam("total"), ["totalRewards"]);
const participants = withFallback(getParam("participants"), ["totalParticipants"]);
const my = withFallback(getParam("my"), ["myRewards"]);

setText("[data-value='end']", end);
setText("[data-value='total']", total);
setText("[data-value='participants']", participants);
setText("[data-value='my']", my);
