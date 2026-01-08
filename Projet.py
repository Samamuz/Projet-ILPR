# On importe les modules nécessaires
import csv  # Pour lire les fichiers CSV (tableur)
from pathlib import Path  # Pour gérer les chemins de fichiers de façon simple
import sys  # Pour récupérer les arguments passés au script


def lire_csv(nom_fichier):
    """
    Lit le fichier CSV et retourne trois dictionnaires :
    - eleves : infos sur chaque élève
    - modules : infos sur chaque module
    - absences : absences par élève et par module
    """
    eleves = {}   # Dictionnaire pour stocker les informations sur les élèves
    modules = {}  # Dictionnaire pour stocker les informations sur les modules
    absences = {} # Dictionnaire pour stocker les absences par élève et par module
    try:
        # On ouvre le fichier CSV avec l'encodage adapté (souvent iso-8859-1 pour les fichiers Windows)
        with open(nom_fichier, encoding="iso-8859-1") as fichier:
            lecteur = csv.DictReader(fichier, delimiter=";")  # On lit le fichier comme un tableau (chaque ligne devient un dictionnaire)
            # On parcourt chaque ligne du fichier CSV
            for ligne in lecteur:
                # On récupère l'identifiant de l'élève (un nombre unique)
                eleve_id = int(ligne["student_id"])
                # Si l'élève n'est pas déjà dans le dictionnaire, on l'ajoute
                if eleve_id not in eleves:
                    eleves[eleve_id] = {"nom": ligne["name"], "prenom": ligne["first_name"]}
                # On récupère l'identifiant du module (matière)
                module_id = int(ligne["module_id"])
                # Si le module n'est pas déjà dans le dictionnaire, on l'ajoute
                if module_id not in modules:
                    modules[module_id] = {"abrev": ligne["module_abrev"], "nb_periodes": int(ligne["module_nb_periodes_total"])}
                # On prépare la structure pour stocker les absences de cet élève pour ce module
                if eleve_id not in absences:
                    absences[eleve_id] = {}
                if module_id not in absences[eleve_id]:
                    absences[eleve_id][module_id] = {"nb_abs": 0, "nb_exc": 0}
                # On ajoute une absence (et on compte si elle est excusée)
                if int(ligne["excuse"]) in (0, 1):
                    absences[eleve_id][module_id]["nb_abs"] += 1  # On ajoute une absence
                    if int(ligne["excuse"]) == 1:
                        absences[eleve_id][module_id]["nb_exc"] += 1  # On ajoute une absence excusée
    except:
        # Si le fichier n'est pas trouvé, on affiche un message d'erreur et on arrête le programme
        print("Fichier CSV introuvable.")
        exit(1)
    # On retourne les trois dictionnaires remplis
    return eleves, modules, absences

def afficher_absences(eleves, modules, absences):
    """
    Affiche le tableau des absences à partir des dictionnaires fournis.
    """
    largeur_nom = 30   # Largeur (en caractères) de la colonne des noms d'élèves
    largeur_col = 18   # Largeur (en caractères) des colonnes des modules

    # Trie les modules par abréviation
    # On trie les modules par abréviation pour un affichage ordonné
    modules_tries = sorted(modules.items(), key=lambda x: x[1]["abrev"])

    # On prépare la première ligne du tableau (en-tête)
    entetes = ["Élève".ljust(largeur_nom)]  # Titre de la colonne des élèves
    for _, module in modules_tries:
        entetes.append(str(module['abrev']).ljust(largeur_col))  # Titre de chaque module
    entetes.append("Total".ljust(largeur_col))  # Colonne pour le total
    print(" ".join(entetes))  # On affiche l'en-tête

    # On affiche chaque élève, trié par nom puis prénom
    for eleve_id in sorted(eleves, key=lambda x: (eleves[x]["nom"], eleves[x]["prenom"])):
        eleve = eleves[eleve_id]
        ligne = [f"{eleve['nom']}, {eleve['prenom']}".ljust(largeur_nom)]  # On commence la ligne avec le nom et prénom
        total_abs = 0  # Total des absences pour l'élève
        total_exc = 0  # Total des absences excusées
        total_per = 0  # Total des périodes suivies
        # On parcourt chaque module pour cet élève
        for module_id, module in modules_tries:
            nb_periodes = module["nb_periodes"]  # Nombre total de périodes pour ce module
            total_per += nb_periodes
            # On récupère les infos d'absence pour ce module (ou 0 si aucune absence)
            infos = absences[eleve_id].get(module_id, {"nb_abs":0, "nb_exc":0})
            if infos["nb_abs"] == 0:
                ligne.append("-".ljust(largeur_col))  # Si aucune absence, on affiche un tiret
            else:
                # On calcule le pourcentage d'absences
                pourcent = infos["nb_abs"] / nb_periodes * 100 if nb_periodes > 0 else 0
                cellule = f"{infos['nb_abs']} / {nb_periodes} ({pourcent:.1f}%)"  # Exemple : 2 / 30 (6.7%)
                ligne.append(cellule.ljust(largeur_col))
                total_abs += infos["nb_abs"]  # On ajoute au total
                total_exc += infos["nb_exc"]  # On ajoute au total excusé
        # On prépare la cellule de total pour l'élève
        total_cellule = f"{total_abs} / {total_exc} / {total_per}"  # absences / excusées / périodes
        ligne.append(total_cellule.ljust(largeur_col))
        print(" ".join(ligne))  # On affiche la ligne complète

def charger_chemin_csv():
    """
    Récupère le chemin du fichier CSV à utiliser (argument ou défaut).
    """
    dossier = Path(__file__).parent  # Dossier où se trouve ce script
    if len(sys.argv) > 1:
        # Si un argument est donné au lancement du script, on l'utilise comme nom de fichier
        chemin = Path(sys.argv[1])
        if not chemin.is_absolute():
            chemin = dossier / chemin  # On complète le chemin si besoin
    else:
        # Sinon, on prend le fichier "absences.csv" par défaut
        chemin = dossier / "absences.csv"
    return str(chemin)  # On retourne le chemin sous forme de texte

def main():
    """
    Fonction principale qui orchestre la lecture et l'affichage.
    """
    # On récupère le chemin du fichier CSV à lire
    chemin_csv = charger_chemin_csv()
    # On lit le fichier CSV et on récupère les données dans des dictionnaires
    eleves, modules, absences = lire_csv(chemin_csv)
    # On affiche le tableau récapitulatif des absences
    afficher_absences(eleves, modules, absences)

# Bloc principal : ce code ne s'exécute que si on lance ce fichier directement
if __name__ == "__main__":
    # On lance la fonction principale
    main()
