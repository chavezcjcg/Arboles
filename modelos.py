class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 0  

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        nuevo = Nodo(valor)
        if not self.raiz:
            self.raiz = nuevo
            return
        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            if not actual.izq:
                actual.izq = nuevo
                break
            else:
                cola.append(actual.izq)
                
            if not actual.der:
                actual.der = nuevo
                break
            else:
                cola.append(actual.der)
class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar(valor, self.raiz)
    def _insertar(self, valor, nodo):
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar(valor, nodo.izq)
        elif valor > nodo.valor:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar(valor, nodo.der)
        return nodo
    def buscar(self, valor):
        return self._buscar(self.raiz, valor, [])
    def _buscar(self, nodo, valor, camino):
        if not nodo:
            return None, camino
        camino.append(nodo.valor)
        if nodo.valor == valor:
            return nodo, camino
        if valor < nodo.valor:
            return self._buscar(nodo.izq, valor, camino)
        return self._buscar(nodo.der, valor, camino)
    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)
    def _eliminar(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq
            else:
                sucesor = self._minimo(nodo.der)
                nodo.valor = sucesor.valor
                nodo.der = self._eliminar(nodo.der, sucesor.valor)
        return nodo
    def _minimo(self, nodo):
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

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
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self.raiz = self._insertar(valor, self.raiz)
    def _insertar(self, valor, nodo):
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                nodo.izq = self._insertar(valor, nodo.izq)
        elif valor > nodo.valor:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                nodo.der = self._insertar(valor, nodo.der)
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
    def buscar(self, valor):
        return self._buscar(self.raiz, valor, [])
    def _buscar(self, nodo, valor, camino):
        if not nodo:
            return None, camino
        camino.append(nodo.valor)
        if nodo.valor == valor:
            return nodo, camino
        if valor < nodo.valor:
            return self._buscar(nodo.izq, valor, camino)
        return self._buscar(nodo.der, valor, camino)
    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)
    def _eliminar(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq
            else:
                sucesor = self._minimo(nodo.der)
                nodo.valor = sucesor.valor
                nodo.der = self._eliminar(nodo.der, sucesor.valor)
        if nodo is None:
            return nodo
        self.actualizar_altura(nodo)
        balance = self.obtener_balance(nodo)
        if balance < -1 and self.obtener_balance(nodo.izq) <= 0:
            return self.rotar_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.izq) > 0:
            nodo.izq = self.rotar_izquierda(nodo.izq)
            return self.rotar_derecha(nodo)
        if balance > 1 and self.obtener_balance(nodo.der) >= 0:
            return self.rotar_izquierda(nodo)
        if balance > 1 and self.obtener_balance(nodo.der) < 0:
            nodo.der = self.rotar_derecha(nodo.der)
            return self.rotar_izquierda(nodo)
        return nodo
    def _minimo(self, nodo):
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

def obtener_preorden(nodo, lista=None):
    if lista is None: lista = []
    if nodo:
        lista.append(nodo.valor)
        obtener_preorden(nodo.izq, lista)
        obtener_preorden(nodo.der, lista)
    return lista

def obtener_inorden(nodo, lista=None):
    if lista is None: lista = []
    if nodo:
        obtener_inorden(nodo.izq, lista)
        lista.append(nodo.valor)
        obtener_inorden(nodo.der, lista)
    return lista

def obtener_postorden(nodo, lista=None):
    if lista is None: lista = []
    if nodo:
        obtener_postorden(nodo.izq, lista)
        obtener_postorden(nodo.der, lista)
        lista.append(nodo.valor)
    return lista

def contar_nodos(nodo):
    if not nodo:
        return 0
    return 1 + contar_nodos(nodo.izq) + contar_nodos(nodo.der)