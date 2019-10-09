import socket
import sys
import threading
import time

Host, Port = input('Adresse Host: '), 6789
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	serveur.bind((Host, Port))
except:
	print ('Impossible dheberger le serveur sur ',Host, Port)
	exit()

print ('Serveur hebergé sur ',Host, Port, '\n', socket.gethostname())

x = 0
Reçu = True

def Stop():		#Re-def only arret, a integrer plus bas dans un if
	MessageArret = ('Arret du serveur')
	#MessageArret = MessageArret.encode('UTF-8')
	client.send(MessageArret.encode('UTF-8'))
	print ('Fermeture de la Connexion avec le client')
	client.close()
	print ('Arret du serveur')
	serveur.close() #Appel a la variable serveur ligne 7

def CommandList():
	if Saisie.startwith(' -'):
		if Saisie.lower == ('-InfoServeur'):
			print ('Host: ', Host, 'Port: ', Port)

		else:
			pass
	else:
		pass

def Reception():
	global x
	print ('Lancement Thread de reception')
	while True:
		données = client.recv(1024)

		Reçu = données.decode('UTF-8')
		CommandList()	#Action en fonction d'une demande syntaxée
		
		if not Reçu:
			print('Erreur de reception')
			x += 1
		
		if x == 5:
			Stop()
			break
		if Reçu.lower() == ('deconnexion'):
			print(NomClient,'deconecté')
			break
		
		else:
			print (NomClient, ' : ', Reçu)


ThreadReception = threading.Thread(target=Reception)



### Demarrage Programme ###
print ('Serveur démarré. \nEn attente de connexion...\n')
serveur.listen(3) #3 connexions maxi
client, AdresseClient = serveur.accept()  #client peux etre remplacé par Client1
#Blocage tant que le client n'est pas connecté

EnvoiNameServer = (socket.gethostname())			#Envoi Nom du serveur
EnvoiNameServer = EnvoiNameServer.encode('UTF-8')
client.send(EnvoiNameServer)

données = client.recv(1024)							#Reception Nom du client
NomClient = données.decode('UTF-8')
print (NomClient,'connecté')
ThreadReception.start()

while True:

	Saisie = input('Saisissez: ')
	Reponse = Saisie.encode('UTF-8')
	n = client.send(Reponse)
	#if (n != len(reponseEncodée)):
	CommandList()
	if not n:
		print ('Erreur d\'envoi')
	if reponse.lower() == ('arret'):
		Stop()
		break
	else:
		print ('Envoyé.')
