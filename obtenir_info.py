def obtenir_info(tree, nom_balise):
    for element in tree.iter():
        if element.tag.endswith(nom_balise) and element.text:
            return element.text.strip()
    return "Non trouvé"