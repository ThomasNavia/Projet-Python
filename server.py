import socket
import select
import random
import struct
hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(10) #Nombre de connexions accepté 

print("Le serveur écoute à présent sur le port {}".format(port))
serveur_lance = True
Questions = []
Results = []
clients_connectes = []
i = 0
Operations_valide = ["+","-","*","/"]

def CreateQuestions():
	for i in range(10):
		FirstRandInt = random.randint(1, 100)
		SecondRandInt = random.randint(1 , 100)
		OperationRand = random.choice(Operations_valide)
		Set_Question = "Question numero 1 : calculez : " + str(FirstRandInt) + " " + str(OperationRand) + " " + str(SecondRandInt)
		Questions.append(Set_Question.encode())
		Results.append(eval(str(FirstRandInt) + str(OperationRand) + str(SecondRandInt)))
	return

while serveur_lance:
	connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 3)

	for connexion in connexions_demandees:
		connexion_avec_client, infos_connexion = connexion.accept()
		clients_connectes.append(connexion_avec_client)
	clients_a_lire = []
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
	except select.error:
		pass
	else:
		CreateQuestions()
		for client in clients_a_lire:
				Set_Welcome = "Bonjour bienvenue vous êtes le joueur : " + str(len(clients_a_lire))
				client.sendall(Set_Welcome.encode())	
				print(Results)
				print(Questions)
				for i in range(10):
					client.sendall(Questions[i])
					ReponseClient = client.recv(1024)
					if ReponseClient.decode() == Results[i]:
						client.send("Gg".encode())
					else:
						client.send("Essayez encore".encode())
					
print("Fermeture des connexions")
for client in clients_connectes:
	client.close()
connexion_principale.close()
