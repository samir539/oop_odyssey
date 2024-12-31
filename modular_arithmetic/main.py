## class to implement basic modular arithmetic operations
from numbers import Integral
from functools import total_ordering
import operator

@total_ordering
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

    def __repr__(self):
        return f"Mod({self.value},{self.mod})"

    def __eq__(self,other):
        """implement mod congruency"""
        if isinstance(other, Mod) and self.mod == other.mod:
            return self.value == other.value
        elif isinstance(other, Integral):
            # a is congruent to b mod n  if n | (a-b)
            return other%self.mod == self.value
        return False 
    
    def __hash__(self):
        return hash((self.mod, self.value))
    
    def __int__(self):
        return self.value 
    
    def __lt__(self,other):
        if isinstance(other,Mod) and self.mod == other.mod:
            return self.value < other.value
        if isinstance(other,int):
            return self.value < other % self.mod

    def _operation(self, other, op,inplace=False):
        if isinstance(other,Mod) and self.mod == other.mod:
            val = other.value
            if inplace:
                self.value  = op(self.value, val)
                return self 
            output = op(self.value,val)
            return Mod(output,self.mod)
        elif isinstance(other, int):
            val = other % self.mod 
            output = op(self.value, val)
            if inplace:
                self.value = op(self.value,val)
                return self 
            return Mod(output,self.mod)
            

    #operators 
    def __add__(self, other):
        return self._operation(other, operator.add)
            
    def __sub__(self,other):
        return self._operation(other, operator.sub)
        
    def __mul__(self,other):
        return self._operation(other, operator.mul)

    def __pow__(self,other):
        return self._operation(other, operator.pow)

    def __iadd__(self,other):
        return self._operation(other, operator.add, inplace=True)

    def __isub__(self,other):
        return self._operation(other, operator.sub, inplace=True)

    def __imul__(self,other):
        return self._operation(other, operator.sub, inplace=True)
            
    def __ipow__(self,other):
        return self._operation(other, operator.pow, inplace=True)

    

if __name__ == "__main__":
    print(Mod(3,12) == Mod(15,12))
    print(Mod(3,11) + Mod(5,11))
    myMod = Mod(3,10)
    myMod2 = Mod(11,10)
    print(int(myMod))
    myVal = 24
    val  = hash(myMod)
    val2 = hash(myMod2)
    print(hex(id(val)),hex(id(val2)))
    print(myVal == myMod)
    print(myMod.__dict__)