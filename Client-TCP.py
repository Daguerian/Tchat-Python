import socket
import sys
import threading
import time


x = 0
Reçu = 0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Client demarré \nConnexion au serveur')
IPserveur = input('saisissez l\'adresse IP sur serveur: ')
client.connect((IPserveur, 6789)) #Connexion au serveur

NomClient = (socket.gethostname())		#Envoi Nom du client
NomClient = NomClient.encode('UTF-8')
client.send(NomClient)

données = client.recv(1024)				#Reception Nom Serveur
NomServeur = données.decode('UTF-8')
print ('Connecté à ',NomServeur,'depuis',socket.gethostname())

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
	Message = input('Saisissez: ')
	if Message.lower() == 'deconnexion':
		client.send(Message.encode('UTF-8'))
		client.close() #Appel a la variable client ligne 7
		print ('Deconecté.')
		break
	else:
		MessageEncodé = Message.encode('utf-8')
		n = client.send (MessageEncodé)
		if (n!= len(Message)) or Message == (''):
			print ('Erreur d\'envoi')
		else:
			print ('Message envoyé.')
