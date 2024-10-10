from author import Author 

class Book:
    def __init__(self, name, author, price, qty=0):
        self.__name = name            
        self.__author = author       
        self.__price = price          
        self.__qty = qty              

    def getName(self):
        return self.__name
    def getAuthor(self):
        return self.__author
    def getPrice(self):
        return self.__price
    def setPrice(self, price):
        self.__price = price
    def getQty(self):
        return self.__qty
    def setQty(self, qty):
        self.__qty = qty
    def toString(self):
        author_info = self.__author.toString() 
        return f"Book[name={self.__name}, {author_info}, price={self.__price}, qty={self.__qty}]"



if __name__ == "__main__":
    author = Author(name="Miya Carablemish", email="miya_cara@gmail.com", gender="f")
    book_name = input("enter book: ")
    price = float(input("enter price: "))
    qty = int(input("enter qty:") or 0)

    book = Book(name=book_name, author=author, price=price, qty=qty)
    print(book.toString())
