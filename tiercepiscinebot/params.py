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

LIST_STRING = "🐎{poulain}: level:{level}, exam1:{exam1},\
exam3:{exam3}, exam3:{exam3}, exam4:{exam4}"

if __name__ == "__main__":
    import random

    print(CREEPY_THINGS[random.randint(0, len(CREEPY_THINGS) - 1)])
