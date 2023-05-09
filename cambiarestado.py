def cambiar_estado(self):
        estado_actual = Filosofo.estado[self.id]
        if estado_actual == 'PENSANDO':
            self.boton.configure(bg='green')
        elif estado_actual == 'HAMBRIENTO':
            self.boton.configure(bg='yellow')
        elif estado_actual == 'COMIENDO':
            self.boton.configure(bg='red')