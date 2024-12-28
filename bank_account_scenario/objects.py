from datetime import datetime, timezone, timedelta

class TimeHandling():
    tz = timezone.utc

    def __init__(self,offset, name):
        self._offset = offset
        self._name = name 

    @classmethod
    def get_utc_time(cls, now=False):
            return datetime.now(cls.tz)
        


    def get_time_in_locale(self, given_time_utc=None):
        tz = timezone(timedelta(hours=self._offset), self._name)
        if given_time_utc is not None:
            return f"{given_time_utc.astimezone(tz)} ({self._name})"
        return datetime.now(tz)


class ConfirmationCode:
    def __init__(self,transaction_type,account_number,transaction_count,time_handling,given_time=None):
        self.account_number = account_number
        self.transaction_code = transaction_type
        self.transaction_id = transaction_count
        self.time_now = time_handling.get_time_in_locale()
        self.time_utc_now = time_handling.get_utc_time()
        if given_time is not None:
            self.time = time_handling.get_time_in_locale(given_time)
            self.time_utc = given_time

    def __call__(self):
        time_processed = datetime.strftime(self.time_utc_now, "%Y%m%d%H%M%S")
        return f"{self.transaction_code}-{self.account_number}-{time_processed}-{self.transaction_id}" 
    


class Account():

    #class attributes
    monthly_interest_rate = 0.05
    transaction_count = 0 

    transaction_type_dict = {"WITHDRAW":"W", "DEPOSIT":"D", "INTEREST_DEPOSIT":"I", "DECLINED":"X"}

    def __init__(self, account_number,first_name,last_name,time_offset,time_offset_name):
        self._account_number = account_number
        self._first_name = first_name
        self._last_name = last_name
        self._balence = 0
        self._time_handling = TimeHandling(time_offset,time_offset_name)


    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter 
    def first_name(self,new_first_name):
        self._first_name = new_first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self._last_name = new_last_name

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def balence(self):
        return self._balence
    
    @balence.setter
    def balence(self, new_balence):
        if new_balence < 0:
            return "you cannot have a negative balence"
        self._balence = new_balence

    
    @classmethod
    def change_monthly_interest_rate(cls,new_rate):
        cls.monthly_interest_rate = new_rate

    def _generate_confirmation_code(self,transaction_type):
        generated_confirmation_code = ConfirmationCode(self.transaction_type_dict[transaction_type],self._account_number,self.transaction_count,self._time_handling)
        return generated_confirmation_code


    #public methods
    def deposit(self,value):
        self.transaction_count += 1 
        new_balence = self.balence + value
        if new_balence < 0:
            return "you cannot have a negative balence"
        self.balence = new_balence
        return self.balence, self._generate_confirmation_code("DEPOSIT")()

    def withdraw(self,value):
        self.transaction_count += 1 
        new_balence = self.balence - value
        if new_balence < 0:
            return "you cannot withdraw more money than you have"
        self.balence = new_balence 
        return self.balence, self._generate_confirmation_code("WITHDRAW")()

    def pay_interest(self):
        self.transaction_count += 1 
        self.balence += self.balence * self.monthly_interest_rate
        return self.balence, self._generate_confirmation_code("INTEREST_DEPOSIT")()

    def parse_confirmation_code(self,conformation_code):
        processed_confirmation_code = conformation_code.replace("-"," ").split()
        ### change time stamp 
        time = datetime.strptime(processed_confirmation_code[2], "%Y%m%d%H%M%S")
        res = {"transaction_type":processed_confirmation_code[0],"account_number":processed_confirmation_code[1],"timestamp":time,"transaction_count":processed_confirmation_code[3]}
        return ConfirmationCode(res["transaction_type"],res["account_number"],res["transaction_count"],self._time_handling,res["timestamp"])
        


if __name__ == "__main__":
    myAccount = Account(555,"myname","mylastname",1,"CET")
    print(myAccount.deposit(500))
    print(myAccount.deposit(1000))
    print(myAccount.balence)
    print(myAccount.pay_interest())
    print(myAccount.balence)
    print(myAccount.withdraw(1574))
    print(myAccount.balence)
    print(myAccount.withdraw(100))
    print(myAccount.balence)
    print(myAccount.transaction_count)
    out = myAccount.parse_confirmation_code('W-555-20241228203913-4')
    print(out.account_number,out.transaction_code,out.transaction_id,out.time,out.time_utc)






