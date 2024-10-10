class Time:
    def __init__(self, hour=13, minute=59, second=59):
        self.__hour = hour      
        self.__minute = minute 
        self.__second = second  
    def getHour(self):
        return self.__hour
    def getMinute(self):
        return self.__minute
    def getSecond(self):
        return self.__second
    def setHour(self, hour):
        self.__hour = hour
    def setMinute(self, minute):
        self.__minute = minute
    def setSecond(self, second):
        self.__second = second


    def toString(self):
        return f"{self.__hour:02}:{self.__minute:02}:{self.__second:02}"
    
    def nextSecond(self):
        self.__second += 1
        if self.__second == 60:
            self.__second = 0
            self.__minute += 1
            if self.__minute == 60:
                self.__minute = 0
                self.__hour += 1
                if self.__hour == 24:
                    self.__hour = 0
        return self

    def previousSecond(self):
        self.__second -= 1
        if self.__second < 0:
            self.__second = 59
            self.__minute -= 1
            if self.__minute < 0:
                self.__minute = 59
                self.__hour -= 1
                if self.__hour < 0:
                    self.__hour = 23
        return self

time1 = Time() 
print("real time: ", time1.toString())

time1.previousSecond()     
print("previous second: ", time1.toString())  

time1.nextSecond()         
time1.nextSecond()       
print("next second: ", time1.toString()) 
