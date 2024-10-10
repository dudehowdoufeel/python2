class Circle:
    def __init__(self, radius=1.0, color="red"):
        self.__radius=radius  
        self.__color=color    #private

    def getRadius(self):
        return self.__radius

    def getArea(self):
        return 3.14 * (self.__radius**2)

circle1=Circle()
print("radius:", circle1.getRadius())  
print("area:", circle1.getArea())      

a = float(input("enter radius:"))
circle2 = Circle(a)

print("radius:", circle2.getRadius())  
print("area:", circle2.getArea())     
