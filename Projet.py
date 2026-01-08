
import csv
from pathlib import Path
import sys

# On prépare des dictionnaires pour stocker les informations
# élève_id -> {"nom": ..., "prenom": ...}
# module_id -> {"abrev": ..., "nb_periodes": ...}
# élève_id -> module_id -> {"nb_abs": ..., "nb_exc": ...}

def lire_csv(nom_fichier):
    """
    Lit le fichier CSV et retourne trois dictionnaires :
    - eleves : infos sur chaque élève
    - modules : infos sur chaque module
    - absences : absences par élève et par module
    """
    eleves = {}
    modules = {}
    absences = {}
    try:
        # Ouvre le fichier CSV
        with open(nom_fichier, encoding="utf-8") as fichier:
            lecteur = csv.DictReader(fichier, delimiter=";")
            # Pour chaque ligne du fichier
            for ligne in lecteur:
                # Récupère l'identifiant de l'élève
                eleve_id = int(ligne["student_id"])
                # Ajoute l'élève s'il n'existe pas déjà
                if eleve_id not in eleves:
                    eleves[eleve_id] = {"nom": ligne["name"], "prenom": ligne["first_name"]}
                # Récupère l'identifiant du module
                module_id = int(ligne["module_id"])
                # Ajoute le module s'il n'existe pas déjà
                if module_id not in modules:
                    modules[module_id] = {"abrev": ligne["module_abrev"], "nb_periodes": int(ligne["module_nb_periodes_total"])}
                # Prépare la structure pour les absences
                if eleve_id not in absences:
                    absences[eleve_id] = {}
                if module_id not in absences[eleve_id]:
                    absences[eleve_id][module_id] = {"nb_abs": 0, "nb_exc": 0}
                # Ajoute une absence (et excuse si besoin)
                if int(ligne["excuse"]) in (0, 1):
                    absences[eleve_id][module_id]["nb_abs"] += 1
                    if int(ligne["excuse"]) == 1:
                        absences[eleve_id][module_id]["nb_exc"] += 1
    except:
        print("Fichier CSV introuvable.")
        exit(1)
    return eleves, modules, absences

def afficher_absences(eleves, modules, absences):
    """
    Affiche le tableau des absences à partir des dictionnaires fournis.
    """
    largeur_nom = 30   # Largeur de la colonne nom
    largeur_col = 18   # Largeur des colonnes modules

    # Trie les modules par abréviation
    modules_tries = sorted(modules.items(), key=lambda x: x[1]["abrev"])

    # Affiche l'en-tête
    ligne = f"{'Élève':{largeur_nom}}"
    for _, module in modules_tries:
        ligne += f" {module['abrev']:{largeur_col}}"
    ligne += f" {'Total':{largeur_col}}"
    print(ligne)

    # Affiche chaque élève (trié par nom, prénom)
    for eleve_id in sorted(eleves, key=lambda x: (eleves[x]["nom"], eleves[x]["prenom"])):
        eleve = eleves[eleve_id]
        ligne = f"{eleve['nom']}, {eleve['prenom']:{largeur_nom-2}}"
        total_abs = 0
        total_exc = 0
        total_per = 0
        # Pour chaque module, affiche les absences
        for module_id, module in modules_tries:
            nb_periodes = module["nb_periodes"]
            total_per += nb_periodes
            # Récupère les absences pour ce module
            infos = absences[eleve_id].get(module_id, {"nb_abs":0, "nb_exc":0})
            if infos["nb_abs"] == 0:
                ligne += f" {'-':{largeur_col}}"  # Pas d'absence
            else:
                pourcent = infos["nb_abs"] / nb_periodes * 100 if nb_periodes > 0 else 0
                cellule = f"{infos['nb_abs']} / {nb_periodes} ({pourcent:.1f}%)"
                ligne += f" {cellule:{largeur_col}}"
                total_abs += infos["nb_abs"]
                total_exc += infos["nb_exc"]
        # Affiche le total pour l'élève
        total_cellule = f"{total_abs} / {total_exc} / {total_per}"
        ligne += f" {total_cellule:{largeur_col}}"
        print(ligne)

def charger_chemin_csv():
    """
    Récupère le chemin du fichier CSV à utiliser (argument ou défaut).
    """
    dossier = Path(__file__).parent
    if len(sys.argv) > 1:
        chemin = Path(sys.argv[1])
        if not chemin.is_absolute():
            chemin = dossier / chemin
    else:
        chemin = dossier / "absences.csv"
    return str(chemin)

def main():
    """
    Fonction principale qui orchestre la lecture et l'affichage.
    """
    # On récupère le chemin du fichier CSV
    chemin_csv = charger_chemin_csv()
    # On lit le fichier et on récupère les données
    eleves, modules, absences = lire_csv(chemin_csv)
    # On affiche le tableau
    afficher_absences(eleves, modules, absences)

# Bloc principal : ce code ne s'exécute que si on lance ce fichier directement
if __name__ == "__main__":
    main()
