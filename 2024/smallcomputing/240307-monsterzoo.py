# A demonstration of python classes, by creating a "monster zoo"
# Where each monster has it's own attributes and information

class food:
    def __init__(self, name: str, servingSize: float):
        self.name = name
        self.servingSize = servingSize
    
    def print(self):
        print(f"name: {self.name}, size: {str(self.servingSize)}")
        return f"name: {self.name}, size: {str(self.servingSize)}"

    def weight(self, servings: int = 1) -> float:
        return servings * self.servingSize


class date:
    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year
    
    def checkValid(self) -> bool:
        # Deal with user putting in day below zero (I think if someone does this its their fault if it doesnt work)
        if self.day <= 0:
            return False
        
        # Deal with stupid months
        if self.month <= 0 or self.month >= 12:
            return False
        
        # check if valid amount of days in month (months are 1 indexed but list is 0 indexed)
        if not self.day <= self.daysInMonth():
            return False
        
        if self.month == 2:  # Febuary is a bad month >:(
            if self.isLeapYear():
                if self.day > 29:
                    return False
            else:
                if self.day > 28:
                    return False
        
        return True
 

    def daysInMonth(self, month: int | None = None) -> int:
        monthDays = [31, 99, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # Return date of birthmonth if no month is specified
        if not month:
            return monthDays[self.month-1]
        else: # else return input
            return monthDays[month-1]
    

    def isLeapYear(self, year: int | None = None) -> bool:
        if not year: # if no year specified use own birthyear
            year = self.year
        
        if not year % 4 == 0:
            return False
        
        if year % 100 == 0 and not year % 400 == 0:
            return False
        
        return True
        
    def date(self) -> str:  # This is just to get a dd/mm/yyyy format for printing easily
        return f"{self.day}/{self.month}/{self.year}"
        
class monster:
    def __init__(self, name: str, birthday: date, nEyes: int, nLegs: int, canFly: bool,
                  favouriteFood: food, personality: str):
        self.name = name
        self.birthday = birthday
        self.nEyes = nEyes
        self.nLegs = nLegs
        self.canFly = canFly
        self.favouriteFood = favouriteFood
        self.amountEaten = 0
        self.personality = personality

    def eat(self, numServes: int) -> float:
        foodAmount = self.favouriteFood.weight(numServes)
        self.amountEaten += foodAmount
        return foodAmount
    
    def loseLimb(self) -> bool:
        if self.nLegs == 0:
            return False
        else:
            self.nLegs -= 1
            return True
    
    def loseEye(self) -> bool:
        if self.nEyes == 0:
            return False
        else:
            self.nEyes -= 1
            return True
    
    def print(self):
        # I really hate this indentation
        print(f"""Name: {self.name}
can fly: {self.canFly}
birthday: {self.birthday.date()}
Number of eyes: {self.nEyes}
Number of legs: {self.nLegs}
Favourite food: {self.favouriteFood.name} ({self.favouriteFood.servingSize})
amount eaten: {self.amountEaten}
personality: {self.personality}""")


class zoo:
    def __init__(self, maxCapacity: int):
        self.monsters = []
        self.numMonsters = 0
        self.maxCapacity = maxCapacity

    def add(self, newMonster: monster) -> bool:
        if self.numMonsters < self.maxCapacity:
            self.monsters.append(newMonster)
            self.numMonsters += 1
            return True
        
        return False
    
    def remove(self, name: str) -> bool:
        index = self.find(name)
        if index == -1: return False

        self.numMonsters -= 1
        self.monsters.pop(index)


    def find(self, name: str) -> int:
        for count, i in enumerate(self.monsters):
            if name == i.name:
                return count
        
        return -1
    
    def printMonster(self, name):
        index = self.find(name)
        if index == -1: print("No monster")

        self.monsters[index].print()

    def printAllMonsters(self):
        for i in self.monsters:
            i.print()


# DEMO

myZoo = zoo(5)

myZoo.add(monster("Jim", date(1, 1, 2000), 2, 4, True, food("apple", 2.8), "annoying"))
    
myZoo.printMonster("Jim")