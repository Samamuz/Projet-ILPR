# Explication détaillée du programme d'affichage des absences

Ce document explique, étape par étape, le fonctionnement du programme Python qui lit un fichier CSV d'absences et affiche un tableau récapitulatif. Tout est expliqué pour un débutant !

## 1. À quoi sert ce programme ?

Ce programme permet de :
- Lire un fichier CSV (tableur) contenant les absences des élèves par module.
- Compter le nombre d'absences (et d'excuses) pour chaque élève et chaque module.
- Afficher un tableau récapitulatif lisible dans la console.

## 2. Structure du fichier CSV attendu

Le fichier CSV doit contenir des colonnes comme :
- `student_id` : identifiant unique de l'élève
- `name` : nom de l'élève
- `first_name` : prénom de l'élève
- `module_id` : identifiant du module
- `module_abrev` : abréviation du module (ex : MATH, HIST)
- `module_nb_periodes_total` : nombre total de périodes pour ce module
- `excuse` : 0 (absence non excusée) ou 1 (absence excusée)

Chaque ligne correspond à une absence.

## 3. Les grandes étapes du programme

### a) Import des modules
- `csv` : pour lire le fichier CSV facilement.
- `pathlib` et `sys` : pour gérer les chemins de fichiers et les arguments de la ligne de commande.

### b) Préparation des "dictionnaires"
- `eleves` : pour stocker les informations sur chaque élève.
- `modules` : pour stocker les informations sur chaque module.
- `absences` : pour stocker, pour chaque élève et chaque module, le nombre d'absences et d'excuses.

### c) Fonction `lire_csv(nom_fichier)`
- Ouvre le fichier CSV.
- Lit chaque ligne du fichier.
- Ajoute l'élève dans `eleves` s'il n'y est pas déjà.
- Ajoute le module dans `modules` s'il n'y est pas déjà.
- Prépare la structure pour compter les absences.
- Incrémente le nombre d'absences et d'excuses selon la colonne `excuse`.
- Si le fichier n'existe pas, affiche un message d'erreur.

### d) Fonction `afficher_absences()`
- Affiche l'en-tête du tableau (noms des modules).
- Pour chaque élève (trié par nom, prénom) :
    - Affiche le nom et le prénom.
    - Pour chaque module, affiche le nombre d'absences et le pourcentage par rapport au nombre de périodes.
    - Affiche le total des absences, des excuses et des périodes pour l'élève.

### e) Programme principal
- Cherche le fichier CSV dans le même dossier que le script, sauf si un autre chemin est donné en argument.
- Appelle `lire_csv()` pour charger les données.
- Appelle `afficher_absences()` pour afficher le tableau.

## 4. Exemple d'utilisation

- Place le fichier `absences.csv` dans le même dossier que le script Python.
- Ouvre un terminal dans ce dossier.
- Lance le programme avec :
  ```
  python 1.1.py
  ```
- Ou, pour utiliser un autre fichier :
  ```
  python 1.1.py mon_fichier.csv
  ```

## 5. Astuces pour débutant
- Les dictionnaires sont comme des "boîtes" pour ranger des informations avec des étiquettes.
- On utilise beaucoup les boucles `for` pour parcourir les élèves et les modules.
- Les fonctions permettent de découper le programme en petits morceaux faciles à comprendre.
- Les commentaires (lignes qui commencent par `#`) expliquent ce que fait chaque partie du code.

## 6. Pour aller plus loin
- On peut modifier le programme pour afficher d'autres statistiques.
- On peut ajouter une sauvegarde des résultats dans un nouveau fichier.
- On peut améliorer l'affichage pour qu'il soit plus joli ou plus compact.

N'hésite pas à relire le code source en parallèle de ce document pour bien comprendre chaque étape !
