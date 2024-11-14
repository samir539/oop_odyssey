## class to implement basic modular arithmetic operations
from numbers import Integral


class Mod:
    """class to implement basic modular arithmetic operations"""

    def __init__(self, value,mod):
        if self._validate_mod(mod):
            self._mod = mod 
        if self._validate_value(value):
            self._value = value % self.mod 


    @property
    def value(self):
        return self._value

    @property 
    def mod(self):
        return self._mod 

    def _validate_mod(self, mod_val):
        if isinstance(mod_val, Integral) and mod_val > 0:
            return True
        
    def _validate_value(self,value):
        if isinstance(value, Integral):
            return True 


myMod = Mod(10,3)
print(myMod.__dict__)