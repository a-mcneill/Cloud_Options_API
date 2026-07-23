""" Options Pricing Model:
    The purpose of this program is to provide an options pricing model, using the Black-Scholes formula to price European call and put options."""

import math
from scipy.stats import norm

def black_scholes_prices(S, K, T, r, sigma, option_type):
    """
       Calculate the Black-Scholes price for a European option.

       Parameters:
       S = current stock price
       K = strike price of option
       T = time to maturity (years)
       r = risk-free interest rate (annualised)
       sigma = Volatility of the stock (standard deviation of returns)
       option_type = call or put
       
       Returns: float - Option price
    
    """

    # calculate d1 & d2 

    # these reflect how far 'in the money' the option is, adjusted for time and volatility

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    
    # calculate option price 

    # norm.cdf(d1 or d2) provide probability of option finishing in the money

    #  discount strike using math.exp(-r, T) to account for time value of money

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

    elif option_type == 'put':
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    else:
        raise ValueError("option_type must be 'call' or 'put'.")
    
    return price
    

# calculate the Greeks

def black_scholes_greeks(S, K, T, r, sigma, option_type):
    """ The purpose of this function is to calculate the Greeks for an option, as detailed by the user's input.
    
        Parameters:
       S = current stock price
       K = strike price of option
       T = time to maturity (years)
       r = risk-free interest rate (annualised)
       sigma = Volatility of the stock (standard deviation of returns)
       option_type = call or put
       
       Returns: dictionary - containing Delta, Gamma, Vega, Theta, and Rho results
    
    """

    # calculate d1 & d2

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    # calculate Delta
        # measures how much the option price changes for a $1 change in the stock price

    delta = norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) -1

        # for a call, delta is between 0 and 1; for a put, delta is between -1 and 0

    # calculate Gamma
        # the rate of change of delta

    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))

        # same for call and puts; high gamma means delta is sensitive to changes in the stock price

    # calculate Vega
        # measures the sensitivity to volatility -> expressed as a percentage

    vega = S * norm.pdf(d1) * math.sqrt(T) / 100

        # a 1% increase in volatility changes the option price by approximately the vega


    # calculate Theta
        # measures the time decay; how much value the option loses each day -> usually negative for short-term options

    theta_call = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365

    theta = theta_call if option_type == 'call' else theta_put


    # calculate Rho
        # measures the sensitivity to the interest rate changes; more relevant for long-dated options -> divided by 100 to express per 1% change in interest rate

    rho_call = K * T * math.exp(-r * T) * norm.cdf(d2) / 100
    rho_put = -K * T * math.exp(-r * T) * norm.cdf(-d2) / 100

    rho = rho_call if option_type == 'call' else rho_put


    # return the results of Greeks

    return {
        'Delta': delta,
        'Gamma': gamma,
        'Vega': vega,
        'Theta': theta,
        'Rho': rho
    }


