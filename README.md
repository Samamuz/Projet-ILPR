But du programme
Ce programme lit un fichier CSV (tableur) qui contient les absences des élèves par matière (module) et affiche un tableau récapitulatif des absences pour chaque élève.

Comment ça marche ?

Il utilise des modules Python :
csv pour lire le fichier CSV.
pathlib pour gérer les chemins de fichiers.
sys pour récupérer les arguments donnés au lancement du script.
Fonctionnement étape par étape :
Lecture du CSV :
La fonction lire_csv lit le fichier CSV et range les informations dans trois dictionnaires :

eleves : les informations sur chaque élève (nom, prénom).
modules : les informations sur chaque matière (abréviation, nombre de périodes).
absences : le nombre d’absences (et d’absences excusées) pour chaque élève et chaque matière.
Affichage :
La fonction afficher_absences affiche un tableau :

Chaque ligne correspond à un élève.
Chaque colonne correspond à une matière.
On voit le nombre d’absences, le nombre de périodes, et le pourcentage d’absences.
À la fin de chaque ligne, il y a un total pour l’élève.
Choix du fichier CSV :
Le programme prend le nom du fichier CSV à lire :

Soit donné en argument lors du lancement.
Soit il prend par défaut le fichier absences.csv dans le même dossier.
Lancement :
Quand on lance le fichier, il exécute la fonction principale qui fait tout le travail.

En résumé :
Ce programme permet de transformer un fichier d’absences d’élèves (format tableur) en un tableau lisible qui résume les absences de chaque élève par matière.
