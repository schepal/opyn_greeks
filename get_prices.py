from web3 import Web3, HTTPProvider
import json
import requests
import pandas as pd

class Prices:
    def __init__(self, api_key):
        '''Instantiate the class with your Infuria API Key'''
        self.api_key = api_key

    def connect(self):
        '''Setup a connection to the Opyn Smart Contract Address'''
        infuria_url = 'https://mainnet.infura.io/v3/' + self.api_key
        w3 = Web3(HTTPProvider(infuria_url))
        abi = json.loads('[{"constant":true,"inputs":[{"name":"oTokenAddress","type":"address"},{"name":"payoutTokenAddress","type":"address"},{"name":"oTokensToSell","type":"uint256"}],"name":"premiumReceived","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"receiver","type":"address"},{"name":"oTokenAddress","type":"address"},{"name":"payoutTokenAddress","type":"address"},{"name":"oTokensToSell","type":"uint256"}],"name":"sellOTokens","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"receiver","type":"address"},{"name":"oTokenAddress","type":"address"},{"name":"paymentTokenAddress","type":"address"},{"name":"oTokensToBuy","type":"uint256"}],"name":"buyOTokens","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"oTokenAddress","type":"address"},{"name":"paymentTokenAddress","type":"address"},{"name":"oTokensToBuy","type":"uint256"}],"name":"premiumToPay","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"UNISWAP_FACTORY","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"paymentToken","type":"address"},{"name":"oToken","type":"address"},{"name":"_amt","type":"uint256"},{"name":"_transferTo","type":"address"}],"name":"uniswapBuyOToken","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_uniswapFactory","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":false,"name":"seller","type":"address"},{"indexed":false,"name":"receiver","type":"address"},{"indexed":false,"name":"oTokenAddress","type":"address"},{"indexed":false,"name":"payoutTokenAddress","type":"address"},{"indexed":false,"name":"oTokensToSell","type":"uint256"}],"name":"SellOTokens","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"buyer","type":"address"},{"indexed":false,"name":"receiver","type":"address"},{"indexed":false,"name":"oTokenAddress","type":"address"},{"indexed":false,"name":"paymentTokenAddress","type":"address"},{"indexed":false,"name":"oTokensToBuy","type":"uint256"},{"indexed":false,"name":"premiumPaid","type":"uint256"}],"name":"BuyOTokens","type":"event"}]')

        # Connect to the ​Options Exchange Smart Contract (Currently Using the Old Address)
        options_address = w3.toChecksumAddress('0x5778f2824a114F6115dc74d432685d3336216017')
        contract = w3.eth.contract(address=options_address, abi=abi)
        return contract

    def bid_ask(self, option_contract_address):
        """
        Retrieves the market related data to input into Black-Scholes
        to calculate the Greeks.

        Parameters
        -------------
        option_contract_address: str
            The smart-contract address of the particular option. A list of addresses
            can be found here: https://opyn.gitbook.io/opyn/abis-smart-contract-addresses

        Returns
        -------------
        tuple:
            Returns the current price of ETH, option bid price and option ask price

        Example
        -------------
        # oETH Put $200, 6/05/20 Contract Address: 0x4edF4f93A45fad46E5a2450bFcFFE8Ff53D0a5B2

        >>> bid_ask("0x4edF4f93A45fad46E5a2450bFcFFE8Ff53D0a5B2")
        (219.38, 1.1013178220787114, 1.1099156299187243)
        """
        opyn_contract = self.connect()
        # Retrieve the most recent price of ETH using CoinGecko's API
        eth_price = requests.get("https://api.coingecko.com/api/v3/simple/price?"\
                             "ids=ethereum&vs_currencies=usd").json()['ethereum']['usd']

        # Retrieve the bid price of the opyn option
        bid = opyn_contract.functions.premiumReceived(option_contract_address,
                                       "0x0000000000000000000000000000000000000000",
                                       10000000).call()/(10**18)*(eth_price)

        # Retrieve the ask price of the opyn option
        ask = opyn_contract.functions.premiumToPay(option_contract_address,
                                            "0x0000000000000000000000000000000000000000",
                                            10000000).call()/(10**18)*eth_price
        return eth_price, bid, ask
