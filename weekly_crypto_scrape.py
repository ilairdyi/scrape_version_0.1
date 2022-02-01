from time import sleep
from hedge_funds_scrape.cftc_get_W import Get_CFTC_Data
from on_chain.richest_btc_walletz_on_chain_W import Get_100_top_Wallets_Data


def get_all_cftc_data():
    cftc_data = Get_CFTC_Data('crypto_hedge_funds_db')
    cftc_data.call_all_cftc()

def get_all_on_chain():
    richest_btc_wallets = Get_100_top_Wallets_Data('crypto_onchain_db')
    richest_btc_wallets.call_all_richest_wallets()

#Calling all weekly functions
get_all_cftc_data()
sleep(4)
get_all_on_chain()