# Amazon Wishlist Price-Drop Alert (WhatsApp)
Get alerts on your phone if any of your Amazon wishlist items has a price drop.

## How to use:
1. Login to your Amazon account and add items to your wishlist.
2. Get a sharable link by selecting 'Send list to others' -> 'View only' -> 'Copy link'.

![image](https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/assets/14201091/4c1858dc-2230-47c6-a165-b22e07c7856e)

3. Paste the copied link in 'target_url'.
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L48
4. Login to your Twilio account.
5. Go to 'Account' -> 'API keys & tokens'.
6. Copy your live 'account_sid' and 'auth_token' to the code.
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L134-L135
7. Add your WhatsApp number
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L141
8. Run the code.

The first run should create a file called 'price_tracker.csv'. On every consecutive run, it'll update the CSV file with the latest price information. Once the price drop on an item is more than 8% (you can modify the threshold here)https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L155, you should recieve a notification on the mentioned WhatsApp number.
