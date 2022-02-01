from time import sleep
from sentiment_webs.fear_greed_index_D import Get_Fear_Greed_index
from marketcap_sites.coingecko_overallstats_D import Get_Overallstats_Coin_Gecko
from marketcap_sites.coingecko_price_vol_D import Get_Price_Vol_Coin_Gecko
from hedge_funds_scrape.cme_get_D import Get_CME_Data
from exchange_balance.get_data_viewbase_D import Get_Crypto_Balance
from coin_glass.oi_coin_glass_get_D import Get_Coin_Glass
from coin_glass.long_vs_shorts_coinglass_D import Get_CoinGlass_Longs_VS_Shorts
from coin_glass.liquidations_coinglass_D import Get_CoinGlass_Liquidations
from coin_glass.grayscale_holdings_coinglass_D import Get_Grayscaleholdings_Coin_Glass
from coin_glass.funding_rate_coinglass_D import Get_CoinGlass_funding
from coin_glass.exchange_flow_coinglass_D import Get_Exchange_Flow_Coin_Glass
from coin_glass.btc_options_oi_coinglass_D import Get_BitcoinBubble_Coin_Glass
from email_config import sendingemail

def get_all_sentiment_data():
    #'crypto_sentiment' is the db name this functions will connect too
    try:
        sentiment_fear_greed = Get_Fear_Greed_index('crypto_sentiment')
        sentiment_fear_greed.call_all()
    except:
        sendingemail("Failed--->Get_Fear_Greed_index('crypto_sentiment')")

def get_all_marketcap_sites():
    try:
        market_coingecko_price_vol = Get_Price_Vol_Coin_Gecko('Crypto_marketcaps')
        market_coingecko_price_vol.call_all()
    except:
        sendingemail("Failed--->Get_Price_Vol_Coin_Gecko('Crypto_marketcaps')")
    sleep(4)
    try:
        coingecko_overall_stats = Get_Overallstats_Coin_Gecko('Crypto_marketcaps')
        coingecko_overall_stats.call_all()
    except:
        sendingemail("Failed--->Get_Overallstats_Coin_Gecko('Crypto_marketcaps')")

def get_all_hedge_funds():
    try:
        cme_oi_vol = Get_CME_Data('crypto_hedge_funds_db')
        cme_oi_vol.call_all_cme()
    except:
        sendingemail("Failed--->Get_CME_Data('crypto_hedge_funds_db')")

def get_all_view_base():
    try:
        view_base = Get_Crypto_Balance('Crypto_Scraping')
        view_base.call_all_viewbase()
    except:
        sendingemail("Failed--->Get_Crypto_Balance('Crypto_Scraping')")

def get_all_coinglass():
    try:
        oi_coinglass = Get_Coin_Glass('crypto_coin_glass_db')
        oi_coinglass.call_all_oi_coinglass()
    except:
        sendingemail("Failed--->Get_Coin_Glass('crypto_coin_glass_db')")
    sleep(4)
    try:
        coin_glass_long_vs_shorts = Get_CoinGlass_Longs_VS_Shorts('crypto_coin_glass_db')
        coin_glass_long_vs_shorts.call_all_long_vs_short()
    except:
        sendingemail("Failed--->Get_CoinGlass_Longs_VS_Shorts('crypto_coin_glass_db')")
    sleep(4)
    try:
        coin_glass_liquidations = Get_CoinGlass_Liquidations('crypto_coin_glass_db')
        coin_glass_liquidations.call_all_liquidations_coinglass()
    except:
        sendingemail("Failed--->Get_CoinGlass_Liquidations('crypto_coin_glass_db')")
    sleep(4)
    try:
        coin_glass_grayscale_holdings = Get_Grayscaleholdings_Coin_Glass('crypto_coin_glass_db')
        coin_glass_grayscale_holdings.call_all_grayscale_holding()
    except:
        sendingemail("Failed--->Get_Grayscaleholdings_Coin_Glass('crypto_coin_glass_db')")
    sleep(4)
    try:
        coin_glass_funding = Get_CoinGlass_funding('crypto_coin_glass_db')
        coin_glass_funding.call_all_funding_rate()
    except:
        sendingemail("Failed--->Get_CoinGlass_funding('crypto_coin_glass_db')")
    sleep(4)
    try:
        coin_glass_exchange_flow = Get_Exchange_Flow_Coin_Glass('crypto_coin_glass_db')
        coin_glass_exchange_flow.call_all_exchange_flow()
    except:
        sendingemail("Failed--->Get_Exchange_Flow_Coin_Glass('crypto_coin_glass_db')")
    sleep(4)
    try:
        coin_glass_options_oi = Get_BitcoinBubble_Coin_Glass('crypto_coin_glass_db')
        coin_glass_options_oi.call_all_ptions_oi()
    except:
        sendingemail("Failed--->Get_BitcoinBubble_Coin_Glass('crypto_coin_glass_db')")

# This would go throught all of my daily scrapes
get_all_sentiment_data()
sleep(4)
get_all_marketcap_sites()
sleep(4)
get_all_hedge_funds()
sleep(4)
get_all_view_base()
sleep(4)
get_all_coinglass()
