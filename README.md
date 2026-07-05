# 💰 Amazon Wishlist Price-Drop Alert

Track an Amazon wishlist and get alerted when an item's price drops. Runs
**console-only** out of the box; add Twilio credentials to also get **WhatsApp**
alerts.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ec96af50-9e08-44dd-8919-13da11bdb70e" width="420" alt="WhatsApp price-drop alert">
</p>

## 🚀 Quick start

Needs **Python 3.10+**.

```bash
pip install -r requirements.txt
cp .env.example .env      # then set WISHLIST_URL (only required value)
python tracker_masked.py
```

First run creates `price_tracker.csv` (your baseline). Each cycle re-checks
prices and reports any drop over the threshold. Stop with `Ctrl+C`.

**Get your wishlist URL:** on Amazon, open the list → **Send list to others** →
**View only** → **Copy link** → paste as `WISHLIST_URL` in `.env`.

## ⚙️ Configuration (`.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `WISHLIST_URL` | ✅ | — | Public "View only" sharable wishlist link |
| `DROP_THRESHOLD` | | `8` | Notify when price drops more than this % |
| `CHECK_INTERVAL_SECONDS` | | `300` | Seconds between checks |
| `CSV_FILE` | | `price_tracker.csv` | Current snapshot output |
| `HISTORY_FILE` | | `price_history.csv` | Durable per-URL history (initial price, lowest seen) |
| `TWILIO_ACCOUNT_SID` | | — | Twilio SID (enables WhatsApp) |
| `TWILIO_AUTH_TOKEN` | | — | Twilio auth token |
| `TWILIO_FROM` | | — | Twilio WhatsApp sender, e.g. `whatsapp:+14155238886` |
| `TWILIO_TO` | | — | Your WhatsApp number, e.g. `whatsapp:+91...` |

WhatsApp turns on only when **all four** Twilio values are set; otherwise drops
print to the console.

**How history works:** `price_history.csv` accumulates each item's initial price
and lowest-ever price keyed by product URL, and is never pruned — so an item
going out of stock or dropping off the wishlist for a cycle keeps its history
when it returns. `price_tracker.csv` carries a `last_updated` timestamp, written
every cycle.

## 💬 WhatsApp alerts (optional)

1. Create a [Twilio](https://www.twilio.com/) account.
2. Activate the WhatsApp sandbox (or a WhatsApp sender).
3. Put your **Account SID** and **Auth Token** in `.env`.
4. Set `TWILIO_FROM` (sandbox number) and `TWILIO_TO` (your number, E.164).

## 🐳 Run 24×7 on TrueNAS SCALE (Docker)

The script self-loops, so it runs as one always-on container. Data persists to a
dataset, surviving restarts and updates. Needs TrueNAS SCALE 24.10 ("Electric
Eel")+.

1. **Create a dataset** for app data (e.g. `tank/appdata/pricedrop`) and note its
   host path (`/mnt/tank/appdata/pricedrop`).
2. **Copy this repo onto the NAS**, add your `.env` (`cp .env.example .env`).
3. **Point the volume at your dataset** in `docker-compose.yml`:
   ```yaml
   volumes:
     - /mnt/tank/appdata/pricedrop:/data   # <-- your dataset host path
   ```
4. **Build and start** (via SSH):
   ```bash
   docker compose up -d --build
   ```

Manage: `docker compose logs -f` (watch), `docker compose restart`,
`docker compose down` (stop). `restart: unless-stopped` auto-recovers after
reboot. CSV lives at `/mnt/tank/appdata/pricedrop/price_tracker.csv`.

> Prefer the Apps UI? **Apps → Discover → Custom App** accepts a Compose spec.
> Build the image first (`docker compose build`) or push to a registry, then
> reference it with `image:` instead of `build:`.

## 🔒 Security

Secrets live only in `.env` (git-ignored — never commit it). `price_tracker.csv`
and `price_history.csv` are generated locally and git-ignored too.
