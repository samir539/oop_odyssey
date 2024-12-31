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

    
    def __eq__(self,other):
        """implement mod congruency"""
        if isinstance(other, Mod):
            return self.mod == other.mod 
        elif isinstance(other, Integral):
            # a is congruent to b mod n  if n | (a-b)
            return other%self.mod == self.value
        return False 
    
    def __hash__(self):
        return hash((self.mod, self._value))


if __name__ == "__main__":
    myMod = Mod(3,10)
    myMod2 = Mod(11,10)
    myVal = 24
    val  = hash(myMod)
    val2 = hash(myMod2)
    print(hex(id(val)),hex(id(val2)))
    print(myVal == myMod)
    print(myMod.__dict__)