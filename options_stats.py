import py_vollib.black_scholes.implied_volatility as iv
import py_vollib.black_scholes as bs
import py_vollib.black_scholes.greeks.numerical as greek
import pandas as pd
import numpy as np
import time

def get_vol(option_price, spot, strike, T, r=0, option_type='p'):
    """
    Calculates the implied volatility of an option.

    Parameters
    -------------
    option_price: int
        The market price of the option
    spot: int
        The current price of the underlying asset (in this case ETH)
    strike: int
        The strike price of the option contract
    T: int
        The time to maturity of the option in years
    r: int
        The current interest rate (assuming zero by default)
    option_type: str
        Option can be either a call ('c') or put ('p')

    Returns
    -------------
    int:
        Returns the annualised implied volatility of the option

    Example
    -------------
    >>> get_vol(option_price=1.1031, spot=200,
                strike=150, T=0.034, r=0, option_type='p')

    1.0713281006448705
    """
    return iv.implied_volatility(option_price, spot, strike, T, r, option_type)

def get_greeks(option_price, spot, strike, T, r=0, option_type='p'):
    """
    Calculates the option greek values.

    Parameters
    -------------
    option_price: int
        The market price of the option
    spot: int
        The current price of the underlying asset (in this case ETH)
    strike: int
        The strike price of the option contract
    T: int
        The time to maturity of the option in years
    r: int
        The current interest rate (assuming zero by default)
    option_type: str
        Option can be either a call ('c') or put ('p')

    Returns
    -------------
    list:
        Current time, implied volatility, gamma, theta, vega and delta

    Example
    -------------
    >>> get_greeks(option_price=1.1031, spot=200,
                strike=150, T=0.034, r=0, option_type='p')

    [1590791181.920008, 1.0713281006448705, 0.0030137160868808216,
    -0.18953283576618232, 0.04391003074487654, -0.05996451476744491]
    """
    iv = get_vol(option_price, spot, strike, T, r)
    gamma = greek.agamma(option_type, spot, strike, T, r, iv)
    theta = greek.atheta(option_type, spot, strike, T, r, iv)
    delta = greek.adelta(option_type, spot, strike, T, r, iv)
    vega = greek.avega(option_type, spot, strike, T, r, iv)
    return [time.time(), iv, gamma, theta, vega, delta]
