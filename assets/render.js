function getParam(name, fallback = "") {
  return new URLSearchParams(window.location.search).get(name) || fallback;
}

function withFallback(preferred, aliases, fallback) {
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

function updateTotalInCopy(total) {
  if (!total) return;

  const title = document.querySelector(".boost-project-card h2");
  if (title) {
    title.textContent = title.textContent.replace(
      /(Earn your share of )[\d,]+/,
      `$1${total}`
    );
  }

  const description = document.querySelector(".boost-project-card p");
  if (description) {
    description.innerHTML = description.innerHTML.replace(
      /(market value of )[\d,]+/,
      `$1${total}`
    );
  }
}

const end = withFallback(getParam("end"), ["endDate"], null);
const total = withFallback(getParam("total"), ["totalRewards"], null);
const participants = withFallback(getParam("participants"), ["totalParticipants"], null);
const my = withFallback(getParam("my"), ["myRewards"], null);
const duration = withFallback(getParam("duration"), ["durationDays"], null);
const asof = withFallback(getParam("asof"), ["asOf"], null);

if (end) setText("[data-value='end']", end);
if (total) {
  setText("[data-value='total']", total);
  updateTotalInCopy(total);
}
if (participants) setText("[data-value='participants']", participants);
if (my) setText("[data-value='my']", my);
if (duration) setText("[data-value='duration']", duration);
if (asof) setText("[data-value='asof']", asof);
