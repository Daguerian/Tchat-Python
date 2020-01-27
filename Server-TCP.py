# -- coding: utf-8 --

import socket
import sys
import threading
import time

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ouverture du socket
#y = 0 #saisie.startwith()
serveur.setblocking(0) #socket serveur non bloquant, exemple serveur.accept
Saisie = 0 #Initialisation de la Saisie, pour le def Join()
Recu = 0
NomServeur = 'Tests ACERVER'
ListeAddrClients = []
ListeClients = []
ListePseudoClients = []
ListeThreadsClients = []

def Stop():

	for i in range(len(ListeClients)):
		print (i)
	# for i in ListeClients:
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

def CommandList(): #Liste des commandes internes
	if Saisie.lower() == ('-help'):
		print ("#############################################################")
		print ("###             ### Commandes disponibles ###             ###")
		print ("###                                                       ###")
		print ("### -help     Affiche cette page d'aide                   ###")
		print ("### -list     Affiche la liste des clients connectés      ###")
		print ("### -thread   Affiche la liste des Threads lancés/arretés ###")
		print ("### -info     Affiche les information du serveur          ###")
		print ("### -stop     Arrete le serveur et deconnecte les clients ###")
		print ("#############################################################")

	elif Saisie.lower() == ('-liste') or Saisie.lower() == ('-list'):
		print (len(ListeClients), "clients connectés")
		print ("Adresses des clients connectés:\n", ListeAddrClients)
		print ("Nom des clients connectés:\n", ListePseudoClients)

	elif Saisie.lower() == ('-thread'):
		print ("Liste Threads: ", ListeThreadsClients)

	elif Saisie.lower() == ('-info'):
		print ('Host:', Host, '|  Port:', Port)

	elif Saisie.lower() == ("-test"):
		print (ListeClients)
	#Commande arret deplacée sur boucle saisie, pour le break
	# elif Saisie.lower() == ('-stop') or Saisie.lower() == ('-arret'):
	# 	Stop()
	# 	break



	else:
		print ('Commande non reconnue')
		pass

def Join():
	serveur.listen(5)
	# serveur.setblocking(False) #defini comme non bloquant, mais non operationnel
	while True:		#Boucle d'attente de nouvelle Connexion
		try:
			client, AdresseClient = serveur.accept()
			ListeAddrClients.append(AdresseClient)
			ListeClients.append(client)
			ThreadReception = threading.Thread(target=Reception, args = (client, AdresseClient))
			ThreadReception.start()
			ListeThreadsClients.append(ThreadReception)
		except:
			pass
		if Saisie == ("-stop"):
			break
		else:
			time.sleep(0.1)
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
				ListeAddrClients.remove(AdresseClient)
				ListePseudoClients.remove(PseudoClient)
				ListeClients.remove(client)
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
			print (PseudoClient, ':', Recu)
			for i in range(len(ListeClients)):
				t = str((PseudoClient,':',Recu))
				t = t.replace('(',"")
				t = t.replace(')',"")
				t = t.replace(',',"")
				t = t.replace("'","")
				ListeClients[i].send(t.encode('UTF-8'))



#### Lancement Progamme ####

# Host, Port = input('Adresse Host: '), 6789
Host,Port = "192.168.1.15",6789
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

	Saisie = input('> ')

	y = Saisie.startswith('-',0,2) #'-' entre 0 et 2, non inclus
	if y:
		if Saisie.lower() == ('-stop') or Saisie.lower() == ('-arret'):
			Stop()
			break
		else:
			CommandList()	#Action en fonction d'une demande syntaxée
			y = 0
	else:
		for i in range(len(ListeClients)):
			Envoi = str((NomServeur,':',Saisie))
			Envoi = Envoi.replace('(','')
			Envoi = Envoi.replace(')','')
			Envoi = Envoi.replace(',','')
			Envoi = Envoi.replace("'",'')
			n = ListeClients[i].send(Envoi.encode('UTF-8'))
			if not n:
				print ('Erreur d\'envoi vers', ListePseudoClients[i])
			else:
				print ('Envoyé.')
