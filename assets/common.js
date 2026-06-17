function setupGetButton() {
  const btn = document.querySelector(".boost-project-card-get-btn");
  if (!btn || !window.PROJECT) return;
  btn.addEventListener("click", () => {
    const raw = (window.PROJECT.getButtonUrl || "").trim();
    if (!raw || raw === "#" || /^javascript:/i.test(raw)) {
      alert("Get button URL is not configured.");
      return;
    }
    let url = raw;
    if (!/^https?:\/\//i.test(url)) url = "https://" + url;
    window.open(url, "_blank", "noopener,noreferrer");
  });
}

function setupReferralSidebar() {
  const btn = document.querySelector(".btn-invite");
  const input = document.querySelector(".tm-boost-referral-email");
  const msg = document.querySelector(".tm-boost-referral-msg");
  if (!btn || !input || !msg) return;

  btn.addEventListener("click", () => {
    const email = (input.value || "").trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }
    msg.textContent =
      "Your referral has been successfully invited! An email will be sent to " +
      email +
      " within 24 hours.";
    msg.style.display = "block";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupGetButton();
  setupReferralSidebar();
});
