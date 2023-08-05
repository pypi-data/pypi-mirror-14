# coding=utf-8

class Calculadora:
    
    def __init__(self, opex=0, opey=0):
        self.asignar_x(opex)
        self.asignar_y(opey)
    
    def obtener_x(self):
        return self.x
    
    def asignar_x(self, valor):
        self.x = valor
        
    def obtener_y(self):
        return self.y
        
    def asignar_y(self, valor):
        self.y = valor
        
    def suma(self):
        return self.obtener_x() + self.obtener_y()
    
    def resta(self):
        return self.obtener_x() - self.obtener_y()
    
    def multiplicacion(self):
        return self.obtener_x() * self.obtener_y()

    def division(self):
        if self.y == 0:
            raise valueError("El segundo operando no debe ser 0.")
        
        return self.obtener_x() / self.obtener_y()
    
    
        
        

        
        
    
        