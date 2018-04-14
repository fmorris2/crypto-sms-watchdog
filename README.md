# Crypto SMS Watchdog

## Overview
The Crypto SMS Watchdog is a notification system which alerts specified phone numbers via SMS when targeted crypto-currencies undergo
a significant change in price. Targeted coins are loaded on startup from a file.

## Python Dependencies
- [requests](http://docs.python-requests.org/en/master/)
- [twilio](https://www.twilio.com/docs/libraries/python)

## Usage
1. Create a file named coins in the data/ directory. Put each coin on a new line. The coin name is the [coinmarketcap](https://coinmarketcap.com/) id, the portion of the coinmarketcap
URL which contains the coin name. For example, if you wanted to track Network Token (NTWK), the coinmarketcap page url is https://coinmarketcap.com/currencies/network-token/, and
so the line in the data/coins file would be as follows:
   - ```
     network-token
     ```
2. Create a file named twilio_credentials in the data/ directory. The file should be in this format:
   - ```
     Twilio Account SID
     Twilio Auth Token
     Twilio phone # to send messages from
     ```
3. Create a file named mobile_numbers in the data/ directory. This will contain the phone numbers to alert of any coin changes. One number per line.
An example is shown below:
   - ```
     +13334445555
     +14445556666
     ```
4. Run the program! On Unix-based systems, you can run this command:
   - ```
     nohup python main.py &
     ```
