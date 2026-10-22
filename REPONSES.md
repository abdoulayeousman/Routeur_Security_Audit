# Réponses aux questions du TP : Audit d'un routeur réseau

Les réponses ci-dessous s'appuient sur les résultats obtenus en exécutant le programme sur mon propre routeur (adresse testée : `192.168.1.254`). Les valeurs qui identifient l'équipement (numéro de série, identifiant unique) sont volontairement masquées.

---

## Partie 1 : Récupérer l'adresse IP

**Pourquoi est-il préférable de récupérer l'adresse IP avec `sys.argv` plutôt que de l'écrire directement dans le programme ?**

- Le programme est **réutilisable** : on peut auditer un autre équipement sans modifier le code, en changeant seulement l'argument.
- L'adresse IP d'un routeur peut changer (réseau différent, configuration DHCP) : le code n'a pas à être réécrit à chaque fois.
- Le programme peut être **automatisé** dans un script qui l'appelle sur plusieurs adresses.
- Le code est plus propre et plus sûr à publier : il ne contient pas l'adresse d'un équipement personnel.

---

## Partie 2 : Tester les connexions TCP

Ports testés par mon programme : `21, 80, 443, 49152, 49153`.

>Mon programme teste `49152` et `49153`, qui sont les ports utilisés par mon routeur pour ce service.

**1. Quels ports sont ouverts ?**

Un seul : le port **49152**. Les ports 21, 80, 443 et 49153 sont fermés.

**2. Quels ports semblent correspondre à des services Web ?**

Les ports 80 (HTTP) et 443 (HTTPS) sont les ports Web standards, mais ils sont fermés sur ce routeur. Le port 49152 n'est pas un port Web standard, mais le test HTTP de la partie 3 montre qu'il répond à des requêtes HTTP.

**3. Que remarque-t-on concernant les ports 44152 et 44153 (49152 et 49153 dans mon cas) ?**

Ce sont des **ports élevés**, hors des ports réservés aux services courants. Les ports à partir de 49152 font partie de la plage des ports dynamiques/privés. Ils ne correspondent donc pas à un service connu comme FTP ou HTTP, mais à un service propre à l'équipement, qui mérite d'être examiné.

---

## Partie 3 : Tester le service HTTP

Requête effectuée : `http://192.168.1.254:49152/`

Résultat observé :

- Code HTTP : `404`
- Content-Type : `text/html`
- Contenu de la réponse : une page HTML « 404 Not Found »

**Observation de la réponse**

Le service accepte bien les requêtes HTTP : c'est un serveur Web. Le code 404 signifie que la page d'accueil `/` n'existe pas, mais pas que le service est inutilisable. Il faut chercher une ressource précise.

---

## Partie 4 : Récupérer le fichier de description

Requête effectuée : `http://192.168.1.254:49152/gatedesc.xml`

**1. Quel est le code HTTP ?**

`200` : la ressource existe et est renvoyée.

**2. Quel est le type de contenu retourné ?**

`text/xml;charset="utf-8"`

**3. Le contenu ressemble-t-il à du HTML ?**

Non. C'est un document **XML** (des balises de description du matériel), pas une page Web destinée à un navigateur.

**4. Que peut-on déduire du type de service ?**

Le fichier décrit l'équipement lui-même. Le champ du modèle indique « IGD », pour *Internet Gateway Device*. Cela correspond au protocole **UPnP** (Universal Plug and Play), qui permet à des appareils du réseau local de découvrir et de configurer la passerelle Internet.

---

## Partie 5 : Enregistrer la réponse

Le programme enregistre la réponse du routeur dans le fichier `gatedesc.xml`. Le fichier est écrit en **mode binaire** (`'wb'`) avec la réponse brute, pour qu'il contienne exactement ce que le routeur a envoyé, sans transformation d'encodage.

**1. Le serveur retourne-t-il bien une réponse ?** Oui, avec le code 200.

**2. Quel est le type du contenu ?** `text/xml`.

**3. Quelle est la structure de la réponse ?**

