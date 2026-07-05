import os
import random
import datetime
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
from dotenv import load_dotenv

load_dotenv()

# --- Configuration (from .env) ---
WISHLIST_URL = os.getenv("WISHLIST_URL", "").strip()
DROP_THRESHOLD = float(os.getenv("DROP_THRESHOLD", "8"))
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "300"))

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_FROM = os.getenv("TWILIO_FROM", "").strip()
TWILIO_TO = os.getenv("TWILIO_TO", "").strip()

WHATSAPP_ENABLED = all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO])

CSV_FILE = os.getenv("CSV_FILE", "price_tracker.csv")
# Durable per-URL history (initial_price, current_low). Never pruned, so a
# transient wishlist dropout (OOS removal, fetch hiccup) can't wipe history.
HISTORY_FILE = os.getenv("HISTORY_FILE", "price_history.csv")
REQUEST_TIMEOUT = 20  # seconds

# User agents to vary request fingerprint and reduce bot-like activity
useragents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
]


def build_headers():
    return {
        "User-Agent": random.choice(useragents),
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }


def get_prod_info(soup):
    items_container = soup.find('ul', {'id': 'g-items'})
    if items_container is None:
        raise ValueError(
            "Could not find wishlist items on the page. "
            "Check that WISHLIST_URL is a public 'View only' sharable link."
        )
    product_list = items_container.find_all('li', {'class': 'g-item-sortable'})
    data = []
    for x in range(len(product_list)):
        name_el = product_list[x].find('h2', {'class': 'a-size-base'})
        product_name = name_el.find('a').text.strip() if name_el else "Unknown"
        price_element = product_list[x].find('span', {'class': 'a-price'})
        span_element = price_element and price_element.find('span')
        price_text = span_element and span_element.text.replace(',', '').replace('₹', '').replace('.00', '')
        price = int(price_text) if price_text else None
        url = 'https://amazon.in' + product_list[x].find('a')['href'].split('?')[0]
        data.append({
            'id': int(x + 1),
            'product_name': product_name,
            'current': price,
            'url': url,
        })
    return data


def fetch_latest_data():
    resp = requests.get(WISHLIST_URL, headers=build_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    return get_prod_info(soup)


def load_history():
    """Durable per-URL history. Prefer HISTORY_FILE; fall back to migrating
    from an existing CSV so already-tracked items aren't reset."""
    cols = ['url', 'initial_price', 'current_low']
    if os.path.isfile(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)[cols]
    if os.path.isfile(CSV_FILE):
        return pd.read_csv(CSV_FILE)[cols]
    return pd.DataFrame(columns=cols)


def _first_non_null(series):
    nn = series.dropna()
    return nn.iloc[0] if len(nn) else float('nan')


def update_prices():
    # Latest snapshot of the wishlist (source of truth for which items exist).
    df = pd.DataFrame(fetch_latest_data())  # columns: id, product_name, current, url

    # Bring forward tracked history (initial_price, current_low), keyed on the
    # stable product URL. History accumulates across all URLs ever seen and is
    # never pruned, so an item that drops out of the wishlist for a cycle keeps
    # its initial_price / current_low when it returns.
    hist = load_history()
    old_urls = set(hist['url'])

    df = df.merge(hist, on='url', how='left')
    # Seed history only for genuinely first-seen items. initial_price comes from
    # history's first non-null value (never overwritten by a NaN out-of-stock
    # price); current_low is the running min, skipping NaN.
    df['initial_price'] = df['initial_price'].fillna(df['current'])
    df['current_low'] = df[['current_low', 'current']].min(axis=1)

    # Update the durable history: union old history with this cycle's values so
    # URLs absent from the current fetch stay put for when they reappear.
    combined = pd.concat([hist, df[['url', 'initial_price', 'current_low']]], ignore_index=True)
    hist_out = combined.groupby('url', as_index=False).agg(
        initial_price=('initial_price', _first_non_null),
        current_low=('current_low', 'min'),
    )
    hist_out.to_csv(HISTORY_FILE, index=False)

    # Announce items that just appeared in the wishlist.
    added = df[~df['url'].isin(old_urls)]
    for _, row in added.iterrows():
        print(f"[new] tracking '{row['product_name']}' at ₹{row['current']}")

    # Renumber ids by current position (removed items simply drop off).
    df = df.reset_index(drop=True)
    df['id'] = df.index + 1

    df['offer'] = ((df['initial_price'] - df['current']) / df['initial_price']) * 100

    df['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df = df[['id', 'product_name', 'initial_price', 'current_low', 'current', 'offer', 'url', 'last_updated']]
    df.to_csv(CSV_FILE, index=False)
    print(df)


def generate_msg_content(offers):
    sentences = ""
    for _, row in offers.iterrows():
        sentences += (
            f"'{row['product_name']}' is now selling for ₹{row['current']}. "
            f"The price is {row['offer']:.2f}% off and the lowest price recorded is "
            f"₹{row['current_low']}. {row['url']}.\n\n"
        )
    print(sentences)
    return sentences


def send_msg(content):
    from twilio.rest import Client

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(from_=TWILIO_FROM, body=content, to=TWILIO_TO)
    return message.sid


def send_offer_notifications():
    df = pd.read_csv(CSV_FILE)
    discounts = df[df['offer'] > DROP_THRESHOLD]
    if discounts.empty:
        print(f"No offers over {DROP_THRESHOLD}% yet")
        return
    content = generate_msg_content(discounts)
    if WHATSAPP_ENABLED:
        print("WhatsApp alert sent, sid:", send_msg(content))
    else:
        print("(WhatsApp disabled — set Twilio vars in .env to enable alerts)")


def main():
    print(datetime.datetime.now())
    try:
        print("Updating prices...")
        update_prices()
        send_offer_notifications()
    except requests.RequestException as e:
        print(f"[warn] fetch failed, will retry next cycle: {e}")
    except ValueError as e:
        print(f"[warn] {e}")


if __name__ == "__main__":
    if not WISHLIST_URL:
        raise SystemExit("WISHLIST_URL is not set. Copy .env.example to .env and fill it in.")

    print(f"Tracking wishlist every {CHECK_INTERVAL_SECONDS}s "
          f"| threshold {DROP_THRESHOLD}% | WhatsApp {'ON' if WHATSAPP_ENABLED else 'OFF'}")

    main()  # run immediately on start
    schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
