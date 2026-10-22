# Router Security Audit

Petit outil Python d'audit d'un routeur réseau, réalisé dans le cadre d'un exercice (TP2).
Il reproduit pas à pas une investigation manuelle, **sans nmap ni outil de scan automatique** : uniquement `socket`, `requests` et `xml.etree.ElementTree`.

> ⚠️ **Avertissement** : utilisez cet outil uniquement sur un équipement qui vous appartient ou que vous êtes explicitement autorisé à tester.

## Objectif

À partir d'une seule adresse IP, le programme :

1. teste une liste de ports TCP (`21, 80, 443, 49152, 49153`) ;
2. envoie une requête HTTP sur chaque port ouvert, jusqu'à trouver un service qui répond ;
3. télécharge le fichier de description `/gatedesc.xml` (service UPnP du routeur) et l'enregistre localement ;
4. analyse ce XML avec `xml.etree.ElementTree` pour en extraire le périphérique, le fabricant, le modèle, le numéro de série et l'identifiant unique (UDN) ;
5. signale que ces informations d'identification sont exposées sans authentification ;
6. génère un rapport `router_audit.txt`.

Le but est de comprendre comment une information apparemment cachée peut être découverte en enchaînant plusieurs observations techniques.

## Structure du projet

| Fichier | Rôle |
|---|---|
| `R_Reseau.py` | Programme principal, appelle toutes les étapes |
| `usage.py` | Affiche l'aide si l'argument est absent |
| `test_tcp.py` | Teste les ports TCP, retourne la liste des ports ouverts |
| `test_http.py` | Requête HTTP sur `http://<cible>:<port>/` |
| `telecharger_gatedesc.py` | Télécharge `http://<cible>:<port>/gatedesc.xml` et l'enregistre |
| `lire_xml.py` | Ouvre et parse `gatedesc.xml` |
| `obtenir_info.py` | Cherche une balise dans l'arbre XML |
| `extraire_infos.py` | Extrait les informations du routeur |
| `fiche_routeur.py` | Affiche la fiche du routeur |
| `analyse_xml.py` | Affiche l'analyse XML et l'alerte de sécurité |
| `rapport.py` | Écrit `router_audit.txt` |

Tous les fichiers doivent rester **dans le même dossier**.

## Installation

Prérequis : Python 3.6 ou plus récent.

```bash
git clone https://github.com/abdoulayeousman/Routeur_Security_Audit.git
cd Routeur_Security_Audit
pip install requests
```

Les modules `sys`, `socket` et `xml.etree.ElementTree` font partie de la bibliothèque standard de Python : il n'y a rien d'autre à installer.

## Lancement

```bash
python R_Reseau.py <adresse_IP>
```

## Options

Le programme n'a qu'**un seul argument**, obligatoire :

| Argument | Description |
|---|---|
| `<adresse_IP>` | Adresse IP du routeur à auditer (ex. `192.168.1.254`) |

Sans argument, le programme affiche :

```
Usage: python R_Reseau.py <adresse_IP>
```

Les ports testés sont définis dans `R_Reseau.py` (appel de `test_tcp`). Pour tester d'autres ports, modifiez cette liste.

## Exemple d'utilisation

```bash
python R_Reseau.py 192.168.1.254
```

Exemple de sortie (valeurs fictives) :

```
===============================
ROUTEUR SECURITY AUDIT
==============================
Cible :  192.168.1.254
==========================
[+] Analyse des port TCP
===============================
Port 21 	 :FERME
Port 80 	 :OUVERT
Port 443 	 :OUVERT
Port 49152 	 :OUVERT
Port 49153 	 :FERME
[+] Essai sur le port 80
...
[+] Essai sur le port 49152
...
URL :  http://192.168.1.254:49152/gatedesc.xml
Code HTTP :  200
===========================
--- FICHE DU ROUTEUR ---
============================
Périphérique : ...
Fabricant    : ...
Modèle       : ... (N° ...)
N° de série  : ...
ID Unique    : uuid:...
[!] Information d'identification Expose
```

Fichiers générés dans le dossier courant :

- `gatedesc.xml` : la réponse XML brute du routeur ;
- `router_audit.txt` : le rapport d'audit (cible, ports ouverts, port HTTP détecté, URL, code HTTP, type de contenu, fabricant, modèle, identifiant).

> 🔒 Ces deux fichiers contiennent le numéro de série et l'identifiant de votre équipement. Ne les publiez pas sur GitHub (voir `.gitignore` ci-dessous).

## Limites du programme

- **Un seul argument** : pas d'option pour choisir les ports, le timeout ou le fichier de sortie.
- **Ports fixes** : la liste est écrite dans le code, et le scan est séquentiel (lent si les ports sont filtrés : 5 s de timeout par port).
- **HTTP uniquement** : les requêtes utilisent `http://`, même sur le port 443 (HTTPS non géré).
- **Ressource unique** : seul `/gatedesc.xml` est recherché ; les routeurs qui exposent leur description ailleurs ne sont pas détectés.
- **Pas de validation de l'adresse IP** : une adresse invalide provoque simplement une erreur de connexion.
- **Fichiers réécrits à chaque exécution** : `gatedesc.xml` et `router_audit.txt` sont écrasés.
- **Outil pédagogique** : ce n'est pas un scanner de vulnérabilités complet.
## Fichier `.gitignore` conseillé

```
gatedesc.xml
router_audit.txt
__pycache__/
```