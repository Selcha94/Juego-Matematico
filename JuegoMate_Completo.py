import pilasengine
pilas= pilasengine.iniciar()

class PantallaMenu(pilasengine.escenas.Escena):
	def iniciar(self):
		self.fondo_menu= pilas.fondos.Noche()
		self.Mi_menu=pilas.actores.Menu(
		[
		(u'Jugar', self.Ir_al_juego),
		(u'salir', self.Salir_de_Pilas),
		(u'Instrucciones',self.como_jugar)
		])
		nombre_de_juego= pilas.actores.Texto(u'Sumas y Restas')
		nombre_de_juego.color= pilas.colores.verde
		nombre_de_juego.y= 170
		
	#Cursor Disparo
	self.cursor_disparo= pilas.actores.CursorDisparo(y=-150)
	self.cursor_disparo.aprender('arrastrable')
	
	def Actualizar(self):
		pass
	def Salir_de_Pilas(self):
		pilas.terminar()
	def Ir_al_juego(self):
		pilas.escenas.PantallaBienvenida()
	def como_jugar(self):
		pilas.escenas.Instrucciones()
			

class PantallaBienvenida(pilasengine.escenas.Escena):
	
	def iniciar(self):
		self.fondo= self.pilas.fondos.Espacio()
		
		#Defino Puntaje
		self.texto_puntos= pilas.actores.Texto('Puntos: ')
		self.texto_puntos.color='amarillo'
		self.texto_puntos.x= -265
		self.texto_puntos.y= 220
		
		self.puntaje= pilas.actores.Puntaje(color='amarillo')
		self.puntaje.x= -195
		self.puntaje.y= 220
		
		#Defino Vidas
		self.texto_vidas= pilas.actores.Texto('Vidas: ')
		self.texto_vidas.color='amarillo'
		self.texto_vidas.y= 220
		self.texto_vidas.x= 220
		
		self.vidas= pilas.actores.Puntaje(color='amarillo')
		self.vidas.aumentar(cantidad=3)
		self.vidas.x= 290
		self.vidas.y= 220
		
		
		self.crear_pregunta()
		pilas.eventos.pulsa_tecla_escape.conectar(self.regresar)
		
		
	def ejecutar(self):
		pass
	def regresar(self, evento):
		pilas.escenas.PantallaMenu()
	def crear_pregunta(self):
		suma_resta= pilas.azar(0,1)
		#Defino preguntas al azar
		self.preg1= pilas.azar(0,10)
		self.preg2= pilas.azar(0,10)
		
		if suma_resta == 0:
			self.pregunta= pilas.actores.Texto('Cuanto es: ' + str(self.preg1)+ '+' + str(self.preg2), y=180, magnitud= 25)
		else:
			self.pregunta= pilas.actores.Texto('Cuanto es: ' + str(self.preg1)+ '-' + str(self.preg2), y=180, magnitud= 25)
			
		#Defino los Planetas
		self.planeta1 = pilas.actores.Planeta(x=-200, y=70)
		self.planeta1.imagen= 'planeta_naranja.png'
		self.planeta1.escala= 1.5
		self.planeta1.esverdadera= False
	
		self.planeta2= pilas.actores.Planeta(x=0, y=70)
		self.planeta2.imagen= 'planeta_marron.png'
		self.planeta2.escala= 1.5
		self.planeta2.esverdadera= False
	
		self.planeta3= pilas.actores.Planeta(x=200, y=70)
		self.planeta3.imagen= 'planeta_rojo.png'
		self.planeta3.escala= 1.5
		self.planeta3.esverdadera= False
	
		#Defino respuestas
		self.rta_1= pilas.actores.Texto('', x=-200, y=70)
		self.rta_2= pilas.actores.Texto('', x=0, y=70)
		self.rta_3= pilas.actores.Texto('',x=200, y= 70)
	
		#Planetas Posibles
		planetas_posibles= [self.planeta1, self.planeta2, self.planeta3]
		textos_posibles= [self.rta_1,self.rta_2,self.rta_3]
		indiceok= pilas.azar(0,2)
		respuesta_verdadera= planetas_posibles[indiceok]
		respuesta_verdadera.esverdadera= True
		texto_de_respuestaok= textos_posibles[indiceok]
	
		if suma_resta == 0:
			texto_de_respuestaok.texto= str(self.preg1+self.preg2)
		else:
			texto_de_respuestaok.texto= str(self.preg1-self.preg2)
		
		#Planetas Falsos
		if self.planeta1.esverdadera:
			self.rta_2.texto= str(pilas.azar(0,20))
			self.rta_3.texto= str(pilas.azar(0,20))
		
		elif self.planeta2.esverdadera:
			self.rta_1.texto= str(pilas.azar(0,20))
			self.rta_3.texto= str(pilas.azar(0,20))
		elif self.planeta3.esverdadera:
			self.rta_1.texto= str(pilas.azar(0,20))
			self.rta_2.texto= str(pilas.azar(0,20))
			
		#Cursor Disparo
		self.cursor_disparo= pilas.actores.CursorDisparo(y=-150)
		self.cursor_disparo.aprender('arrastrable')
		
			#Colisiones
		planetas= [self.planeta1, self.planeta2,self.planeta3]
		pilas.colisiones.agregar(self.cursor_disparo,planetas,self.respuesta)
	
	def respuesta(self, cursor_disparo,planeta):
		if planeta.esverdadera:
			cursor_disparo.decir('MUY BIEN!!!')
		
			#Genera una estrella para mostrar que contesto Bien 
			estrella= pilas.actores.Estrella()
			estrella.x= planeta.x
			estrella.y= planeta.y
			estrella.escala= 0.2
			estrella.escala= [2,1]*2
			
			#Aumenta el Puntaje
			if self.puntaje.valor < 9:
				self.puntaje.aumentar(1)
				
				#Reinicia el juego pasados los 2 segundos.
				pilas.tareas.una_vez(2,self.reiniciar)
			else:
				pilas.avisar(u'Has Ganado!!!')
				self.puntaje.aumentar(1)
			
				#Vuelve al menu pasados los 4 segundos.
				pilas.tareas.una_vez(4, self.regresar_menu)
				
		
		else:
			cursor_disparo.decir('Vuelve a Intentarlo!')
			pilas.camara.vibrar()
			planeta.eliminar()
			self.puntaje.reducir(1)
			self.vidas.reducir(1)
			
			
			if self.vidas.valor == 0: 
				self.ir_a_pantalla_final()
				pilas.tareas.una_vez(5,self.regresar_menu)
				return
			#Reinicia el juego pasados los 2 segundos.
			pilas.tareas.una_vez(2,self.reiniciar)
		
	def reiniciar(self):
		#Obtiene todos los actores de la Pantalla
		actores= pilas.actores.listar_actores()
			
		#Eliminar todos los actores excepto el fondo y el puntaje
		for actor in actores: 
			if actor not in [self.puntaje, self.texto_puntos, self.texto_vidas, self.vidas, pilas.escena.fondo]:
				actor.eliminar()
			
		#Genera una pregunta nueva
		self.crear_pregunta()
			
	def regresar_menu(self):
		pilas.escenas.PantallaMenu()
		
	def ir_a_pantalla_final(self):
		pantalla_final = pilas.escenas.PantallaFinal()
		pantalla_final.iniciar()
		
		
		
