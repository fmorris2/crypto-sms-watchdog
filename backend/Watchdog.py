import time
from requests import get
from twilio.rest import Client

class Watchdog:
    COINS_FILE_PATH = '/data/coins'
    MOBILE_NUMBERS_FILE_PATH = '/data/mobile_numbers'
    TWILIO_CREDS_FILE_PATH = '/data/twilio_credentials'

    COIN_MARKET_CAP_API_ENDPOINT = 'https://api.coinmarketcap.com/v1/ticker/'
    PERCENT_CHANGE_THRESHOLD = 10

    CYCLE_TIME = 60 #in seconds
    coins = []
    mobile_numbers = []
    twilio_creds = ()

    def __init__(self):
        from main import ROOT_PATH
        self.root_path = ROOT_PATH
        self.load_coins()
        self.load_mobile_numbers()
        self.load_twilio_creds()
        self.sms_client = Client(self.twilio_creds[0], self.twilio_creds[1]);

    def run(self):
        while(True):
            for i in range(0, len(self.coins)):
                if self.has_change(i):
                    print self.coins[i][0] + " has notable change... notifying SMS"
                    self.notify_sms(i)
            time.sleep(self.CYCLE_TIME)

    def has_change(self, coin_index):
        new_info = self.get_coin_info(self.coins[coin_index][0])
        old_info = self.coins[coin_index][1]

        if old_info is None:
            self.coins[coin_index][1] = new_info

        if new_info is None or old_info is None:
            return False

        has_notable_change = self.has_notable_change(old_info, new_info)
        if has_notable_change:
            self.coins[coin_index] = (self.coins[coin_index][0], new_info)

        return has_notable_change

    def has_notable_change(self, old_info, new_info):
        for i in range(0, 3):
            num_one = old_info[i]
            num_two = new_info[i]
            diff = abs(float(num_one) - float(num_two))
            perc_change = (diff / float(num_one)) * 100
            return perc_change >= self.PERCENT_CHANGE_THRESHOLD

    def notify_sms(self, coin_index):
        coin = self.coins[coin_index]
        msg =  coin[1][5]+" ("+coin[1][6]+")\n" \
                + "Market cap: $" + self.human_format(float(coin[1][0])) + "\n" \
                + "Price: $" + self.human_format(float(coin[1][4])) + "\n" \
                + "1h: " + self.plus_prepended(coin[1][1]) + "%\n" \
                + "24h: " + self.plus_prepended(coin[1][2]) + "%\n" \
                + "7d: " + self.plus_prepended(coin[1][3]) + "%\n" \

        for number in self.mobile_numbers:
            self.sms_client.messages.create(to=number,
                                    from_= self.twilio_creds[2],
                                    body=msg)

    def plus_prepended(self, str):
        return str if "-" in str else "+"+str

    def human_format(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def get_coin_info(self, coin):
        print coin
        try:
            response = get(self.COIN_MARKET_CAP_API_ENDPOINT+coin)
            json = response.json()[0]
            return (json['market_cap_usd'],json['percent_change_1h'],
                    json['percent_change_24h'], json['percent_change_7d'],
                    json['price_usd'], json['name'], json['symbol'])
        except Exception:
            return None

    def load_coins(self):
        for coin in open(self.root_path + self.COINS_FILE_PATH).read().splitlines():
            self.coins.append((coin, self.get_coin_info(coin)))

    def load_mobile_numbers(self):
        self.mobile_numbers = open(self.root_path + self.MOBILE_NUMBERS_FILE_PATH).read().splitlines()

    def load_twilio_creds(self):
        self.twilio_creds = open(self.root_path + self.TWILIO_CREDS_FILE_PATH).read().splitlines()