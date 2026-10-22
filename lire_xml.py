import xml.etree.ElementTree as ET

def lire_xml():
    try:
        tree = ET.parse('gatedesc.xml')
        root = tree.getroot()
    except ET.ParseError as error:
        print(f"[!] XML invalide : {error}")
        return None
    except FileNotFoundError:
        print("[!] Fichier gatedesc.xml introuvable.")
        return None
    return tree
