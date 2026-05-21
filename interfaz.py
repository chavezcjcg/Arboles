import tkinter as tk
from tkinter import messagebox, filedialog
import json
from modelos import ArbolBST, ArbolAvl, ArbolBinario, Nodo, contar_nodos, obtener_preorden, obtener_inorden, obtener_postorden

class AplicacionArboles:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Educativo de Árboles")
        self.root.geometry("1280x720")
        
        # se inicia con el arbol binario
        self.tipo_arbol = tk.StringVar(value="BINARIO")
        self.arbol = ArbolBinario()
        
        self.crear_interfaz()


    def crear_interfaz(self):
        panel_control = tk.Frame(self.root, width=250, bg="#f0f0f0", padx=10, pady=10)
        panel_control.pack(side=tk.LEFT, fill=tk.Y)

        # seleccionar el tipo de arbol
        tk.Label(panel_control, text="Tipo de Árbol:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Radiobutton(panel_control, text="Árbol Binario", variable=self.tipo_arbol, value="BINARIO", command=self.cambiar_arbol, bg="#f0f0f0").pack(anchor=tk.W)
        tk.Radiobutton(panel_control, text="Binario de Búsqueda (BST)", variable=self.tipo_arbol, value="BST", command=self.cambiar_arbol, bg="#f0f0f0").pack(anchor=tk.W)
        tk.Radiobutton(panel_control, text="Árbol AVL", variable=self.tipo_arbol, value="AVL", command=self.cambiar_arbol, bg="#f0f0f0").pack(anchor=tk.W)
        
        # entradas
        tk.Label(panel_control, text="Valor del Nodo:", bg="#f0f0f0").pack(pady=(15, 0))
        self.entry_valor = tk.Entry(panel_control)
        self.entry_valor.pack(pady=5)

        # botones
        tk.Button(panel_control, text="Insertar", command=self.insertar_nodo, width=20, bg="#d4edda").pack(pady=2)
        tk.Button(panel_control, text="Buscar", command=self.buscar_nodo, width=20, bg="#cce5ff").pack(pady=2)
        tk.Button(panel_control, text="Eliminar", command=self.eliminar_nodo, width=20, bg="#f8d7da").pack(pady=2)
        
        # botones de recorridos
        tk.Label(panel_control, text="Recorridos:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        tk.Button(panel_control, text="Preorden", command=lambda: self.mostrar_recorrido("pre"), width=20).pack(pady=2)
        tk.Button(panel_control, text="Inorden", command=lambda: self.mostrar_recorrido("in"), width=20).pack(pady=2)
        tk.Button(panel_control, text="Postorden", command=lambda: self.mostrar_recorrido("post"), width=20).pack(pady=2)

        # Guardar / Cargar
        tk.Label(panel_control, text="Archivos:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        tk.Button(panel_control, text="Guardar Árbol", command=self.guardar_arbol, width=20).pack(pady=2)
        tk.Button(panel_control, text="Cargar Árbol", command=self.cargar_arbol, width=20).pack(pady=2)

        # informacion del arbol
        self.lbl_info = tk.Label(panel_control, text="Nodos: 0 | Raíz: Ninguna\nAltura: 0", bg="#f0f0f0", justify=tk.LEFT)
        self.lbl_info.pack(pady=20)

        # apartado de dibujo
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    #reinicia el arbol actual segun la seleccion 
    def cambiar_arbol(self):
        if self.tipo_arbol.get() == "BINARIO":
            self.arbol = ArbolBinario()
        elif self.tipo_arbol.get() == "BST":
            self.arbol = ArbolBST()
        elif self.tipo_arbol.get() == "AVL":
            self.arbol = ArbolAvl()
        self.dibujar_arbol()

    def obtener_valor(self):
        try:
            valor = int(self.entry_valor.get())
            self.entry_valor.delete(0, tk.END)
            return valor
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número entero válido.")
            return None

    def insertar_nodo(self):
        valor = self.obtener_valor()
        if valor is not None:
            self.arbol.insertar(valor)
            self.dibujar_arbol()

    def eliminar_nodo(self):
        if self.tipo_arbol.get() == "BINARIO":
            messagebox.showinfo("Aviso", "La eliminación no está implementada para el Árbol Binario.")
            return
            
        valor = self.obtener_valor()
        if valor is not None:
            self.arbol.eliminar(valor)
            self.dibujar_arbol()

    def buscar_nodo(self):
        if self.tipo_arbol.get() == "BINARIO":
            messagebox.showinfo("Aviso", "La búsqueda interactiva no está implementada para el Árbol Binario.")
            return
            
        valor = self.obtener_valor()
        if valor is not None:
            nodo, camino = self.arbol.buscar(valor)
            if nodo:
                messagebox.showinfo("Búsqueda", f"Valor {valor} encontrado.\nCamino recorrido: {camino}")
                self.dibujar_arbol(camino_resaltado=camino)
            else:
                messagebox.showwarning("Búsqueda", f"El valor {valor} no existe en el árbol.\nCamino intentado: {camino}")
                self.dibujar_arbol(camino_resaltado=camino)

    def mostrar_recorrido(self, tipo):
        if not self.arbol.raiz:
            messagebox.showinfo("Recorrido", "El árbol está vacío.")
            return
        
        resultado = []
        if tipo == "pre":
            resultado = obtener_preorden(self.arbol.raiz)
            nombre = "Preorden"
        elif tipo == "in":
            resultado = obtener_inorden(self.arbol.raiz)
            nombre = "Inorden"
        elif tipo == "post":
            resultado = obtener_postorden(self.arbol.raiz)
            nombre = "Postorden"
            
        messagebox.showinfo(f"Recorrido {nombre}", f"Orden de visita:\n{resultado}")

    # parte de visualizacion del arbol
    def dibujar_arbol(self, camino_resaltado=None):
        self.canvas.delete("all")
        if self.arbol.raiz:
            self.root.update_idletasks()
            ancho_canvas = self.canvas.winfo_width()
        
            if ancho_canvas <= 1:
                ancho_canvas = 1030 
                
            x_centro = ancho_canvas // 2
            self._dibujar_nodo(self.arbol.raiz, x=x_centro, y=50, dx=200, camino_resaltado=camino_resaltado)
        self.actualizar_info()

    def _dibujar_nodo(self, nodo, x, y, dx, camino_resaltado):
        if nodo is None:
            return

        # dubujo de las conexiones de raiz a hijo
        if nodo.izq:
            self.canvas.create_line(x, y, x - dx, y + 60, fill="gray")
            self._dibujar_nodo(nodo.izq, x - dx, y + 60, dx / 1.5, camino_resaltado)
        if nodo.der:
            self.canvas.create_line(x, y, x + dx, y + 60, fill="gray")
            self._dibujar_nodo(nodo.der, x + dx, y + 60, dx / 1.5, camino_resaltado)

        color_fondo = "red" if camino_resaltado and nodo.valor in camino_resaltado else "lightblue"

        # figura del nodo
        r = 15
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color_fondo, outline="black")
        self.canvas.create_text(x, y, text=str(nodo.valor), font=("Arial", 10, "bold"))

        # Visualizar balances para el arbol avl
        if self.tipo_arbol.get() == "AVL":
            try:
                balance = self.arbol.obtener_balance(nodo)
                self.canvas.create_text(x + 25, y - 15, text=f"B:{balance}", font=("Arial", 8), fill="red")
            except AttributeError:
                pass

    def actualizar_info(self):
        nodos = contar_nodos(self.arbol.raiz)
        raiz_val = self.arbol.raiz.valor if self.arbol.raiz else "Ninguna"
        
        def altura_recursiva(n):
            if not n: return 0
            return 1 + max(altura_recursiva(n.izq), altura_recursiva(n.der))
        
        altura = altura_recursiva(self.arbol.raiz)
        self.lbl_info.config(text=f"Nodos: {nodos} | Raíz: {raiz_val}\nAltura del Árbol: {altura}")

    # apartado de guardado y carga de los arboles.

    def guardar_arbol(self):
        if not self.arbol.raiz:
            messagebox.showwarning("Advertencia", "El árbol está vacío.")
            return
            
        def nodo_a_dict(nodo):
            if not nodo:
                return None
            return {
                "valor": nodo.valor,
                "izq": nodo_a_dict(nodo.izq),
                "der": nodo_a_dict(nodo.der)
            }
            
        datos = {
            "tipo": self.tipo_arbol.get(),
            "estructura": nodo_a_dict(self.arbol.raiz)
        }
        
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if filepath:
            with open(filepath, "w") as file:
                json.dump(datos, file, indent=4)
            messagebox.showinfo("Éxito", "Árbol guardado correctamente.")

    def cargar_arbol(self):
        filepath = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if filepath:
            with open(filepath, "r") as file:
                datos = json.load(file)
            
            tipo = datos.get("tipo", "BST")
            self.tipo_arbol.set(tipo)
            self.cambiar_arbol()
            
            def dict_a_nodo(d):
                if d is None: return None
                n = Nodo(d["valor"])
                n.izq = dict_a_nodo(d.get("izq"))
                n.der = dict_a_nodo(d.get("der"))
                return n
                
            self.arbol.raiz = dict_a_nodo(datos.get("estructura"))
            
            if tipo == "AVL":
                def recalcular_alturas(nodo):
                    if not nodo: return
                    recalcular_alturas(nodo.izq)
                    recalcular_alturas(nodo.der)
                    self.arbol.actualizar_altura(nodo)
                recalcular_alturas(self.arbol.raiz)

            self.dibujar_arbol()
            messagebox.showinfo("Éxito", "Árbol cargado correctamente.")
