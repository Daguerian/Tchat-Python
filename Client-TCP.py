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

	if Saisie.lower() == ('-help'):
		print ('### Commandes disponibles:')
		print ('### -help')
		print ('### -info')
		print ('### -name')
		print ('### -stop\n')

	if Saisie.lower() == ('-info') or Saisie.lower() == ('-infos'):
		print ('### {}, connecté à {}'.format(NomClient,NomServeur))
		print ('### sur {}:{}\n'.format(IPserveur,Port) )
	
	if Saisie.lower() == ('-name'):
		print ('###Vous:',NomClient)
		print ('###Serveur:', NomServeur,'\n')
		

	if Saisie.lower() == ('-stop'):
		Message = ('!stop')
		client.send(Message.encode('UTF-8'))
		client.close()
		print ('Deconnecté.')
		exit()

	else:
		print('Commande non reconnue')

def Reception():
	global x
	print ('Lancement Thread de reception')
	while True:

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

#NomClient = (socket.gethostname())		#Envoi Nom du client
while True:
	NomClient = input('Saisissez votre nom: ')
	if not NomClient:
		print ('Entrée vide')
	else:
		client.send(NomClient.encode('UTF-8'))
		break

données = client.recv(1024)				#Reception Nom Serveur
NomServeur = données.decode('UTF-8')
print ('Connecté à', NomServeur,'sur {}:{}'.format(IPserveur,Port))
print ('depuis',socket.gethostname())

ThreadReception.start()

while True:
	Saisie = input('Saisissez: ')

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
