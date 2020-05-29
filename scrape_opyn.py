import get_prices as prices
import options_stats as op_stat
import time
import pandas as pd
from datetime import datetime

class Data:
    def __init__(self, api_key):
        '''Instantiate the class with your Infuria API Key'''
        self.api_key = api_key

    def collect(self, expiry, strike, smart_contract_address, freq=10):
        """
        Collects and saves Opyn option greeks data.

        Parameters
        -------------
        expiry: int
            The maturity date of the option in Unix Epoch Seconds. This can be
            found by navigating the smart-contract input data for a particular
            option of interest. As an example consider the `_expiry` parameter for the
            following link:
            https://etherscan.io/tx/0xd6366d32282acb2641512ce3c898b0466b5c908361fa18db168a379e1c4027fe
        strike: int
            The strike of the selected option
        smart_contract_address: str
            The smart-contract address of the particular option. A list of addresses
            can be found here: https://opyn.gitbook.io/opyn/abis-smart-contract-addresses
        freq: int
            The time (in seconds) to wait before collecting new data. By default
            the time delay is 10 seconds. Be warned that retrieving data too quickly
            can lead to potential problems with the API.
        Returns
        -------------
        csv:
            Saves a snapshot of the option greeks every 10 seconds in a csv file.

        Example
        -------------
        >>> collect(expiry=1593158400, strike=180, smart_contract_address='0xd48723715Cc1CA4fB10427a9a298094EC1e08aDB')
        180_PUT-2020_May_29-16_08_50.csv
        ....
        """
        # Create a live connection
        load = prices.Prices(self.api_key)
        while True:
            data = load.bid_ask(smart_contract_address)
            time_to_maturity = (expiry - time.time())/(60*60*24*365) # Convert seconds to years
            df = pd.DataFrame(op_stat.get_greeks(data[2], data[0], strike, time_to_maturity)).T
            df.columns = ['time','iv', 'gamma', 'theta', 'vega', 'delta']
            label = datetime.now().strftime(str(strike)+"_"+ "PUT" + '-%Y_%B_%d-%H_%M_%S.csv')
            print(label)
            df.to_csv(label+'.csv')
            time.sleep(freq)
