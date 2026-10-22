import requests

def test_http(cible, port):
    content_type = None
    try:
        response = requests.get('http://{}:{}/'.format(cible, port), timeout=5)
        code_http = response.status_code
        content_type = response.headers['content-type']
        type_response = response.content.decode('utf-8')

        print("=========== TESTER LE SERVICE HTTP ===========")
        print("Code HTTP : ",code_http)
        print("Content type : ",content_type)
        print("Contenu de la response : ",type_response)
    except requests.exceptions.ConnectionError :
        print("Erreur de connexion")
    return content_type