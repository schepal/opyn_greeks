# Opyn Greeks Data Collector
A tool that can be used to calculate and store the greeks of Opyn put option contracts in a csv file.

## Example
``` python
>>> import scrape_opyn as so
>>> api_key = "INFURIA_API_KEY"
# Instantiate the class with your Infuria API Key
>>> data = so.Data(api_key)

# Configure Option Parameters:
# oETH Put $180, 6/26/20 Contract Address: 0xd48723715Cc1CA4fB10427a9a298094EC1e08aDB
# Unix epoch timestamp for the option's expiry date
>>> time_expiry=1593158400 
# Strike price of the option
>>> strike=180
# Smart-contract address for the option
>>> address='0xd48723715Cc1CA4fB10427a9a298094EC1e08aDB'
# Frequency of how often to collect new data (seconds)
>>> freq=10

>>> data.collect(expiry=time_expiry, strike=strike, smart_contract_address=address, freq=freq)
# Function will print out the name of the csv file being saved every "freq" seconds
'180_PUT-2020_May_29-16_08_50.csv'
'180_PUT-2020_May_29-16_09_00.csv'
...
```

### Dependencies
- pandas==1.0.3
- requests==2.21.0
- numpy==1.17.3
- tqdm==4.38.0
- web3==5.10.0
- py_vollib==1.0.1

