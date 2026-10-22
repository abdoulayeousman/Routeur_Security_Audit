import requests

def telecharger_gatedesc(cible, port):
    url_test = None
    code_test = None
    content_type = None
    print("=============================\n"
          "Fichier Description\n"
          "==============================\n")
    try:

        result = requests.get("http://{}:{}/gatedesc.xml".format(cible, port), timeout=5)
        url_test = result.url
        code_test = result.status_code
        content_type = result.headers.get('content-type')
        print("URL : ",url_test)
        print("Code HTTP : ",code_test)
        print("Content type : ",content_type)

        if code_test == 200:
            with open ("gatedesc.xml", 'wb') as fichier:
                fichier.write(result.content)
        else:
            print("[!] Réponse HTTP inattendue : {}".format(code_test))
    except requests.exceptions.Timeout:
        print("[!] Délai dépassé pour {}:{}".format(cible, port))
    except requests.exceptions.RequestException:
        print("[!] Impossible de contacter {}:{}".format(cible, port))
    return url_test, code_test, content_type