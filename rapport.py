def rapport(cible, ports_testes, ports_ouverts, port_http, url_test, code_test, content_type, fabricant, modele, identifiant, exposee):
    file = open("router_audit.txt","w", encoding="utf-8")
    file.write("===========================\n"
               "Routeur SECURITY AUDIT\n"
               "===========================\n")
    file.write("Cible :" + str(cible)+ "\n")
    file.write("--------- PORTS TCP --------\n")
    for port in ports_testes:
        if port in ports_ouverts:
            etat = "OUVERT"
        else:
            etat = "FERME"
        file.write("{} : {}\n".format(port, etat))
    file.write("----Service HTTP------\n")
    file.write("Port détecté :" + str(port_http) + "\n")
    file.write("URL :"+ url_test +"\n")
    file.write("-----GATADESC.XML-------\n")
    file.write("Code HTTP : " + str(code_test)+ "\n")
    file.write("Content type : " + str(content_type)+ "\n")
    file.write("----INFORMATION XML ----------\n")
    file.write("Fabricant   :" + str(fabricant)+ "\n")
    file.write("Model : " + str(modele)+ "\n")
    file.write("Identifiant : " +str(identifiant)+ "\n")
    file.write("--- CONCLUSION ---\n")
    if exposee:
        file.write("Le routeur expose son identifiant unique sans authentification via gatedesc.xml (port " + str(port_http) + ").\n"
                   "Risque : n'importe quel appareil du réseau peut identifier précisément l'équipement.\n")
    else:
        file.write("Aucun identifiant exposé n'a été trouvé dans gatedesc.xml.\n")
    file.close()