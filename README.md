# :moneybag: Amazon Wishlist Price-Drop Alert (WhatsApp)
Get alerts on your phone if any of your Amazon wishlist items has a price drop.

## :rotating_light: Alert:
![Screenshot](https://github.com/user-attachments/assets/ec96af50-9e08-44dd-8919-13da11bdb70e)



## :ledger: Output logs:
```
2023-09-25 02:48:37.795554
Updating prices...
   id                                       product_name  initial_price  current_low  current      offer                               url
0   1  Crucial RAM 16GB DDR5 4800MHz CL40 Laptop Memo...           3907         3907     3907   0.000000  https://amazon.in/dp/B09S2MN8JH/
1   2  Crucial P5 Plus 2TB PCIe 4.0 3D NAND NVMe M.2 ...          11700        11700    15500 -32.478632  https://amazon.in/dp/B098WKQRDL/
2   3  Samsung 980 PRO 2TB Up to 7,000 MB/s PCIe 4.0 ...          16389        16389    16389   0.000000  https://amazon.in/dp/B08QJHLC8J/
3   4  Apple 2023 MacBook Air Laptop with M2 chip: 38...         145790       145790   145790   0.000000  https://amazon.in/dp/B0C76D5QPG/
4   5  Apple 2023 MacBook Pro Laptop M2 Pro chip with...         199900       199900   199900   0.000000  https://amazon.in/dp/B0BSHHL4TY/
No offers yet
```

## :information_desk_person: How to use:
1. Login to your Amazon account and add items to your wishlist.
2. Get a sharable link by selecting `Send list to others` -> `View only` -> `Copy link`.

![image](https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/assets/14201091/4c1858dc-2230-47c6-a165-b22e07c7856e)

3. Paste the copied link in `target_url`.
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L48
4. Login to your Twilio account.
5. Go to `Account` -> `API keys & tokens`.
6. Copy your live `account_sid` and `auth_token` to the code.
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L134-L135
7. Add your WhatsApp number
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L141
8. Run the code. The first run should create a file called `price_tracker.csv`. On every consecutive run, it'll update the CSV file with the latest price information. Once the price drop on an item is more than `8%` (you can modify the threshold here)
https://github.com/aneeshtigga/amazon_wl_pricedrop_alert/blob/94b2d6739c3b3d685fae09ddb9051cb719528d4d/tracker_masked.py#L155


