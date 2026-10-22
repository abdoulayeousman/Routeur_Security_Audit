import sys

from usage import usage
from valider_ip import valider_ip
from test_tcp import test_tcp
from test_http import test_http
from telecharger_gatedesc import telecharger_gatedesc
from lire_xml import lire_xml
from extraire_infos import extraire_infos
from fiche_routeur import fiche_routeur
from analyse_xml import analyse_xml
from rapport import rapport


args = sys.argv

if len(args) <2:
    usage()
    sys.exit()

cible = args[1]

if not valider_ip(cible):
    sys.exit()

ports_testes = [21,80,443,49152,49153]

print("===============================\n"
      "ROUTEUR SECURITY AUDIT\n"
      "==============================")
print("Cible : ",cible)

ports_ouverts = test_tcp(cible, ports_testes)

if not ports_ouverts:
    print("Aucun port ouvert.")
    sys.exit()

content_type = None
url_test = None
code_test = None

for port_http in ports_ouverts:
    print("[+] Essai sur le port {}".format(port_http))
    test_http(cible, port_http)
    url_test, code_test, content_type = telecharger_gatedesc(cible, port_http)
    if code_test == 200:
        break
else:
    print("gatedesc.xml introuvable sur les ports ouverts.")
    sys.exit()

tree = lire_xml()

if tree is None:
    print("Impossible d'analyser le fichier gatedesc.xml.")
    sys.exit()

peripherique, fabricant, modele, num_modele, serie, identifiant = extraire_infos(tree)

fiche_routeur(peripherique, fabricant, modele, num_modele, serie, identifiant)

exposee = analyse_xml(fabricant, modele, identifiant)

rapport(cible, ports_testes, ports_ouverts, port_http, url_test, code_test, content_type, fabricant, modele, identifiant, exposee)