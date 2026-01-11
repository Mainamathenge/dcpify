"""
Monte Carlo Option Pricing - Perfect for DCP Distribution
===========================================================
This workload simulates thousands of stock price paths to price financial options.
Each simulation is independent, making it ideal for distributed computing.

Computational Characteristics:
- CPU-intensive: Nested loops with mathematical operations
- Embarrassingly parallel: Each price point can be computed independently
- Scalable: Can easily scale from hundreds to millions of simulations
- Real-world application: Used in quantitative finance
"""

import numpy as np


def price_european_call_option(strike_price, num_simulations=10000):
    """
    Price a European call option using Monte Carlo simulation.
    
    This function is computationally expensive due to:
    1. Large number of random path simulations
    2. Nested loops for time-step evolution
    3. Statistical calculations across all paths
    
    Args:
        strike_price: The strike price of the option
        num_simulations: Number of Monte Carlo paths to simulate
    
    Returns:
        dict: Contains option price, standard error, and confidence interval
    """
    # Market parameters
    S0 = 100.0          # Initial stock price
    K = strike_price    # Strike price
    T = 1.0             # Time to maturity (1 year)
    r = 0.05            # Risk-free rate (5%)
    sigma = 0.2         # Volatility (20%)
    
    # Simulation parameters
    num_steps = 252     # Daily steps in a year
    dt = T / num_steps
    
    # Initialize array to store final payoffs
    payoffs = np.zeros(num_simulations)
    
    # Run Monte Carlo simulations
    for i in range(num_simulations):
        # Initialize stock price path
        S = S0
        
        # Simulate stock price path
        for step in range(num_steps):
            # Generate random shock
            z = np.random.standard_normal()
            
            # Update stock price using geometric Brownian motion
            S = S * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
        
        # Calculate payoff at maturity
        payoffs[i] = max(S - K, 0)
    
    # Discount payoffs to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    # Calculate standard error and confidence interval
    std_error = np.std(payoffs) / np.sqrt(num_simulations)
    confidence_interval = 1.96 * std_error * np.exp(-r * T)
    
    return {
        'strike_price': strike_price,
        'option_price': option_price,
        'std_error': std_error,
        'confidence_interval_95': confidence_interval,
        'num_simulations': num_simulations
    }


def calculate_greeks(strike_price, num_simulations=10000):
    """
    Calculate option Greeks (Delta, Gamma, Vega) using finite differences.
    
    This is even more computationally intensive as it requires multiple
    option pricing calculations with perturbed parameters.
    
    Args:
        strike_price: The strike price of the option
        num_simulations: Number of Monte Carlo paths per calculation
    
    Returns:
        dict: Contains all option Greeks
    """
    # Base parameters
    S0 = 100.0
    r = 0.05
    sigma = 0.2
    T = 1.0
    
    # Small perturbations for finite differences
    dS = 0.01 * S0
    dsigma = 0.01
    
    # Calculate base option price
    base_result = price_european_call_option(strike_price, num_simulations)
    base_price = base_result['option_price']
    
    # Calculate Delta (sensitivity to stock price)
    # This requires additional expensive simulations
    price_up = price_european_call_option(strike_price, num_simulations)['option_price']
    price_down = price_european_call_option(strike_price, num_simulations)['option_price']
    delta = (price_up - price_down) / (2 * dS)
    
    # Calculate Gamma (second derivative w.r.t. stock price)
    gamma = (price_up - 2 * base_price + price_down) / (dS ** 2)
    
    # Calculate Vega (sensitivity to volatility)
    vega = (price_up - price_down) / (2 * dsigma)
    
    return {
        'strike_price': strike_price,
        'option_price': base_price,
        'delta': delta,
        'gamma': gamma,
        'vega': vega,
        'num_simulations': num_simulations
    }


def price_asian_option(strike_price, num_simulations=10000):
    """
    Price an Asian option (payoff based on average price) using Monte Carlo.
    
    Asian options are path-dependent, requiring tracking of the entire price path,
    making them more computationally intensive than European options.
    
    Args:
        strike_price: The strike price of the option
        num_simulations: Number of Monte Carlo paths to simulate
    
    Returns:
        float: The estimated option price
    """
    # Market parameters
    S0 = 100.0
    K = strike_price
    T = 1.0
    r = 0.05
    sigma = 0.2
    
    # Simulation parameters
    num_steps = 252
    dt = T / num_steps
    
    payoffs = np.zeros(num_simulations)
    
    for i in range(num_simulations):
        S = S0
        price_sum = 0.0
        
        # Track entire price path
        for step in range(num_steps):
            z = np.random.standard_normal()
            S = S * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
            price_sum += S
        
        # Payoff based on average price
        average_price = price_sum / num_steps
        payoffs[i] = max(average_price - K, 0)
    
    # Discount to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    return {
        'strike_price': strike_price,
        'option_price': option_price,
        'option_type': 'Asian Call',
        'num_simulations': num_simulations
    }


# Example usage - this would be the input for dcpify
if __name__ == "__main__":
    # Price options at different strike prices
    strike_prices = [90, 95, 100, 105, 110]
    
    print("Pricing European Call Options...")
    for strike in strike_prices:
        result = price_european_call_option(strike, num_simulations=50000)
        print(f"Strike ${strike}: Price = ${result['option_price']:.4f} "
              f"± ${result['confidence_interval_95']:.4f}")
    
    print("\nPricing Asian Call Options...")
    for strike in strike_prices:
        result = price_asian_option(strike, num_simulations=50000)
        print(f"Strike ${strike}: Price = ${result['option_price']:.4f}")
