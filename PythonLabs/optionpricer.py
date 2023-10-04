# Importing libraries
from numpy import *
from scipy.stats import norm

class BS:
    
    """
    This is a class for options contract for pricing european options on stocks without dividends.
    
    Attributes:
        spot        : int or float
        strike      : int or float
        rate        : float
        dte         : int or float [days to expiration in number os years]
        volatility  : float
    """
    
    def __init__(self, spot, strike, rate, dte, volatility):
        
        # Spot price
        self.spot = spot
        
        # Option strike
        self.strike = strike
        
        # Interest rate
        self.rate = rate
        
        # Days to Expire
        self.dte = dte
        
        # Volatility
        self.volatility = volatility
        
        # Utility
        self._a_ = self.volatility * self.dte**0.5
        
        if self.strike == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            self._d1_ = (log(self.spot / self.strike) + (self.rate + (self.volatility**2)/2)*self.dte) / self._a_
            
        self._d2_ = self._d1_ - self._a_
        
        self._b_ = e**-(self.rate * self.dte)
        
        # The __dict__ attribute
        """
        Contains all the attributes defined for the object itself. It maps the attribute name to its value
        """
        
        for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', 'callTheta', 'putTheta', 
                  'callRho', 'putRho', 'vega', 'gamma']:
            self.__dict__[i] = None
        
        [self.callPrice, self.putPrice] = self._price
        [self.callDelta, self.putDelta] = self._delta
        [self.callTheta, self.putTheta] = self._theta
        [self.callRho, self.putPrice] = self._rho
        self.vega = self._vega
        self.gamma = self._gamma
    
        
    # Option price
    @property
    def _price(self):
        """
        Returns the option price: [Call price, Put price]
        """      
        
        if self.volatility == 0 or self.dte == 0:
            call = maximum(0.0, self.spot - self.strike)
            put = maximum(0.0, self.strike - self.spot)
        else:
            call = self.spot * norm.cdf(self._d1_) - self.strike * e **(-self.rate * self.dte)*norm.cdf(self._d2_)
            put = self.strike * e**(-self.rate * self.dte) * norm.cdf(-self._d2_) - self.spot * norm.cdf(-self._d1_)
            
        return [call, put]
    
    # Option delta
    @property
    def _delta(self):
        """
        Returns the option delta: [Call delta, Put delta]
        """
        
        if self.volatility == 0 or self.dte == 0:
            call = 1.0 if self.spot > self.strike else 0.0
            put = -1.0 if self.spot < self.strike else 0.0
        else:
            call = norm.cdf(self._d1_)
            put = -norm.cdf(-self._d1_)
        
        return [call, put]
    
    # Option gamma
    @property
    def _gamma(self):
        """
        Returns the option gamma
        """        
        return norm.pdf(self._d1_) / (self.spot * self._a_)
    
    # Option vega
    @property
    def _vega(self):
        """
        Returns the option vega
        """
        if self.volatility == 0 or self.dte == 0:
            return 0.0
        else:
            return self.spot * norm.pdf(self._d1_) * self.dte**0.5 / 100
        
    # Option theta
    @property
    def _theta(self):
        """
        Returns the option theta: [Call theta, Put theta]
        """
        call = -self.spot * norm.pdf(self._d1_) * self.volatility / (2 * self.dte**0.5) - \
            self.rate * self.strike * self._b_ * norm.cdf(self._d2_)
            
        put = -self.spot * norm.pdf(self._d1_) * self.volatility / (2 * self.dte**0.5) - \
            self.rate * self.strike * self._b_ * norm.cdf(-self._d2_)
            
        return [call/365, put/365]
        
    # Option rho
    @property
    def _rho(self):
        """
        Returns the option rho: [Call rho, Put rho]
        """
        call = self.strike * self.dte * self._b_ * norm.cdf(self._d2_) / 100
        put = -self.strike * self.dte * self._b_ * norm.cdf(-self._d2_) / 100
        
        return [call, put]