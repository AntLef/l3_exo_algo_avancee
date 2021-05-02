from heapq import *


def table_frequences(texte):
    table = {}
    for caractere in texte:
        if caractere in table:
            table[caractere] = table[caractere] + 1
        else:
            table[caractere] = 1
    return table


def arbre_huffman(occurrences):
    # Construction d'un tas avec les lettres sous forme de feuilles
    tas = [(occ, lettre) for (lettre, occ) in occurrences.items()]
    heapify(tas)

    # Création de l'arbre
    while len(tas) >= 2:
        print("-", tas)
        occ1, noeud1 = heappop(tas)  # noeud de plus petit poids occ1
        occ2, noeud2 = heappop(tas)  # noeud de deuxième plus petit poids occ2
        print(occ1, noeud1)
        print(occ2, noeud2)
        heappush(tas, (occ1 + occ2, {0: noeud1, 1: noeud2}))
        # ajoute au tas le noeud de poids occ1+occ2 et avec les fils noeud1 et noeud2

    return heappop(tas)[1]


print(arbre_huffman(table_frequences("CHIEN")))
print()


def code_huffman_parcours(arbre, prefixe, code):
    for noeud in arbre:
        if len(arbre[noeud]) == 1:
            code[str(prefixe) + str(noeud)] = arbre[noeud]
        else:
            code_huffman_parcours(arbre[noeud], str(prefixe) + str(noeud), code)


def code_huffman(arbre):
    code = {}
    code_huffman_parcours(arbre, '', code)
    return code


T = arbre_huffman(table_frequences("CHIEN"))
T={'10': 'R', '111': 'B', '0': 'A', '1100': 'C', '1101': 'D'}
C = code_huffman(T)


# print(T)

def encodage(texte,code):
    # code_inv = dict((code[bits], bits) for bits in code)
    code_inv = {j: i for i, j in texte.items()}

    # construit le dictionnaire inverse
    texte_binaire = ''
    for c in texte:
        texte_binaire = texte_binaire + code_inv[c]
    return texte_binaire

"""
def encodage(texte, code):
    print("_________")
    print(code)
    print(texte)
    print("------")
    # code_inv = dict((code[bits], bits) for bits in code)

    code_inv = {j: int(i) for i, j in texte.items()}
    print(code_inv)
    # construit le dictionnaire inverse
    texte_binaire = ''
    for c in texte:
        print(c)
        texte_binaire = texte_binaire + code_inv[c]
    print(texte_binaire)
    return texte_binaire
"""

encodage(C, "CHIEN")
