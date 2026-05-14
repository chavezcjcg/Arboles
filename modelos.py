class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 0

class ArbolAvl:
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        if not nodo:
            return -1
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.der) - self.obtener_altura(nodo.izq)

    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.obtener_altura(nodo.izq), self.obtener_altura(nodo.der))

    def rotar_derecha(self, z):
        y = z.izq
        T3 = y.der
        y.der = z
        z.izq = T3
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        return y

    def rotar_izquierda(self, z):
        y = z.der
        T2 = y.izq
        y.izq = z
        z.der = T2
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        return y

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if not nodo:
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izq = self._insertar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._insertar(nodo.der, valor)
        else:
            return nodo 

        self.actualizar_altura(nodo)
        balance = self.obtener_balance(nodo)
        if balance < -1 and valor < nodo.izq.valor:
            return self.rotar_derecha(nodo)
        if balance > 1 and valor > nodo.der.valor:
            return self.rotar_izquierda(nodo)
        if balance < -1 and valor > nodo.izq.valor:
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)
        if balance > 1 and valor < nodo.der.valor:
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)
        return nodo