class Instrucciones(pilasengine.escenas.Escena):
	#Instrucciones sencillas sobre el Juego.
	
    def iniciar(self):
        self.fondo= self.pilas.fondos.Galaxia(dx=0, dy=-1)
        texto= pilas.actores.Texto('*INSTRUCCIONES SOBRE EL JUEGO*')
        texto.y=200
        texto.color= pilas.colores.naranja
        expli= pilas.actores.Texto('Este juego se trata sobre sumas y restas.')
        expli.y=150          
        expli1= pilas.actores.Texto('Para responder, tiene que mover el cursor.')
        expli1.y=120
        expli2= pilas.actores.Texto('El cursor se movera cuando lo arrastre con el mouse.')
        expli2.y= 90                    
        expli3= pilas.actores.Texto('Sumando 1p por cada respuesta correcta y si es')
        expli3.y= 60                                                    
        expli4= pilas.actores.Texto('incorrecta se restara 1p y perderas 1 vida')                                                                                                
        expli4.y=30                                                                                                                                            
        expli5= pilas.actores.Texto('No te preocupes tienes 3 Vidas.')
        expli5.y= 0
        expli6= pilas.actores.Texto('El juego termina cuando se obtengan 10p.')
        expli6.y=-30
        mensaje= pilas.actores.Texto('**QUE TE DIVIERTAS!**')
        mensaje.y= -140
        mensaje.color= pilas.colores.naranja
        mensaje.escala= 1.5
        volver= pilas.interfaz.Boton('Volver')
        volver.y= -200
        volver.x= 260
        volver.conectar(pilas.escenas.PantallaMenu)
		
		
       
		
class PantallaFinal(pilasengine.escenas.Escena):
	
	def iniciar(self):

		self.fondo= self.pilas.fondos.Galaxia(dx=0, dy=-1)
		self.estrella = pilas.actores.Estrella(x=0, y=0)
		self.estrella.imagen= 'estrella.png'
		self.estrella.escala= 2.5
		texto_animo= pilas.actores.Texto('Vuelve a Intentar , No te desanimes!!! (<>__<>)')
		texto_animo.y= 0
		texto_animo.color= pilas.colores.verde
	
		
		
		
			
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.vincular(PantallaBienvenida)
pilas.escenas.vincular(Instrucciones)
pilas.escenas.vincular(PantallaFinal)

pilas.escenas.PantallaMenu()
pilas.ejecutar()
				
		

	
		
		
		
	
			
		
							
		
	