Un document XML hiérarchique : une balise racine qui contient des balises imbriquées. Parmi elles, on trouve notamment les balises `friendlyName`, `manufacturer`, `modelName`, `modelNumber`, `serialNumber` et `UDN`, que le programme extrait.

**4. Pourquoi cette ressource est-elle intéressante pour un audit de sécurité ?**

Elle est accessible **sans authentification** et donne des informations précises sur l'équipement : fabricant, modèle, numéro de série, identifiant unique. Ces informations peuvent servir à préparer une attaque.

---

## Partie 6 : Analyser le XML

Le programme utilise `xml.etree.ElementTree` pour parcourir réellement l'arbre XML (et non une simple recherche de texte). La fonction `obtenir_info` parcourt toutes les balises et retourne le contenu de celle dont le nom correspond.

Informations trouvées :

| Information | Balise XML | Valeur |
|---|---|---|
| Périphérique | `friendlyName` | Internet Home Gateway Device |
| Fabricant | `manufacturer` | Nokia |
| Modèle | `modelName` | IGD Version 2.00 |
| Numéro de modèle | `modelNumber` | 2.00 |
| Numéro de série | `serialNumber` | *(masqué)* |
| Identifiant unique | `UDN` | *(masqué)* |

---

## Partie 7 : Identifier l'information sensible

**1. Quelle information permet d'identifier précisément l'équipement ?**

Le **numéro de série** (`serialNumber`) et l'**identifiant unique** (`UDN`, de la forme `uuid:...`). Chacun est propre à un exemplaire du routeur.

**2. Où apparaît-elle dans le XML ?**

Dans les balises `serialNumber` et `UDN`, qui décrivent l'équipement dans le fichier `gatedesc.xml`.

**3. Cette information devrait-elle être exposée par une ressource HTTP accessible sans authentification ?**

Non. Une information qui identifie un exemplaire précis de l'équipement ne devrait pas être lisible par n'importe quel appareil sans authentification.

**4. Pourquoi cette exposition peut-elle représenter un risque de sécurité ?**

- Elle permet d'**identifier précisément le matériel** (fabricant, modèle, version) et de chercher des vulnérabilités connues qui le concernent.
- Un numéro de série peut servir à **se faire passer pour le propriétaire** auprès d'un support technique (ingénierie sociale).
- L'identifiant unique permet de **reconnaître et suivre** l'équipement.
- Ici, le fichier est accessible depuis le réseau local, donc le risque vient d'un appareil du réseau compromis. Il serait bien plus grave si ce service était accessible depuis Internet.

---

## Partie 8 : Automatiser la recherche

Le programme cherche automatiquement les balises dans le XML et affiche :

```
[+] Analyse XML
Fabricant    :  Nokia
Modéle       :  IGD Version 2.00
Identifiant de l'equipement:  (masqué)
[!] Information d'identification Expose
```

L'alerte `[!]` n'est affichée que si l'identifiant a bien été trouvé dans le XML.

---

## Partie 9 : Gérer les erreurs

Le programme gère ces cas sans afficher de longue erreur Python :

| Cas | Comportement |
|---|---|
| Absence d'argument | Affiche l'usage |
| Adresse IP incorrecte | `[!] Adresse IP incorrecte : ...` |
| Connexion TCP impossible | Le port est affiché `FERME` |
| Timeout HTTP | `[!] Délai dépassé pour <cible>:<port>` |
| Serveur HTTP inaccessible | `[!] Impossible de contacter <cible>:<port>` |
| Réponse HTTP inattendue | `[!] Réponse HTTP inattendue : <code>` |
| XML invalide ou absent | Message d'erreur clair, arrêt propre du programme |

---

## Partie 10 : Rapport d'audit

Le programme génère `router_audit.txt` avec l'état de chaque port, le service HTTP détecté, le code HTTP et le type de contenu de `gatedesc.xml`, les informations XML et une **conclusion** de sécurité.

## Conclusion générale

En enchaînant quatre observations : un port TCP ouvert, un service HTTP qui répond, un fichier de description accessible, puis l'analyse du XML, on découvre sans aucune authentification des informations qui identifient précisément le routeur. Aucune de ces étapes n'est complexe prise seule : c'est leur enchaînement qui révèle l'information.