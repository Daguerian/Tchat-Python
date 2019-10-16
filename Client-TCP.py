import socket
import sys
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
x = 0
y = 0
Reçu = 0
Port = 6789

def CommandList():
	if Saisie.lower() == ('-info') or Saisie.lower() == ('-infos'):
		print (socket.gethostname, 'connexté à', NomServeur)
		print ('sur', IPserveur, ':', Port)

	if Saisie.lower() == ('-stop'):
		Message = ('-stop')
		client.send(Message.encode('UTF-8'))
		client.close()
		print ('Deconnecté.')
		
	#if Saisie.lower == ('-time')
	#	print (time)

	else:
		print('Commande non reconnue')

def Reception():
	global x
	print ('Lancement Thread de reception')
	while True:
		#données = client.recv(1024)
		#Reçu = données.decode('UTF-8')
		Reçu = client.recv(1024).decode('UTF-8')
		if not Reçu:
			print ('Erreur de reception')
			x += 1
			if x == 5:
				print ('Fermeture de la connexion')
				client.close()
				break
		if Reçu.lower() == ('!arret'):
				print ('Arret du serveur. Deconnexion client')
				client.close()
				exit()
		else:
			print(NomServeur,':',Reçu)
ThreadReception = threading.Thread(target=Reception)

#### Lancement Programme ####
print ('Client demarré \nConnexion au serveur')

while True:
	IPserveur = input('Saisissez l\'adresse IP du serveur: ')
	if not IPserveur:
		pass
	else:
		try:
			client.connect((IPserveur,6789))
			break
		except:
			print('Impossible de se connecter à {}:{}'.format(IPserveur,Port))
			exit()

NomClient = (socket.gethostname())		#Envoi Nom du client
client.send(NomClient.encode('UTF-8'))

données = client.recv(1024)				#Reception Nom Serveur
NomServeur = données.decode('UTF-8')
print ('Connecté à', NomServeur,'sur {}:{}'.format(IPserveur,Port))
print ('depuis',socket.gethostname())

ThreadReception.start()

while True:
	Saisie = input('Saisissez: ')

	# if Saisie.lower() == ('-deconnexion'):
	# 	Message = ('-stop')
	# 	client.send(Message.encode('UTF-8'))
	# 	client.close() #Appel a la variable client ligne 7
	# 	print ('Deconecté.')
	# 	break

	y = Saisie.startswith('-',0,2) #Saisie commence par '-' entre le caractere 0 et 2 (non inclus)
	if y:
		CommandList()
		y = 0

	else:
		Message = Saisie.encode('utf-8')
		n = client.send (Message)	#Envoi du message
		if (n!= len(Saisie)) or Saisie == (''):
			print ('Erreur d\'envoi')
		else:
			#client.send(Saisie.encode('UTF-8'))
			print ('Message envoyé.')
