# -- coding: utf-8 --

import socket
import sys
import threading
import time

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ouverture du socket
#y = 0 #saisie.startwith()
Recu = 0
NomServeur = 'Tests ACERVER'
ListeAddrClients = []
ListeClients = []
ListePseudoClients = []
ListeThreadsClients = []

def Stop():
	for i in ListeClients:
		print ("Fermeture de la Connexion avec", ListePseudoClients[0])
		t = ('!arret')
		ListeClients[0].send(t.encode('UTF-8')) #envoi au 1er de la liste
		time.sleep(0.5) #Delais de reponse du client
		ListeClients[0].close()
		del ListeClients[0] #supprime les 1ers de chaque liste
		del ListeAddrClients[0]
		del ListePseudoClients[0]

	print ('Arret du serveur')
	serveur.close()
	exit()

def CommandList(): #Liste des commandes internes
	if Saisie.lower() == ('-help'):
		print ('')

	if Saisie.lower() == ('-liste') or Saisie.lower() == ('-list'):
		print ("Adresses des clients connectés:\n", ListeAddrClients)
		print ("Nom des clients connectés:\n", ListePseudoClients)
		print ("Clients connectés: ", ListeClients)
		print ("Liste Threads: ", ListeThreadsClients)
	if Saisie.lower() == ('-infoserveur'):
		print ('Host:', Host, '|  Port:', Port)

	if Saisie.lower() == ('-stop') or Saisie.lower() == ('-arret'):
		Stop()

	if Saisie.lower() == ('-infoclient'):
		print (client, AdresseClient)

	else:
		print ('Commande non reconnue')
		pass

def Join():
	serveur.listen(5)
	# serveur.setblocking(0) #defini comme non bloquant, mais non operationnel
	while True:		#Boucle d'attente de nouvelle Connexion
		client, AdresseClient = serveur.accept()
		ListeAddrClients.append(AdresseClient)
		ListeClients.append(client)
		ThreadReception = threading.Thread(target=Reception, args = (client, AdresseClient))
		ThreadReception.start()
		ListeThreadsClients.append(ThreadReception)

def Reception(client, AdresseClient):	#à renommer "Gestion clients"
	x = 0
	while True:		#Boucle verification de nom deja utilisé
		PseudoClient = client.recv(1024).decode('UTF-8')
		if PseudoClient in ListePseudoClients:
			t = ('!name-already-used')
			client.send(t.encode('UTF-8'))
		else:
			print (PseudoClient, "s'est connecté depuis",AdresseClient)
			client.send(NomServeur.encode('UTF-8'))
			ListePseudoClients.append(PseudoClient)
			break

	while True:
		data = client.recv(1024)
		Recu = data.decode('UTF-8')

		if not Recu:
			print('Erreur de reception')
			x += 1

		if x == 10:
			print (AdresseClient, "déconnecté. \nTrop d'erreurs de reception")
			client.close()
		t = Recu.startswith('!',0,2)
		if t:

			if Recu.lower() == ('!leave'): #Demande de deconnexion depuis le client
				t = ('!leaveOK')
				client.send(t.encode('UTF-8')) #Envoi de confirmation de deconnexion
				print(AdresseClient,'deconecté') #sendall plus tard
				# while AdresseClient in ListeAddrClients:
				ListeAddrClients.remove(AdresseClient)
				# while PseudoClient in ListePseudoClients:
				ListePseudoClients.remove(PseudoClient)
				break
			if Recu.lower() == ('!leaveok'): #confirmation deconnexion du client par le serveur
				break
			# if Recu.lower() == ('!listeusers'):
			# 	t = ('Liste des clients connectés:', ListePseudoClients)
			# 	client.send(t.encode('UTF-8'))
			# 	print ('Liste des utilisateur envoyé à ', PseudoClient)

			else:
				print ("Commande '{}' de '{}' non reconnue".format(recu,PseudoClient))
		else:
			print (PseudoClient, ' : ', Recu)

#### Lancement Progamme ####

Host, Port = input('Adresse Host: '), 6789
try:
	serveur.bind((Host, Port)) #Essaie de se connecter
except:
	print ('Impossible d\'heberger le serveur sur {}:{}'.format(Host,Port))
	exit()

print ('Serveur hebergé sur ',Host, Port, '\nAppareil', socket.gethostname())
print ('En attente de connexion...\n')
ThreadJoinClients = threading.Thread(target = Join)
ThreadJoinClients.start()


while True:

	Saisie = input('Saisissez: ')

	# if Saisie.lower() == ('-arret'):
	# 	Stop()
	# 	break
	y = Saisie.startswith('-',0,2) #'-' entre 0 et 2, non inclus
	if y:
		CommandList()	#Action en fonction d'une demande syntaxée
		y = 0
	else:
		n = serveur.sendto(Saisie.encode('UTF-8'),client in ListeAddrClients)
		if not n:
			print ('Erreur d\'envoi')
		else:
			print ('Envoyé.')

#Apres arret, client non deconnecté /!\
