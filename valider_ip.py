import ipaddress

def valider_ip(cible):
    try:
        ipaddress.ip_address(cible)
        return True
    except ValueError:
        print("[!] Adresse IP incorrecte : {}".format(cible))
        return False