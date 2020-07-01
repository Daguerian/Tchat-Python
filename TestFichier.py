# coding: utf-8
print ('LANCEMENT')

'''fichier = open('Data.txt','r')
#r = mode READ, w = WRITE, a = ouvertre ajout a la fin
#t = ouverture en mode texte, x = crée new et l'ouvre en WRITE
'''

Fichier = open("Data.txt", "w")
#print("\n(3) Ouvrir le fichier')
Fichier.write('Yey1\n')
Fichier.write('Yey2\n')
Fichier.write('Yey3\n')
Fichier.write('Yey4\n')
Fichier.write('Yey5\n')
line1 = Fichier.readline()
line2 = Fichier.readline()
line3 = Fichier.readline()
line4 = Fichier.readline()
print(repr(line1))
print(repr(line2))
print(repr(line3))
print(repr(line4))
Fichier.close() # Fermer le fichier