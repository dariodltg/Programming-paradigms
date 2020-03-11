#Dario de la Torre Guinaldo T3 L7, Paradigmas de Programación
import gtk
import timeit

from random import randint
class Interfaz():
    def __init__(self):
        #Inicia el programa
        self.builder=gtk.Builder()
        self.builder.add_from_file('Buscaminas.glade')
        self.ventana_menu=self.builder.get_object('ventana_menu')
        self.ventana_tablero=self.builder.get_object('ventana_tablero')
        self.ventana_abrir_fichero=self.builder.get_object('ventana_abrir_fichero')
        self.boton_principiante=self.builder.get_object('boton principiante')
        self.boton_intermedio=self.builder.get_object('boton_intermedio')
        self.boton_experto=self.builder.get_object('boton_experto')
        self.boton_leer_fichero=self.builder.get_object('boton_leer_fichero')
        self.boton_abrir_marcar=self.builder.get_object('boton_abrir_marcar')
        self.etiqueta_numero_marcas=self.builder.get_object('etiqueta_numero_marcas')
        self.etiqueta_numero_minas_sin_marcar=self.builder.get_object('etiqueta_numero_minas_sin_marcar')
        self.etiqueta_cronometro=self.builder.get_object('etiqueta_cronometro')
        self.etiqueta_informacion=self.builder.get_object('etiqueta_informacion')
        self.lienzo=self.builder.get_object('lienzo')
        self.builder.connect_signals(self)
        self.ventana_menu.show()
        self.ventana_tablero.hide()
        self.celdas=()
    def seleccionar_principiante(self,widget):
        self.juego = Modo(9,9,10,False)
        self.inicio_juego()
    def seleccionar_intermedio(self,widget):
        self.juego = Modo(16,16,40,False)
        self.inicio_juego()
    def seleccionar_experto(self,widget):
        self.juego = Modo(16,30,99,False)
        self.inicio_juego()
    def seleccionar_fichero(self,widget):
        fichero=self.boton_leer_fichero.get_file()
        nombre=fichero.get_basename()
        f = open(nombre)
        self.cadena=f.read()
        cadena1 = self.cadena.split("\n")
        cadena2 = cadena1[0].split(" ")
        filas = cadena2[0]
        columnas = cadena2[1]
        filas = int(filas)
        columnas = int(columnas)
        minas = 0
        for posicion in range(0, len(self.cadena)):
            if self.cadena[posicion] == "*":
                minas = minas + 1
        self.juego=Modo(filas,columnas,minas,True)
        self.inicio_juego()
        return None
    def cerrar_ventana(self,widget,event):
        #Cierra el programa
        gtk.main_quit()
        return gtk.FALSE
    
    def inicio_juego(self):
        #Cada vez que se inicie una nueva partida
        for i in range(len(self.celdas)):
            self.lienzo.remove(self.celdas[i])
        self.primera_jugada=True           
        self.marcar=False
        self.numero_marcas=0
        self.minas_restantes=self.juego.minas
        self.boton_abrir_marcar.set_label("Abrir")
        #Si es tablero aleatorio
        if self.juego.fichero is False:
            self.matriz_de_juego=self.juego.generar_tablero()        
        #Si es tablero de fichero
        elif self.juego.fichero is True:
            self.matriz_de_juego=self.juego.generar_tablero_fichero(self.cadena)
        self.ventana_menu.hide()
        self.ventana_tablero.show()
        self.etiqueta_informacion.set_label("")
        self.etiqueta_numero_marcas.set_label("Celdas marcadas: "+str(self.numero_marcas))
        self.etiqueta_numero_minas_sin_marcar.set_label("Minas restantes: "+str(self.minas_restantes))
        for i in range(self.juego.fil):
            for j in range(self.juego.col):
                self.matriz_de_juego[i][j].detectar_minas_alrededor(self.matriz_de_juego)
                self.celda=gtk.Button()
                if i%2==0:
                    self.lienzo.put(self.celda, 40*j+20, 40*i)
                if i%2==1:
                    self.lienzo.put(self.celda, 40*j, 40*i)
                self.imagen_celda_cerrada=gtk.Image()
                self.imagen_celda_cerrada.set_from_file('hexagonocerrado.png')
                self.celda.set_image(self.imagen_celda_cerrada)
                self.celda.show()
                self.celda.set_alignment(i,j)
        self.celdas=self.lienzo.get_children()
        for i in range(len(self.celdas)):
            self.celdas[i].connect("clicked", self.celda_clicked)
        #Iniciar el cronometro
        self.iniciar_cronometro = timeit.default_timer()
        return None
    
    def celda_clicked(self,widget):
        #Cada vez que se realice una jugada
        self.mina_descubierta=False
        self.etiqueta_informacion.set_label("")
        self.parar_cronometro = timeit.default_timer() - self.iniciar_cronometro
        self.animar()
        for i in range(len(self.celdas)):
            if self.celdas[i] == widget:
                coordenadas=self.celdas[i].get_alignment()
                coordenadax=int(coordenadas[0])
                coordenaday=int(coordenadas[1])
                if self.marcar is False: #Si esta en modo abrir casilla
                    if  self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is False:
                        self.matriz_de_juego[coordenadax][coordenaday].esta_abierta=True
                        if self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==0:
                            self.matriz_de_juego[coordenadax][coordenaday].abrir_recursivamente(self.matriz_de_juego)   
                    elif self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is True:
                        self.etiqueta_informacion.set_label("No se puede abrir una celda marcada")
                if self.marcar is True: #Si esta en modo marcar casilla
                        if self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is True:
                            self.etiqueta_informacion.set_label("No se puede marcar una celda abierta")
                        elif self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is False:
                            if self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is False:
                                if self.numero_marcas<self.juego.minas:
                                    self.matriz_de_juego[coordenadax][coordenaday].tiene_marca=True
                                    self.numero_marcas=self.numero_marcas+1
                                    self.minas_restantes=self.minas_restantes-1
                                elif self.numero_marcas==self.juego.minas:
                                    self.etiqueta_informacion.set_label("No se pueden marcar mas celdas")
                            elif self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is True:
                                self.matriz_de_juego[coordenadax][coordenaday].tiene_marca=False
                                self.numero_marcas=self.numero_marcas-1
                                self.minas_restantes=self.minas_restantes+1
                #Actualizar las etiquetas
                self.etiqueta_numero_marcas.set_label("Celdas marcadas: "+str(self.numero_marcas))
                self.etiqueta_numero_minas_sin_marcar.set_label("Minas restantes: "+str(self.minas_restantes))
                #Contar las minas alrededor de cada casilla en cada jugada
                for a in range(len(self.celdas)):
                    coordenadas2=self.celdas[a].get_alignment()
                    coordenadax2=int(coordenadas2[0])
                    coordenaday2=int(coordenadas2[1])
                    self.matriz_de_juego[coordenadax2][coordenaday2].detectar_minas_alrededor(self.matriz_de_juego)
                #Cambiar la imagen de la casilla seleccionada
                if self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is True:
                    if self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==0:
                        self.imagen_celda_abierta=gtk.Image()
                        self.imagen_celda_abierta.set_from_file('hexagonoabierto.png')
                        self.celdas[i].set_image(self.imagen_celda_abierta)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==1:
                        self.imagen_1mina=gtk.Image()
                        self.imagen_1mina.set_from_file('hexagono1mina.png')
                        self.celdas[i].set_image(self.imagen_1mina)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==2:
                        self.imagen_2minas=gtk.Image()
                        self.imagen_2minas.set_from_file('hexagono2minas.png')
                        self.celdas[i].set_image(self.imagen_2minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==3:
                        self.imagen_3minas=gtk.Image()
                        self.imagen_3minas.set_from_file('hexagono3minas.png')
                        self.celdas[i].set_image(self.imagen_3minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==4:
                        self.imagen_4minas=gtk.Image()
                        self.imagen_4minas.set_from_file('hexagono4minas.png')
                        self.celdas[i].set_image(self.imagen_4minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==5:
                        self.imagen_5minas=gtk.Image()
                        self.imagen_5minas.set_from_file('hexagono5minas.png')
                        self.celdas[i].set_image(self.imagen_5minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==6:
                        self.imagen_6minas=gtk.Image()
                        self.imagen_6minas.set_from_file('hexagono6minas.png')
                        self.celdas[i].set_image(self.imagen_6minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor<0:
                        self.imagen_interrogacion=gtk.Image()
                        self.imagen_interrogacion.set_from_file('hexagonointerrogacion.png')
                        self.celdas[i].set_image(self.imagen_interrogacion)
                    if self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is True:
                        #Si es la primera jugada
                        if self.primera_jugada is True:
                            self.primera_jugada=False
                            for f in range(0, self.juego.fil):
                                for c in range(0, self.juego.col):
                                    if self.matriz_de_juego[f][c].tiene_mina is False:
                                        self.matriz_de_juego[f][c].tiene_mina=True
                                        self.primera_jugada=False
                                        break
                                if self.primera_jugada is False:
                                    break
                            self.matriz_de_juego[coordenadax][coordenaday].tiene_mina=False
                            for a in range(len(self.celdas)):
                                coordenadas2=self.celdas[a].get_alignment()
                                coordenadax2=int(coordenadas2[0])
                                coordenaday2=int(coordenadas2[1])
                                self.matriz_de_juego[coordenadax2][coordenaday2].detectar_minas_alrededor(self.matriz_de_juego)
                            if self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==0:
                                self.matriz_de_juego[coordenadax][coordenaday].abrir_recursivamente(self.matriz_de_juego)
                        #Si no es la primera jugada
                        elif self.primera_jugada is False:
                            self.mina_descubierta=True
                elif self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is False:
                    if self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is True:
                        self.imagen_marca=gtk.Image()
                        self.imagen_marca.set_from_file('hexagonomarcado.png')
                        self.celdas[i].set_image(self.imagen_marca)
                    elif self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is False:
                        self.imagen_celda_cerrada=gtk.Image()
                        self.imagen_celda_cerrada.set_from_file('hexagonocerrado.png')
                        self.celdas[i].set_image(self.imagen_celda_cerrada)
        #Cambiar las imagenes de todas las casillas            
        if self.mina_descubierta is False:
            #Si el juego continua
            for i in range(len(self.celdas)):
                coordenadas=self.celdas[i].get_alignment()
                coordenadax=int(coordenadas[0])
                coordenaday=int(coordenadas[1])
                if self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is True:
                    if self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==0:
                        self.imagen_celda_abierta=gtk.Image()
                        self.imagen_celda_abierta.set_from_file('hexagonoabierto.png')
                        self.celdas[i].set_image(self.imagen_celda_abierta)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==1:
                        self.imagen_1mina=gtk.Image()
                        self.imagen_1mina.set_from_file('hexagono1mina.png')
                        self.celdas[i].set_image(self.imagen_1mina)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==2:
                        self.imagen_2minas=gtk.Image()
                        self.imagen_2minas.set_from_file('hexagono2minas.png')
                        self.celdas[i].set_image(self.imagen_2minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==3:
                        self.imagen_3minas=gtk.Image()
                        self.imagen_3minas.set_from_file('hexagono3minas.png')
                        self.celdas[i].set_image(self.imagen_3minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==4:
                        self.imagen_4minas=gtk.Image()
                        self.imagen_4minas.set_from_file('hexagono4minas.png')
                        self.celdas[i].set_image(self.imagen_4minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==5:
                        self.imagen_5minas=gtk.Image()
                        self.imagen_5minas.set_from_file('hexagono5minas.png')
                        self.celdas[i].set_image(self.imagen_5minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor==6:
                        self.imagen_6minas=gtk.Image()
                        self.imagen_6minas.set_from_file('hexagono6minas.png')
                        self.celdas[i].set_image(self.imagen_6minas)
                    elif self.matriz_de_juego[coordenadax][coordenaday].numero_minas_alrededor<0:
                        self.imagen_interrogacion=gtk.Image()
                        self.imagen_interrogacion.set_from_file('hexagonointerrogacion.png')
                        self.celdas[i].set_image(self.imagen_interrogacion)
                elif self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is False:
                    if self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is True:
                        self.imagen_marca=gtk.Image()
                        self.imagen_marca.set_from_file('hexagonomarcado.png')
                        self.celdas[i].set_image(self.imagen_marca)
                    elif self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is False:
                        self.imagen_celda_cerrada=gtk.Image()
                        self.imagen_celda_cerrada.set_from_file('hexagonocerrado.png')
                        self.celdas[i].set_image(self.imagen_celda_cerrada)
        elif self.mina_descubierta is True:
            #Si se ha descubierto una mina
            self.etiqueta_informacion.set_label("BOOM!")
            for i in range(len(self.celdas)):
                coordenadas=self.celdas[i].get_alignment()
                coordenadax=int(coordenadas[0])
                coordenaday=int(coordenadas[1])
                if self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is False:
                    if self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is True:
                        self.imagen_mina=gtk.Image()
                        self.imagen_mina.set_from_file('hexagonomina.png')
                        self.celdas[i].set_image(self.imagen_mina)
                    elif self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is False:
                        self.imagen_celda_abierta=gtk.Image()
                        self.imagen_celda_abierta.set_from_file('hexagonoabierto.png')
                        self.celdas[i].set_image(self.imagen_celda_abierta)
                elif self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is True:
                    if self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is True:
                        self.imagen_marca=gtk.Image()
                        self.imagen_marca.set_from_file('hexagonomarcado.png')
                        self.celdas[i].set_image(self.imagen_marca)
                    elif self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is False:
                        self.imagen_fallo_marca=gtk.Image()
                        self.imagen_fallo_marca.set_from_file('hexagonocruz.png')
                        self.celdas[i].set_image(self.imagen_fallo_marca)
            for i in range(len(self.celdas)):
                self.celdas[i].handler_block_by_func(self.celda_clicked)
        if self.numero_marcas==self.juego.minas:
            #Se comprueba si el jugador ha ganado
            self.partida_ganada=True
            for i in range(len(self.celdas)):
                coordenadas=self.celdas[i].get_alignment()
                coordenadax=int(coordenadas[0])
                coordenaday=int(coordenadas[1])
                if ((self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is True) & (self.matriz_de_juego[coordenadax][coordenaday].tiene_marca is False)):
                    self.partida_ganada = False
                if ((self.matriz_de_juego[coordenadax][coordenaday].esta_abierta is False) & (self.matriz_de_juego[coordenadax][coordenaday].tiene_mina is False)):
                    self.partida_ganada = False
            if self.partida_ganada is True:
                #self.etiqueta_informacion.modify_bg(gtk.gdk.Color(0, 65535, 0), gtk.STATE_NORMAL)
                self.etiqueta_informacion.set_label("VICTORIA") #Victoria
                for i in range(len(self.celdas)):
                    self.celdas[i].handler_block_by_func(self.celda_clicked)
        self.primera_jugada=False                                                            
        return None
    
    def animar(self):
        #Controla el cronometro
        txt = "{:0>2}:{:0>4.1f}".format(int(self.parar_cronometro/60),self.parar_cronometro%60)
        self.etiqueta_cronometro.set_text(txt)
        return None
    
    def volver_al_menu(self,widget):
        #Vuelve a mostrar el menu principal
        self.ventana_menu.show()
        return None
    
    def cambiar_a_marcar(self,widget):
        #Cambia entre abrir casilla y marcar casilla
        if self.marcar is True:
            self.marcar=False
            self.boton_abrir_marcar.set_label("Abrir")
        elif self.marcar is False:
            self.marcar=True
            self.boton_abrir_marcar.set_label("Marcar")
        return None
    

class Celda:

    def __init__(self, fil, col, mina, marca, abierta, minas_alrededor):
        self.fil = fil
        self.col = col
        self.tiene_mina = mina
        self.tiene_marca = marca
        self.esta_abierta = abierta
        self.numero_minas_alrededor = minas_alrededor

    def detectar_minas_alrededor(self, matriz):
        #Calcula el numero de minas que tiene una celda alrededor
        self.numero_minas_alrededor = 0
        if self.fil == 0:  # En la primera fila
            if self.col == 0:  # Si es la primera columna
                if matriz[self.fil + 1][self.col + 1].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if matriz[self.fil + 1][self.col].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if matriz[self.fil][self.col + 1].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
            elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                if matriz[self.fil][self.col - 1].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if matriz[self.fil + 1][self.col].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
            elif self.col > 0 & self.col < (len(matriz[0]) - 1):  # Si son las columnas intermedias
                if matriz[self.fil + 1][self.col + 1].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if matriz[self.fil + 1][self.col].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if matriz[self.fil][self.col + 1].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if matriz[self.fil][self.col - 1].tiene_mina is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor + 1

        elif (self.fil > 0) & (self.fil < (len(matriz) - 1)):  # En las filas intermedias
            if self.fil % 2 == 0:  # Si la fila es par
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                elif (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil + 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
            elif self.fil % 2 == 1:  # Si la fila es impar
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                elif (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil - 1][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil + 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1

        elif self.fil == (len(matriz) - 1):  # En la ultima fila
            if self.fil % 2 == 0:  # Si la ultima fila es par
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
            elif self.fil % 2 == 1:  # Si la ultima fila es impar
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil - 1][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col + 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                if self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil - 1][self.col].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1
                    if matriz[self.fil][self.col - 1].tiene_mina is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor + 1

        if self.fil == 0:  # En la primera fila
            if self.col == 0:  # Si es la primera columna
                if matriz[self.fil + 1][self.col + 1].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if matriz[self.fil + 1][self.col].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if matriz[self.fil][self.col + 1].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
            elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                if matriz[self.fil][self.col - 1].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if matriz[self.fil + 1][self.col].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
            elif self.col > 0 & self.col < (len(matriz[0]) - 1):  # Si son las columnas intermedias
                if matriz[self.fil + 1][self.col + 1].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if matriz[self.fil + 1][self.col].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if matriz[self.fil][self.col + 1].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if matriz[self.fil][self.col - 1].tiene_marca is True:
                    self.numero_minas_alrededor = self.numero_minas_alrededor - 1

        elif (self.fil > 0) & (self.fil < (len(matriz) - 1)):  # En las filas intermedias
            if self.fil % 2 == 0:  # Si la fila es par
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                elif (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil + 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
            elif self.fil % 2 == 1:  # Si la fila es impar
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                elif (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil - 1][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil + 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1

        elif self.fil == (len(matriz) - 1):  # En la ultima fila
            if self.fil % 2 == 0:  # Si la ultima fila es par
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
            elif self.fil % 2 == 1:  # Si la ultima fila es impar
                if self.col == 0:  # Si es la primera columna
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if matriz[self.fil - 1][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col + 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                if self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if matriz[self.fil - 1][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil - 1][self.col].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1
                    if matriz[self.fil][self.col - 1].tiene_marca is True:
                        self.numero_minas_alrededor = self.numero_minas_alrededor - 1

        return matriz

    def abrir_recursivamente(self, matriz):
        # Cambia las celdas a estado abierto de forma recursiva
        self.esta_abierta = True
        if self.fil == 0:  # En la primera fila
            if self.col == 0:  # Si es la primera columna
                if (matriz[self.fil + 1][self.col + 1].esta_abierta is False) & (
                        matriz[self.fil + 1][self.col + 1].tiene_marca is False):
                    matriz[self.fil + 1][self.col + 1].esta_abierta = True
                    if matriz[self.fil + 1][self.col + 1].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil + 1][self.col + 1].abrir_recursivamente(matriz)
                if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                        matriz[self.fil + 1][self.col].tiene_marca is False):
                    matriz[self.fil + 1][self.col].esta_abierta = True
                    if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
                if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                        matriz[self.fil][self.col + 1].tiene_marca is False):
                    matriz[self.fil][self.col + 1].esta_abierta = True
                    if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
            elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                        matriz[self.fil][self.col - 1].tiene_marca is False):
                    matriz[self.fil][self.col - 1].esta_abierta = True
                    if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
                if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                        matriz[self.fil + 1][self.col].tiene_marca is False):
                    matriz[self.fil + 1][self.col].esta_abierta = True
                    if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
            elif self.col > 0 & self.col < (len(matriz[0]) - 1):  # Si son las columnas intermedia
                if (matriz[self.fil + 1][self.col + 1].esta_abierta is False) & (
                        matriz[self.fil + 1][self.col + 1].tiene_marca is False):
                    matriz[self.fil + 1][self.col + 1].esta_abierta = True
                    if matriz[self.fil + 1][self.col + 1].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil + 1][self.col + 1].abrir_recursivamente(matriz)
                if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                        matriz[self.fil + 1][self.col].tiene_marca is False):
                    matriz[self.fil + 1][self.col].esta_abierta = True
                    if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
                if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                        matriz[self.fil][self.col + 1].tiene_marca is False):
                    matriz[self.fil][self.col + 1].esta_abierta = True
                    if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                        matriz[self.fil][self.col - 1].tiene_marca is False):
                    matriz[self.fil][self.col - 1].esta_abierta = True
                    if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                        matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)

        elif (self.fil > 0) & (self.fil < (len(matriz) - 1)):  # En las filas intermedias
            if self.fil % 2 == 0:  # Si la fila es par
                if self.col == 0:  # Si es la primera columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col + 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col + 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col].tiene_marca is False):
                        matriz[self.fil + 1][self.col].esta_abierta = True
                        if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col + 1].tiene_marca is False):
                        matriz[self.fil + 1][self.col + 1].esta_abierta = True
                        if matriz[self.fil + 1][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col + 1].abrir_recursivamente(matriz)
                elif (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col].tiene_marca is False):
                        matriz[self.fil + 1][self.col].esta_abierta = True
                        if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col + 1].tiene_marca is False):
                        matriz[self.fil + 1][self.col + 1].esta_abierta = True
                        if matriz[self.fil + 1][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col-1].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col + 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col + 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col].tiene_marca is False):
                        matriz[self.fil + 1][self.col].esta_abierta = True
                        if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)

            elif self.fil % 2 == 1:  # Si la fila es impar
                if self.col == 0:  # Si es la primera columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col].tiene_marca is False):
                        matriz[self.fil + 1][self.col].esta_abierta = True
                        if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
                elif (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if (matriz[self.fil - 1][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col - 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col - 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col - 1].tiene_marca is False):
                        matriz[self.fil + 1][self.col - 1].esta_abierta = True
                        if matriz[self.fil + 1][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col].tiene_marca is False):
                        matriz[self.fil + 1][self.col].esta_abierta = True
                        if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)
                elif self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col - 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col - 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col - 1].tiene_marca is False):
                        matriz[self.fil + 1][self.col - 1].esta_abierta = True
                        if matriz[self.fil + 1][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil + 1][self.col].esta_abierta is False) & (
                            matriz[self.fil + 1][self.col].tiene_marca is False):
                        matriz[self.fil + 1][self.col].esta_abierta = True
                        if matriz[self.fil + 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil + 1][self.col].abrir_recursivamente(matriz)

        elif self.fil == (len(matriz) - 1):  # En la ultima fila
            if self.fil % 2 == 0:  # Si la ultima fila es par
                if self.col == 0:  # Si es la primera columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col + 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col + 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                if (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col + 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col + 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col + 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                if self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)

            elif self.fil % 2 == 1:  # Si la ultima fila es impar
                if self.col == 0:  # Si es la primera columna
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                if (self.col > 0) & (self.col < (len(matriz[0]) - 1)):  # Si son las columnas intermedias
                    if (matriz[self.fil - 1][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col - 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col - 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col + 1].esta_abierta is False) & (
                            matriz[self.fil][self.col + 1].tiene_marca is False):
                        matriz[self.fil][self.col + 1].esta_abierta = True
                        if matriz[self.fil][self.col + 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col + 1].abrir_recursivamente(matriz)
                if self.col == (len(matriz[0]) - 1):  # Si es la ultima columna
                    if (matriz[self.fil - 1][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col - 1].tiene_marca is False):
                        matriz[self.fil - 1][self.col - 1].esta_abierta = True
                        if matriz[self.fil - 1][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col - 1].abrir_recursivamente(matriz)
                    if (matriz[self.fil - 1][self.col].esta_abierta is False) & (
                            matriz[self.fil - 1][self.col].tiene_marca is False):
                        matriz[self.fil - 1][self.col].esta_abierta = True
                        if matriz[self.fil - 1][self.col].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil - 1][self.col].abrir_recursivamente(matriz)
                    if (matriz[self.fil][self.col - 1].esta_abierta is False) & (
                            matriz[self.fil][self.col - 1].tiene_marca is False):
                        matriz[self.fil][self.col - 1].esta_abierta = True
                        if matriz[self.fil][self.col - 1].numero_minas_alrededor < 1:
                            matriz = matriz[self.fil][self.col - 1].abrir_recursivamente(matriz)
        return matriz


