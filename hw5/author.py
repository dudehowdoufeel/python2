class Author:
    def __init__(self, name, email, gender):
        self.__name = name           
        self.__email = email         
        self.__gender = gender        

        if self.__gender not in ['m', 'f']:
            raise ValueError("gender must be 'm' or 'f'")

    def getName(self):
        return self.__name
    def getEmail(self):
        return self.__email
    def setEmail(self, email):
        self.__email = email
    def getGender(self):
        return self.__gender
    def toString(self):
        return f"author[name={self.__name}, email={self.__email}, gender={self.__gender}]"

author = Author(name="Miya Carablemish", email="miya_cara@gmail.com", gender="f")
print(author.toString())