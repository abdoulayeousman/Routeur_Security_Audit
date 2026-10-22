from obtenir_info import obtenir_info

def extraire_infos(tree):
    peripherique = obtenir_info(tree, 'friendlyName')
    fabricant    = obtenir_info(tree, 'manufacturer')
    modele       = obtenir_info(tree, 'modelName')
    num_modele   = obtenir_info(tree, 'modelNumber')
    serie        = obtenir_info(tree, 'serialNumber')
    identifiant  = obtenir_info(tree, 'UDN')
    return peripherique, fabricant, modele, num_modele, serie, identifiant