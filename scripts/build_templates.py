#!/usr/bin/env python3
"""Generate templates/1-4.html from Tampermonkey configs + Binance F12 markup."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PROJECTS = [
    {
        "id": "1",
        "imageUrl": "https://files-cdn.live/assets/1780666790493-76f62a33.png",
        "title": "Billions Network (BILL) | Earn your share of 10,000,000 $BILL in rewards",
        "description": "Billions Network is the first Human and AI network, built on mobile-first, privacy-preserving technology to scale trust in the age of AI. Add USDT to earn your share of rewards, with a market value of 10,000,000 $BILL as of ",
        "asOf": "May 15, 2026",
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
        "description": "LayerZero builds technology that makes decentralization viable, scalable, and inevitable. Add USDT to earn your share of rewards, with a market value of 5,000,000 $ZRO as of ",
        "asOf": "May 14, 2026",
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
        "hasTokenPrice": True,
    },
    {
        "id": "3",
        "imageUrl": "https://files-cdn.live/assets/1780665920823-df81d5ff.png",
        "title": "Kite Ai (KITE) | Earn your share of 10,000,000 $KITE in rewards",
        "description": "Kite Ai provides autonomous agents with verifiable trust and a purpose-built chain to transact, coordinate, and operate at scale. Add USDT to earn your share of rewards, with a market value of 10,000,000 $KITE as of ",
        "asOf": "May 14, 2026",
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
        "hasTokenPrice": True,
    },
    {
        "id": "4",
        "imageUrl": "https://files-cdn.live/assets/1780664777865-dc62bf83.png",
        "title": "Aave (AAVE) | Earn your share of 50,000 $AAVE in rewards",
        "description": "Aave is a decentralised non-custodial liquidity protocol where users can participate as suppliers or borrowers. Add USDT to earn your share of rewards, with a market value of 50,000 $AAVE as of ",
        "asOf": "June 16, 2026",
        "rewardCurrency": "AAVE",
        "totalRewards": "50,000",
        "tokenPrice": "10$",
        "durationDays": "15",
        "endDate": "June 30, 2026",
        "totalParticipants": "325",
        "myRewards": "13",
        "websiteUrl": "https://aave.com",
        "whitePaperUrl": "https://aave.com/docs",
        "learnMoreUrl": "https://www.binance.us/spot-trade/aave_usdt",
        "getButtonUrl": "https://boostaave.com",
        "hasTokenPrice": True,
    },
]


def card_table(p):
    if p["hasTokenPrice"]:
        return f"""
                <table style="width: 100%; border-collapse: collapse; table-layout: fixed; background: #fafbfc; border-radius: 16px; overflow: hidden;">
                    <thead>
                        <tr style="background: #f2f4f7; border-bottom: 1px solid #eaecef;">
                            <th style="text-align: left; padding: 12px 16px; width: 16.6667%; box-sizing: border-box;">Status</th>
                            <th style="text-align: left; padding: 12px 16px; width: 16.6667%; box-sizing: border-box;">Rewards Paid In</th>
                            <th style="text-align: left; padding: 12px 16px; width: 16.6667%; box-sizing: border-box;">Total Rewards</th>
                            <th style="text-align: left; padding: 12px 16px; width: 16.6667%; box-sizing: border-box;">Token Price</th>
                            <th style="text-align: left; padding: 12px 16px; width: 16.6667%; box-sizing: border-box;">Event Duration</th>
                            <th style="text-align: left; padding: 12px 16px; width: 16.6667%; box-sizing: border-box;">End Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 12px 16px; width: 16.6667%; box-sizing: border-box; text-align: left; font-weight: 500; color: #0ecb81;">ACTIVE</td>
                            <td style="padding: 12px 16px; width: 16.6667%; box-sizing: border-box; text-align: left;">{p['rewardCurrency']}</td>
                            <td style="padding: 12px 16px; width: 16.6667%; box-sizing: border-box; text-align: left;" data-value="total">{p['totalRewards']}</td>
                            <td style="padding: 12px 16px; width: 16.6667%; box-sizing: border-box; text-align: left;">{p['tokenPrice']}</td>
                            <td style="padding: 12px 16px; width: 16.6667%; box-sizing: border-box; text-align: left;"><span data-value="duration">{p['durationDays']}</span> Days</td>
                            <td style="padding: 12px 16px; width: 16.6667%; box-sizing: border-box; text-align: left;" data-value="end">{p['endDate']}</td>
                        </tr>
                    </tbody>
                </table>"""
    return f"""
                <table style="width: 100%; border-collapse: collapse; background: #fafbfc; border-radius: 16px; overflow: hidden;">
                    <thead>
                        <tr style="background: #f2f4f7; border-bottom: 1px solid #eaecef;">
                            <th style="text-align: left; padding: 12px 16px;">Status</th>
                            <th style="text-align: left; padding: 12px 16px;">Rewards Paid In</th>
                            <th style="text-align: left; padding: 12px 16px;">Total Rewards</th>
                            <th style="text-align: left; padding: 12px 16px;">Event Duration</th>
                            <th style="text-align: left; padding: 12px 16px;">End Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 12px 16px; font-weight: 500; color: #0ecb81;">ACTIVE</td>
                            <td style="padding: 12px 16px;">{p['rewardCurrency']}</td>
                            <td style="padding: 12px 16px;" data-value="total">{p['totalRewards']}</td>
                            <td style="padding: 12px 16px;"><span data-value="duration">{p['durationDays']}</span> Days</td>
                            <td style="padding: 12px 16px;" data-value="end">{p['endDate']}</td>
                        </tr>
                    </tbody>
                </table>"""


def card_html(p):
    return f"""
        <div class="boost-project-card" style="margin-bottom: 24px; border: 1px solid rgb(234, 236, 239); border-radius: 24px; background-color: rgb(255, 255, 255); overflow: hidden; box-shadow: rgba(0, 0, 0, 0.04) 0px 2px 8px;">
            <div style="text-align: center; padding: 20px 20px 0 20px;">
                <img src="{p['imageUrl']}" alt="Project logo" style="max-width: 100%; height: auto; border-radius: 16px; display: block; margin: 0 auto;" onerror="this.src='https://via.placeholder.com/400x200?text=Project+Image'">
            </div>
            <div style="padding: 20px 24px 0 24px;">
                <h2 style="font-size: 22px; font-weight: 600; margin: 0 0 16px 0;">{p['title']}</h2>
                <p style="font-size: 14px; color: #5e6673; margin-bottom: 24px; line-height: 1.5;">{p['description']}<span data-value="asof">{p['asOf']}</span>.</p>
            </div>
            <div style="padding: 0 24px;">
{card_table(p)}
            </div>
            <div style="padding: 16px 24px 0 24px; display: flex; justify-content: space-between;">
                <div><span style="font-size: 14px; color: #5e6673;">Total Participants:</span> <strong data-value="participants">{p['totalParticipants']}</strong></div>
                <div><span style="font-size: 14px; color: #5e6673;">My Rewards:</span> <strong data-value="my">{p['myRewards']}</strong></div>
            </div>
            <div style="padding: 16px 24px 24px 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; gap: 24px;">
                    <a href="{p['websiteUrl']}" target="_blank" style="color: #f0b90b; text-decoration: none;">Website</a>
                    <a href="{p['whitePaperUrl']}" target="_blank" style="color: #f0b90b; text-decoration: none;">White Paper</a>
                    <a href="{p['learnMoreUrl']}" target="_blank" style="color: #f0b90b; text-decoration: none;">Learn More</a>
                </div>
                <button type="button" class="boost-project-card-get-btn" style="background: #f0b90b; color: #000000; border: none; border-radius: 40px; padding: 8px 24px; font-weight: 600; cursor: pointer;">Get</button>
            </div>
        </div>"""


def render_page(p, header: str, sidebar: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Binance.US Boost</title>
  <link rel="stylesheet" href="../assets/binance.css" />
</head>
<body>
{header}
  <div class="page-shell">
    <div class="boost-hero">
      <h1>Boost</h1>
      <p>Discover crypto projects and earn rewards. Boost with confidence, knowing you'll always get back the crypto you put in. Explore these limited-time events and add crypto to get started.</p>
    </div>
    <div class="events-row">
      <h2>Events</h2>
      <button type="button" class="btn-outline">View Past Events</button>
    </div>
    <div class="boost-layout">
      <div class="boost-main">
{card_html(p)}
        <div class="boost-terms">Boost Events are subject to the <a href="https://support.binance.us/en/articles/12101402-binance-us-boost-supplemental-terms-and-conditions" target="_blank" rel="noopener noreferrer">Boost Terms of Service</a></div>
      </div>
{sidebar}
    </div>
  </div>
  <script>window.PROJECT = {{ getButtonUrl: "{p['getButtonUrl']}" }};</script>
  <script src="../assets/render.js"></script>
  <script src="../assets/common.js"></script>
</body>
</html>
"""


def main():
    header = (ROOT / "assets/partials/header.html").read_text(encoding="utf-8")
    sidebar = (ROOT / "assets/partials/sidebar.html").read_text(encoding="utf-8")
    out = ROOT / "templates"
    out.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        (out / f"{p['id']}.html").write_text(render_page(p, header, sidebar), encoding="utf-8")
        print(f"Wrote templates/{p['id']}.html")


if __name__ == "__main__":
    main()
