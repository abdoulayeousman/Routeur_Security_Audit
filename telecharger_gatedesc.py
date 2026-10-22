import requests

def telecharger_gatedesc(cible, port):
    url_test = None
    code_test = None
    print("=============================\n"
          "Fichier Description\n"
          "==============================\n")
    try:

        result = requests.get("http://{}:{}/gatedesc.xml".format(cible, port), timeout=5)
        url_test = result.url
        code_test = result.status_code
        content_test = result.content.decode('utf-8')
        print("URL : ",url_test)
        print("Code HTTP : ",code_test)

        if code_test == 200:
            with open ("gatedesc.xml", 'w') as fichier:
                fichier.write(content_test)
                fichier.close()
    except requests.exceptions.RequestException:
        print("Erreur de connexion")
    return url_test, code_test
