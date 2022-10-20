import socket
import sys

HOST = ''  # Nombre o direccion de la maquina. Puede estar vacio en el servidor
PORT = 8888  # Puerto de escucha del servidor. PORT >= 5000
BUFFER = 1024 # Tamano del buffer de recepcion

# Primero se crea el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print('Socket creado...')

# Enlaza el socket con la direccion y puerto local
try:
	s.bind(("localhost", 8888))

#print(type(s.blind))

# Captura excepciones. Si existe, un error sale del programa
except socket.error as msg:
	print('Fallo en BIND. Cod. Error: {} Mensaje: {}'.format(msg.errno,msg.strerror))
	sys.exit()

print('Socket Enlazado...')

# Comienza la escucha en el socket
s.listen(10)

print('Socket escuchando...')

while 1:
	try:
		# Espera a que lleguen clientes. Se aceptan conexiones.
		cliente, addr = s.accept()
		print('Conectado con {}:{}'.format(addr[0],addr[1]))
		
		while 1:
			# Recepcion de datos. Se reciben datos del cliente.
			datos = cliente.recv(1024)
			if datos=='quit':
                # Se envia al cliente lo mismo que se ha recibido (eco).
				cliente.send(datos)
				# Se imprime pasando un byte string a string
				print('Recibido: {}'.format(datos.decode("utf-8")))
			 # Se dejara de trabajar con el cliente si se recibe EXIT
			 	# Tambien lo podemos comparar si lo hacemos con un byte string (los dos tipos deben ser iguales)
				if datos[0:4] == b'EXIT':
					cliente.close() 
					break
	except KeyboardInterrupt:
		print('\nCerrando socket y apagando servidor...')
		s.close()
		break
		
s.close()

