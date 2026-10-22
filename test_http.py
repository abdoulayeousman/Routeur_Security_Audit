import requests

def test_http(cible, port):
    content_type = None
    try:
        response = requests.get('http://{}:{}/'.format(cible, port), timeout=5)
        code_http = response.status_code
        content_type = response.headers.get('content-type')
        type_response = response.text

        print("=========== TESTER LE SERVICE HTTP ===========")
        print("Code HTTP : ",code_http)
        print("Content type : ",content_type)
        print("Contenu de la response : ",type_response)
    except requests.exceptions.Timeout :
        print("[!] Délai dépassé pour {}:{}".format(cible, port))
    except requests.exceptions.RequestException :
        print("[!] Impossible de contacter {}:{}".format(cible, port))
    return content_type