import socket
import sys
import threading
import time


x = 0
Reçu = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Client demarré \nConnexion au serveur')

while True:
	IPserveur = input('saisissez l\'adresse IP sur serveur: ')
	if not IPserveur:
		pass
	else:
		try:
			client.connect((IPserveur, 6789)) #Connexion au serveur
			break
		except:
			print ('Impossible de se connecter à "{}"'.format(IPserveur))
			exit()

NomClient = (socket.gethostname())		#Envoi Nom du client
NomClient = NomClient.encode('UTF-8')
client.send(NomClient)

données = client.recv(1024)				#Reception Nom Serveur
NomServeur = données.decode('UTF-8')
print ('Connecté à ', NomServeur,'depuis',socket.gethostname())

def Reception():
	global x
	print ('Lancement Thread de reception')
	while True:
		données = client.recv(1024)
		Reçu = données.decode('UTF-8')
		print (NomServeur,':',Reçu)
		time.sleep(0.1)
		if not Reçu:
			print ('Erreur de reception')
			x += 1
			if x == 5:
				print ('Fermeture de la connexion')
				client.close()
				break
		if Reçu.lower() == ('arret'):
				print ('Arret du serveur. Deconnexion client')
				client.close()
				exit()

ThreadReception = threading.Thread(target=Reception)
ThreadReception.start()

while True:
	Saisie = input('Saisissez: ')
	if Saisie.lower() == 'deconnexion':
		client.send(Saisie.encode('UTF-8'))
		client.close() #Appel a la variable client ligne 7
		print ('Deconecté.')
		break
	else:
		Message = Saisie.encode('utf-8')
		n = client.send (Message)
		if (n!= len(Saisie)) or Saisie == (''):
			print ('Erreur d\'envoi')
		else:
			print ('Message envoyé.')
