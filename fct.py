import datetime,time,requests,json,os,gspread

def wait_hour(HH,MM):
    while(True):
        if datetime.datetime.now().hour == HH:
            if datetime.datetime.now().minute == MM:
                break
        time.sleep(10)

def Lun_Pol(webhook):
    data = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0076D7",
    "summary": "Choix du restauant",
    "sections": [{
        "activityTitle": "Aujourd'hui c'est Lundi, démerdez-vous !",
        "markdown": True
    }]
}
    r = requests.post(webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})

def Mar_Jeu_Pol(webhook,HH,MM,test_mode,creds):
    data = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Choix du restauant",
        "sections": [{
            "activityTitle": "On mange où ?",
            "activitySubtitle": "Fin du vote à 11H, à vous de voter !",
            "markdown": True
        }],
        "potentialAction": [{
            "@type": "OpenUri",
            "name": "Je vote",
            "targets": [{
                "os": "default",
                "uri": "https://forms.gle/W3wUNRmWuVu9ch3S7"
            }]
        }]
    }

    r = requests.post(webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    if not test_mode:
        wait_hour(HH,MM)
    else:
        os.system('pause')

    client = gspread.authorize(creds)
    responses = client.open("Responses").worksheet('Resto Classique')

    data = responses.get_all_records()

    participants_resto_1 = []
    choix = []
    is_follow_majority = []

    for i in range(0,len(data)):
        choix.append(data[i]['Votre choix :'])
        is_follow_majority.append(data[i]["Si votre choix n'est pas sélectionné, venez vous quand même ?"])

    result_choix = {"L'Antenne":choix.count("L'Antenne"),
                "Willgo":choix.count("Willgo"),
                "Les 3 gouts":choix.count("Les 3 gouts"),
                "Le saumon":choix.count("Le saumon"),
                "Crousti Tacos":choix.count("Crousti Tacos")}

    result_choix = dict(sorted(result_choix.items(),key=lambda item: item[1],reverse=True))
    result_list = []
    for key,value in result_choix.items():
        result_list.append(key)
        result_list.append(value)

    Resto_1 = result_list[0]
    Resto_2 = result_list[2]
    nb_pers_Resto_1 = result_list[1]
    nb_pers_Resto_2 = 0
    participants_resto_1 = []
    participants_resto_2 = []

    for i in range(0,len(data)):
        if data[i]['Votre choix :'] == Resto_1:
            participants_resto_1.append(data[i]['Qui êtes-vous ?'])
        elif data[i]["Si votre choix n'est pas sélectionné, venez vous quand même ?"] == "Oui":
            participants_resto_1.append(data[i]['Qui êtes-vous ?'])
            nb_pers_Resto_1+=1

    nb_voitures = int(round((nb_pers_Resto_1/4)+0.4,0))
    participants = ""
    for i in range(0,len(participants_resto_1)):
        participants = participants+participants_resto_1[i]+" "

    
    for i in range(0,len(data)):
        if data[i]['Votre choix :'] == Resto_2 and data[i]["Si votre choix n'est pas sélectionné, venez vous quand même ?"] == "Non":
            participants_resto_2.append(data[i]['Qui êtes-vous ?'])
            nb_pers_Resto_2+=1

    participants_2 = ""
    for i in range(0,len(participants_resto_2)):
        participants_2 = participants_2+participants_resto_2[i]+" "

    nb_voitures_2 = int(round((nb_pers_Resto_2/4)+0.4,0))

    if (nb_pers_Resto_2 == 0):
        data = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Résultats !",
            "sections": [{
                "activityTitle": "Résultats !",
                "facts": [{
                    "name": "Restaurant choisi :",
                    "value": f"{Resto_1}"
                }, {
                    "name": "Nombre de personnes : ",
                    "value": f"{nb_pers_Resto_1}"
                }, {
                    "name": "Il y aura : ",
                    "value": f"{participants}"
                }, {
                    "name": "Convoi : ",
                    "value": f"Prévoyez {nb_voitures} voitures"
                }],
                "markdown": True
            }]
        }
    else:
        data = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Résultats !",
            "sections": [{
                "activityTitle": "Résultats !",
                "facts": [{
                    "name": "Restaurant N°1 choisi :",
                    "value": f"{Resto_1}"
                }, {
                    "name": "Nombre de personnes : ",
                    "value": f"{nb_pers_Resto_1}"
                }, {
                    "name": "Il y aura : ",
                    "value": f"{participants}"
                }, {
                    "name": "Convoi : ",
                    "value": f"Prévoyez {nb_voitures} voitures"
                },
                {
                    "name": "     ",
                    "value": "      "
                },{
                    "name": "     ",
                    "value": "      "
                },{
                    "name": "     ",
                    "value": "      "
                },
                {
                    "name": "Restaurant N°2 choisi :",
                    "value": f"{Resto_2}"
                }, {
                    "name": "Nombre de personnes : ",
                    "value": f"{nb_pers_Resto_2}"
                }, {
                    "name": "Il y aura : ",
                    "value": f"{participants_2}"
                }, {
                    "name": "Convoi : ",
                    "value": f"Prévoyez {nb_voitures_2} voitures"
                }],
                "markdown": True
            }]
        }

    r = requests.post(webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    if not test_mode:
        responses.delete_rows(2,30)
    else:
        print("Mode Test --> Réponses non suprimées")

def Mer_Pol(webhook,HH,MM,test_mode,creds):

    pizzas = {
        'Margarita':[10.5,11],
        'Reine':[10.5,12],
        'Paysanne':[10.5,12],
        'Mexicaine':[10.5,12],
        'Orientale':[10.5,12],
        'Dolce':[11,12],
        'Margarita':[10.5,11],
        'Provençale':[10.5,11.5],
        'Calzone':[12.5,12.5],
        '4 Saisons':[10.5,12.5],
        'Napolitaine':[10.5,12.5],
        'Cabri':[11,13],
        'Catalane':[11,13.5],
        'Hawaienne':[11,13.5],
        'Speciale':[11,14],
        'Niçoise':[11,14],
        '4 Fromages':[11,14.5],
        'Barbecue':[11,14.5],
        'Chicken Run':[11,15],
        'Amiral':[11,15],
        "Hot'Mex":[11,12.5],
        'Carbo':[11,13.5],
        'Roquette':[11,13.5],
        'Trois Champignons':[11,13.5],
        'Norvegienne':[11,14],
        'Maya':[11,14.5],
        "Mont D'or":[11,13.5],
        'Poulette':[11,15],
        'St Jacques':[12,15.5],
        'Campagnarde':[11,14.5],
        'Supreme':[11,15],
        'Savoyarde':[11,15],
        'Raclette':[11,15],
        'Bolognaise':[11,15],
        'Cannibale':[11,15],
        'Flambée':[10,10.5],
        'Alsacienne':[10,11],
        'Flambée Champignons':[11,11.5],
        'Munster':[11,13.5],
        'Calzone Choco':[6.5,6.5],
        'Calzone Choco Banane':[7.5,7.5],
        'Calzone Choco Poire':[7.5,7.5],
        'Burger':[11,15]
    }

    data = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Choix du restauant",
        "sections": [{
            "activityTitle": "Mercredi c'est PIZZA !",
            "activitySubtitle": "Fin du vote à 11H, faite votre choix !",
            "markdown": True
        }],
        "potentialAction": [{
            "@type": "OpenUri",
            "name": "Je choisi ma pizza",
            "targets": [{
                "os": "default",
                "uri": "https://forms.gle/zGqPf6SNeGnfsZHL9"
            }]
        }]
    }

    r = requests.post(webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    if not test_mode:
        wait_hour(HH,MM)
    else:
        os.system('pause')

    client = gspread.authorize(creds)
    responses = client.open("Responses").worksheet('Pizza')

    data = responses.get_all_records()

    total = 0
    petites = []
    grandes = []
    commande_finale = []

    for element in data:
        if element['Votre Taille :'] == "Petite":
            if element['Suppléments :'] != "":
                price = pizzas[element['Votre Pizza :']][0]+1
            else :
                price = pizzas[element['Votre Pizza :']][0]
            commande = f"{element['Qui êtes-vous ?']} - {element['Votre Taille :']} {element['Votre Pizza :']} | Avec : {element['Suppléments :']} | Sans : {element['Sans : ']} | Total : {price}€"
            petites.append(commande)
        else:
            if element['Suppléments :'] != "":
                price = pizzas[element['Votre Pizza :']][1]+1
            else :
                price = pizzas[element['Votre Pizza :']][1]
            commande = f"{element['Qui êtes-vous ?']} - {element['Votre Taille :']} {element['Votre Pizza :']} | Avec : {element['Suppléments :']} | Sans : {element['Sans : ']} | Total : {price}€"
            grandes.append(commande)

        total = total + price
        
    for element in grandes:
        commande_finale.append(element)
    
    for element in petites:
        commande_finale.append(element)

    result = ""
    for element in commande_finale:
        result = result + str(element)+"   \n   \n"
    
    result = result + f"Nombre de pizza : {len(data)}   \n"
    result = result + f"Total : {total}€"

    data = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Choix du restauant",
        "sections": [{
            "activityTitle": "Voici les résultat !",
            "activitySubtitle": f"{result}",
            "markdown": True
        }]
    }

    r = requests.post(webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    if not test_mode:
        responses.delete_rows(2,30)
    else:
        print("Mode Test --> Réponses non suprimées")
    

        