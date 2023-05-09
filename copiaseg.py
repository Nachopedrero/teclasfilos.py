import tkinter as tk
import time
import random
import threading

N = 5
TIEMPO_TOTAL = 3

class Filosofo(threading.Thread):
    semaforo = threading.Lock()
    estado = []
    tenedores = []
    count = 0
    
    def __init__(self, ventana):
        super().__init__()
        self.id = Filosofo.count
        Filosofo.count += 1
        Filosofo.estado.append('PENSANDO')
        Filosofo.tenedores.append(threading.Semaphore(0))
        self.boton = tk.Button(ventana, text=f"Filósofo {self.id}", state=tk.DISABLED)
        self.boton.pack()
        self.ventana = ventana
    def __del__(self):
        self.boton.destroy()

    def cambiar_estado(self):
        estado_actual = Filosofo.estado[self.id]
        if estado_actual == 'PENSANDO':
            self.boton.configure(bg='green')
        elif estado_actual == 'HAMBRIENTO':
            self.boton.configure(bg='yellow')
            print(f"Filósofo {self.id} está HAMBRIENTO")
        elif estado_actual == 'COMIENDO':
            self.boton.configure(bg='red')

    def pensar(self):
        time.sleep(random.randint(0, 5))

    def derecha(self, i):
        return (i - 1) % N

    def izquierda(self, i):
        return (i + 1) % N

    def verificar(self, i):
        if Filosofo.estado[i] == 'HAMBRIENTO' and Filosofo.estado[self.izquierda(i)] != 'COMIENDO' and Filosofo.estado[self.derecha(i)] != 'COMIENDO':
            Filosofo.estado[i] = 'COMIENDO'
            Filosofo.tenedores[i].release()

    def tomar(self):
        Filosofo.semaforo.acquire()
        Filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id)
        Filosofo.semaforo.release()
        Filosofo.tenedores[self.id].acquire()
        print("FILOSOFO {} hambriento".format(self.id))
        self.boton.configure(bg= "red")

        self.ventana.update()
    def soltar(self):
        Filosofo.semaforo.acquire()
        Filosofo.estado[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        Filosofo.semaforo.release()
        print("FILOSOFO {} pensando".format(self.id))
        self.boton.configure(bg="yellow")

        self.ventana.update()

    def comer(self):
        print("FILOSOFO {} COMIENDO".format(self.id))
        time.sleep(2)  # Tiempo arbitrario para comer
        print("FILOSOFO {} TERMINO DE COMER".format(self.id))
        
        self.boton.configure(bg="green")
    
    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar()
            self.tomar()
            self.comer()
            self.soltar()
            self.cambiar_estado()


def main():
    ventanaf = tk.Tk()
    ventanaf.title("Filósofos")
    etiqueta_comiendo = tk.Label(ventanaf, text="Rojo: Comiendo", fg="red")
    etiqueta_comiendo.pack()

# Etiqueta para indicar que el color verde significa que está esperando los palillos
    etiqueta_esperando = tk.Label(ventanaf, text="Verde: Esperando los palillos", fg="green")
    etiqueta_esperando.pack()
    

    filosofos = []
    for i in range(N):
        filosofo = Filosofo(ventanaf)
        filosofos.append(filosofo)

    for f in filosofos:
        f.start()

    ventanaf.mainloop()






# Llamar a la función para agregar la terminal


# Agregar otros elementos a la ventana principal

main()
