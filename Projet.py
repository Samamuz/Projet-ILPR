import csv
from pathlib import Path
import argparse
import sys

# =========================
# Dictionnaires principaux
# =========================

eleves = {}
modules = {}
absences = {}


def load_csv(csv_path):
    """Charge le CSV d'absences depuis `csv_path`.
    `csv_path` peut être un str ou un Path. Lance FileNotFoundError si absent.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier CSV introuvable: {csv_path}")

    def safe_int(value, default=0):
        try:
            if value is None or str(value).strip() == "":
                return default
            return int(value)
        except (ValueError, TypeError):
            return default

    def process_reader(reader):
        for row in reader:
            # --- Élève ---
            student_id = safe_int(row.get("student_id"))
            nom = row.get("name", "")
            prenom = row.get("first_name", "")

            # --- Module ---
            module_id = safe_int(row.get("module_id"))
            periodes_total = safe_int(row.get("module_nb_periodes_total"))

            # --- Matière ---
            matiere_id = safe_int(row.get("matiere_id"))

            # --- Absence ---
            absence = safe_int(row.get("absence_position"))
            excuse = safe_int(row.get("excuse"))

            # =========================
            # eleves (référentiel)
            # =========================
            if student_id not in eleves:
                eleves[student_id] = {"nom": nom, "prenom": prenom}

            # =========================
            # modules (référentiel)
            # =========================
            if module_id not in modules:
                modules[module_id] = {
                    "numero": row.get("module_numero", ""),
                    "abrev": row.get("module_abrev", ""),
                    "nom": row.get("module_nom", ""),
                    "periodes_total": periodes_total,
                    "matieres": {},
                }

            if matiere_id not in modules[module_id]["matieres"]:
                modules[module_id]["matieres"][matiere_id] = {
                    "abrev": row.get("matiere_abrev", ""),
                    "nom": row.get("matiere_nom", ""),
                }

            # =========================
            # absences (métier)
            # =========================
            absences.setdefault(student_id, {})
            absences[student_id].setdefault(
                module_id, {"nb_absences": 0, "nb_excuses": 0, "par_matiere": {}}
            )

            absences[student_id][module_id]["par_matiere"].setdefault(
                matiere_id, {"abs": 0, "exc": 0}
            )

            # Incréments
            if absence == 0:
                absences[student_id][module_id]["nb_absences"] += 1
                absences[student_id][module_id]["par_matiere"][matiere_id]["abs"] += 1

            if excuse == 1:
                absences[student_id][module_id]["nb_excuses"] += 1
                absences[student_id][module_id]["par_matiere"][matiere_id]["exc"] += 1

    try:
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            process_reader(reader)
    except UnicodeDecodeError:
        with csv_path.open(encoding="cp1252", newline="") as f2:
            reader = csv.DictReader(f2, delimiter=";")
            process_reader(reader)


##FONCTION POUR TESTER L'IMPORTATION
def print_report():
    # Configuration des largeurs
    name_w = 30
    col_w = 18

    # Ordre des modules (par abréviation)
    module_list = sorted(modules.items(), key=lambda kv: kv[1].get("abrev", ""))

    # En-tête
    header = f"{'Élève':{name_w}}"
    for _mid, minfo in module_list:
        header += f" {minfo.get('abrev',''):{col_w}}"
    header += f" {'Total':{col_w}}"
    print(header)

    # Lignes pour chaque élève (tri par nom, prénom)
    for student_id in sorted(eleves.keys(), key=lambda sid: (eleves[sid].get('nom',''), eleves[sid].get('prenom',''))):
        info = eleves[student_id]
        name = f"{info.get('nom','')}, {info.get('prenom','')}"
        row = f"{name:{name_w}}"

        s_abs = 0
        s_exc = 0
        total_periods = 0

        for mid, minfo in module_list:
            periodes_total = minfo.get('periodes_total', 0)
            total_periods += periodes_total

            student_modules = absences.get(student_id, {})
            mdata = student_modules.get(mid)

            if not mdata or (mdata.get('nb_absences', 0) == 0 and mdata.get('nb_excuses', 0) == 0):
                cell = '-'
                row += f" {cell:{col_w}}"
            else:
                nb_abs = mdata.get('nb_absences', 0)
                nb_exc = mdata.get('nb_excuses', 0)
                pct = (nb_abs / periodes_total * 100) if periodes_total > 0 else 0.0
                cell = f"{nb_abs} / {periodes_total} ({pct:.1f}%)"
                row += f" {cell:{col_w}}"
                s_abs += nb_abs
                s_exc += nb_exc

        total_cell = f"{s_abs} / {s_exc} / {total_periods}"
        row += f" {total_cell:{col_w}}"
        print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Charger et afficher les absences depuis un fichier CSV")
    parser.add_argument("--csv", type=Path, default=Path(__file__).parent / "absences.csv", help="Chemin vers le fichier absences.csv")
    args = parser.parse_args()

    try:
        load_csv(args.csv)
    except FileNotFoundError as e:
        print("Erreur lors de l'ouverture du CSV:\n", e, file=sys.stderr)
        print("Placez `absences.csv` dans le même dossier que le script ou lancez-le avec --csv <chemin>", file=sys.stderr)
        sys.exit(1)

    print_report()
