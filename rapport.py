def rapport(cible, ports_ouverts, port_http, url_test, code_test, content_type, fabricant, modele, identifiant):
    file = open("router_audit.txt","w", encoding="utf-8")
    file.write("===========================\n"
               "Routeur SECURITY AUDIT\n"
               "===========================\n")
    file.write("Cible :" + str(cible)+ "\n")
    file.write("--------- PORTS TCP --------\n")
    file.write("Ports ouverts :" + str(ports_ouverts)+ "\n")
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
    file.close()