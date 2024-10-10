class Rectangle:
    def __init__(self, length=1.0, width=1.0):
        self.__length = length  
        self.__width = width    
    def getLength(self):
        return self.__length
    def setLength(self, length):          #can add extra check
        self.__length = length
    def getWidth(self):
        return self.__width
    def setWidth(self, width):
        self.__width = width
    def getArea(self):
        return self.__length * self.__width
    def getPerimeter(self):
        return 2 * (self.__length + self.__width)
    def toString(self):
        return f"Rectangle[length={self.__length}, width={self.__width}]"


rectangle1 = Rectangle() 
print(rectangle1.toString()) 
print(f"area: {rectangle1.getArea()}")         
print(f"perimeter: {rectangle1.getPerimeter()}")  

a = float(input("enter a: "))  
b = float(input("enter b: "))  

rectangle1.setLength(a) 
rectangle1.setWidth(b)    

print(rectangle1.toString())  
print(f"area: {rectangle1.getArea()}")        
print(f"perimeter: {rectangle1.getPerimeter()}")  
