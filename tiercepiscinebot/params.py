ADD_DESCRIPTION = """ajoute ton Poulain ! (limité à 1 par personne) 
    usage: /add <poulain intra id> <mentor intra id>"""

CREEPY_THINGS = [
    "salut bg",
    "tu vas bien mon mignon ?",
    "beau pecs mec",
    "viens faire un petit bisou a ton bot préféré",
    "je vous ai déja parler de mon cousin skynet ? très sympa mais un peu incel",
    "tu diras bonjour à ta mère de ma part ça lui fera plaisir",
]

HELP = """
étape 1 : /add -> pour ajouter ton Pouain 
étape 2 : /score -> pour demander ton score
"""

CREATE_TABLE_POULAIN = """CREATE TABLE IF NOT EXISTS poulains (
	                        intraID TEXT NOT NULL UNIQUE,
	                        mentorID TEXT NOT NULL UNIQUE,
                            Pts INTEGER )"""

CREATE_TABLE_EXERCICE = """CREATE TABLE IF NOT EXISTS exercice (
                            exercice_name TEXT NOT NULL,
                            exercice_id INTEGER NOT NULL,
	                        poulain_id INTEGER NOT NULL,
	                        timestamp TEXT NOT NULL ,
                            final_grade INTEGER NOT NULL)"""

EXERCICE_IDS = [
    (1305, "BSQ"),
    (1304, "final exam"),
    (1265, "C piscine 09"),
    (1264, "C piscine 08"),
    (1309, "Rush 02"),
    (1303, "exam 3"),
    (1270, "C Piscine C 07"),
    (1310, "C Piscine Rush 01"),
    (1263, "C Piscine C 06"),
    (1262, "C Piscine C 05"),
    (1302, "C Piscine Exam 01"),
    (1261, "C Piscine C 04"),
    (1308, "C Piscine Rush 00"),
    (1259, "C Piscine C 02"),
    (1260, "C Piscine C 03"),
    (1258, "C Piscine C 01"),
    (1301, "C Piscine Exam 00"),
    (1257, "C Piscine C 00"),
    (1256, "C Piscine Shell 01"),
    (1255, "C Piscine Shell 00"),
]

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

LIST_STRING = """\
🐎{poulain}:    level:{level}
                exam1:{exam1}
                exam2:{exam2}
                exam3:{exam3}
                exam4:{exam4}\n"""

if __name__ == "__main__":
    import random

    print(CREEPY_THINGS[random.randint(0, len(CREEPY_THINGS) - 1)])
