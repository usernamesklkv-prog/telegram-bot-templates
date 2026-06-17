#!/usr/bin/env python3
"""Generate templates/1-4.html from Tampermonkey project configs."""

from pathlib import Path

REFERRAL_DISCLAIMER = (
    'Please note that for users in CIS countries and non-U.S. residents, emails may '
    'automatically be filtered into the "Promotions," "Subscriptions," "Spam," and other '
    'folders in your email service. We recommend checking these folders periodically so '
    "you don't miss important project notifications."
)

REFERRAL_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 64 64" fill="none" aria-hidden="true">
<circle cx="24" cy="22" r="8" stroke="#F0B90B" stroke-width="3" fill="none"/>
<path d="M8 54c0-11 9.5-18 16-18s16 7 16 18" stroke="#F0B90B" stroke-width="3" fill="none" stroke-linecap="round"/>
<circle cx="44" cy="26" r="6" stroke="#F0B90B" stroke-width="2.8" fill="none"/>
<path d="M33 52c0-9 7.5-14.5 13-14.5s13 5.5 13 14.5" stroke="#F0B90B" stroke-width="2.6" fill="none" stroke-linecap="round"/>
</svg>"""

PROJECTS = [
    {
        "id": "1",
        "imageUrl": "https://files-cdn.live/assets/1780666790493-76f62a33.png",
        "title": "Billions Network (BILL) | Earn your share of 10,000,000 $BILL in rewards",
        "description": "Billions Network is the first Human and AI network, built on mobile-first, privacy-preserving technology to scale trust in the age of AI. Add USDT to earn your share of rewards, with a market value of 10,000,000 $BILL as of May 15, 2026.",
        "rewardCurrency": "BILL",
        "totalRewards": "10,000,000",
        "tokenPrice": "0.01$",
        "durationDays": "10",
        "endDate": "May 23, 2026",
        "totalParticipants": "1125",
        "myRewards": "13",
        "websiteUrl": "https://billions.network",
        "whitePaperUrl": "https://cdn.prod.website-files.com/682b2da9ef522c285ba6550a/69c2d6c8710e5a24ff67111f_704e9fcb4864828b750e434703526a87_Billions_WhitePaper_v5.pdf",
        "learnMoreUrl": "#",
        "getButtonUrl": "https://billionsnetworkboost.com",
        "hasTokenPrice": True,
    },
    {
        "id": "2",
        "imageUrl": "https://files-cdn.live/assets/1780664933440-93c785cb.png",
        "title": "LayerZero (ZRO) | Earn your share of 5,000,000 $ZRO in rewards",
        "description": "LayerZero builds technology that makes decentralization viable, scalable, and inevitable. Add USDT to earn your share of rewards, with a market value of 5,000,000 $ZRO as of May 14, 2026.",
        "rewardCurrency": "ZRO",
        "totalRewards": "5,000,000",
        "tokenPrice": "0.1$",
        "durationDays": "10",
        "endDate": "May 30, 2026",
        "totalParticipants": "1288",
        "myRewards": "***",
        "websiteUrl": "https://layerzero.network",
        "whitePaperUrl": "https://layerzero.network/publications/LayerZero_Whitepaper_V2.1.0.pdf",
        "learnMoreUrl": "#",
        "getButtonUrl": "https://boostzro.us",
        "hasTokenPrice": False,
    },
    {
        "id": "3",
        "imageUrl": "https://files-cdn.live/assets/1780665920823-df81d5ff.png",
        "title": "Kite Ai (KITE) | Earn your share of 10,000,000 $KITE in rewards",
        "description": "Kite Ai provides autonomous agents with verifiable trust and a purpose-built chain to transact, coordinate, and operate at scale. Add USDT to earn your share of rewards, with a market value of 10,000,000 $KITE as of May 14, 2026.",
        "rewardCurrency": "KITE",
        "totalRewards": "10,000,000",
        "tokenPrice": "0.01$",
        "durationDays": "16",
        "endDate": "May 30, 2026",
        "totalParticipants": "1288",
        "myRewards": "***",
        "websiteUrl": "https://gokite.ai",
        "whitePaperUrl": "https://gokite.ai/kite-whitepaper",
        "learnMoreUrl": "#",
        "getButtonUrl": "https://boostkite.us",
        "hasTokenPrice": False,
    },
    {
        "id": "4",
        "imageUrl": "https://files-cdn.live/assets/1780664777865-dc62bf83.png",
        "title": "Aave (AAVE) | Earn your share of 50,000 $AAVE in rewards",
        "description": "Aave is a decentralised non-custodial liquidity protocol where users can participate as suppliers or borrowers. Add USDT to earn your share of rewards, with a market value of 50,000 $AAVE as of May 13, 2026.",
        "rewardCurrency": "AAVE",
        "totalRewards": "50,000",
        "tokenPrice": "10$",
        "durationDays": "10",
        "endDate": "May 23, 2026",
        "totalParticipants": "1125",
        "myRewards": "13",
        "websiteUrl": "https://aave.com",
        "whitePaperUrl": "https://aave.com/docs",
        "learnMoreUrl": "https://www.binance.us/spot-trade/aave_usdt",
        "getButtonUrl": "https://boostaave.com",
        "hasTokenPrice": True,
    },
]


def table_head(p):
    if p["hasTokenPrice"]:
        return """<th>Status</th><th>Rewards Paid In</th><th>Total Rewards</th><th>Token Price</th><th>Event Duration</th><th>End Date</th>"""
    return """<th>Status</th><th>Rewards Paid In</th><th>Total Rewards</th><th>Event Duration</th><th>End Date</th>"""


def table_row(p):
    if p["hasTokenPrice"]:
        return f"""<td style="font-weight:500;color:#0ecb81;">ACTIVE</td>
              <td>{p['rewardCurrency']}</td>
              <td data-value="total">{p['totalRewards']}</td>
              <td>{p['tokenPrice']}</td>
              <td>{p['durationDays']} Days</td>
              <td data-value="end">{p['endDate']}</td>"""
    return f"""<td style="font-weight:500;color:#0ecb81;">ACTIVE</td>
              <td>{p['rewardCurrency']}</td>
              <td data-value="total">{p['totalRewards']}</td>
              <td>{p['durationDays']} Days</td>
              <td data-value="end">{p['endDate']}</td>"""


def render(p):
    table_style = 'table-layout: fixed;' if p["hasTokenPrice"] else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Binance.US Boost</title>
  <link rel="stylesheet" href="../assets/boost-page.css" />
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a class="logo" href="#"><img src="https://public.bnbstatic.com/static/images/common/logo.png" alt="Binance.US" onerror="this.src='https://files-cdn.live/assets/1778672960531-22e5fc49.png'" /></a>
      <nav class="main-nav">
        <a href="#">Buy Crypto</a>
        <a href="#">Markets</a>
        <a href="#">Trade</a>
        <a href="#">Earn</a>
        <a href="#">Manage Assets</a>
        <a href="#" class="active">Boost</a>
        <a href="#">Services</a>
        <a href="#">Institutions</a>
        <a href="#">Staking</a>
        <a href="#">OTC</a>
      </nav>
      <div class="header-actions">
        <button class="btn-deposit" type="button">Deposit</button>
        <span class="icon-btn">🌐</span>
        <span class="icon-btn">👤</span>
        <span class="icon-btn">💼</span>
      </div>
    </div>
  </header>

  <main class="boost-page">
    <h1>Boost</h1>
    <div class="tabs">
      <button class="tab active" type="button">Events</button>
      <button class="tab" type="button">History</button>
    </div>

    <div class="boost-layout">
      <div class="boost-main">
        <div class="boost-project-card">
          <div style="text-align:center;padding:20px 20px 0;">
            <img src="{p['imageUrl']}" alt="Project logo" style="max-width:100%;height:auto;border-radius:16px;display:block;margin:0 auto;" />
          </div>
          <div style="padding:20px 24px 0;">
            <h2 style="font-size:22px;font-weight:600;margin:0 0 16px;">{p['title']}</h2>
            <p style="font-size:14px;color:#5e6673;margin-bottom:24px;line-height:1.5;">{p['description']}</p>
          </div>
          <div style="padding:0 24px;">
            <table style="{table_style}">
              <thead><tr>{table_head(p)}</tr></thead>
              <tbody><tr>{table_row(p)}</tr></tbody>
            </table>
          </div>
          <div style="padding:16px 24px 0;display:flex;justify-content:space-between;">
            <div><span style="font-size:14px;color:#5e6673;">Total Participants:</span> <strong data-value="participants">{p['totalParticipants']}</strong></div>
            <div><span style="font-size:14px;color:#5e6673;">My Rewards:</span> <strong data-value="my">{p['myRewards']}</strong></div>
          </div>
          <div style="padding:16px 24px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div style="display:flex;gap:24px;flex-wrap:wrap;">
              <a href="{p['websiteUrl']}" target="_blank" style="color:#f0b90b;">Website</a>
              <a href="{p['whitePaperUrl']}" target="_blank" style="color:#f0b90b;">White Paper</a>
              <a href="{p['learnMoreUrl']}" target="_blank" style="color:#f0b90b;">Learn More</a>
            </div>
            <button type="button" class="boost-project-card-get-btn">Get</button>
          </div>
        </div>
      </div>

      <aside class="boost-sidebar">
        {REFERRAL_SVG}
        <h3>Referral Program</h3>
        <input class="tm-boost-referral-email" type="email" placeholder="Email address" autocomplete="email" />
        <button class="btn-invite" type="button">Invite referral</button>
        <div class="tm-boost-referral-disclaimer">{REFERRAL_DISCLAIMER}</div>
        <div class="tm-boost-referral-msg"></div>
      </aside>
    </div>

    <div class="boost-footer-links">
      <a href="#">Boost Terms of Service</a>
      <a href="#">View Past Events</a>
    </div>
  </main>

  <script>window.PROJECT = {{ getButtonUrl: "{p['getButtonUrl']}" }};</script>
  <script src="../assets/render.js"></script>
  <script src="../assets/common.js"></script>
</body>
</html>
"""


def main():
    out = Path(__file__).resolve().parent.parent / "templates"
    out.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        (out / f"{p['id']}.html").write_text(render(p), encoding="utf-8")
        print(f"Wrote templates/{p['id']}.html")


if __name__ == "__main__":
    main()
