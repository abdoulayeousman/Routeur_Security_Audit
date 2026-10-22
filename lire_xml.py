import sys
import xml.etree.ElementTree as ET

def lire_xml():
    try:
        tree = ET.parse('gatedesc.xml')
        root = tree.getroot()
    except ET.ParseError as error:
        print(f"Erreur d'ouverture: {error}")
        sys.exit()
    except FileNotFoundError:
        print("Fichier introuvable.")
        sys.exit()
    return tree