class Modo:

    def __init__(self, fil, col, minas, fichero):
        self.fil = fil
        self.col = col
        self.minas = minas
        self.fichero = fichero

    def generar_tablero(self):
        # Crea el tablero de juego aleatoriamente
        matriz = [[0 for c in range(self.col)] for f in range(self.fil)]
        # Rellena el interior
        for f in range(0, self.fil):
            for c in range(0, self.col):
                matriz[f][c] = Celda(f, c, False, False, False, 0)
        # Coloca las minas
        minas_restantes = self.minas
        for f in range(0, self.fil):
            for c in range(0, self.col):
                while minas_restantes > 0:
                    f = randint(0, len(matriz) - 1)
                    c = randint(0, len(matriz[0]) - 1)
                    if matriz[f][c].tiene_mina is True:
                        minas_restantes = minas_restantes + 1
                    matriz[f][c].tiene_mina = True
                    minas_restantes = minas_restantes - 1
        return matriz

    def generar_tablero_fichero(self, cadena):
        # Crea el tablero de juego segun el fichero
        lista_filas = cadena.split("\n")
        matriz = [[0 for c in range(self.col)] for f in range(self.fil)]
        for f in range(0, self.fil):
            for c in range(0, self.col):
                if lista_filas[f+1][c] == ".":
                    matriz[f][c] = Celda(f, c, False, False, False, 0)
                elif lista_filas[f+1][c] == "*":
                    matriz[f][c] = Celda(f, c, True, False, False, 0)
        return matriz

        
if __name__=='__main__':       
    app=Interfaz()    
    gtk.main()
