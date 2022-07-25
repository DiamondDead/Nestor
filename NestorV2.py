import json, datetime
from oauth2client.service_account import ServiceAccountCredentials
from fct import Lun_Pol,Mar_Jeu_Pol, Mer_Pol

is_test = False
# Google Sheet login
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

# var ms teams
with open("webhook.json",'r') as f:
    webhook_links = json.load(f)
if not is_test:
    # EEPI Channel
    webhook_url = webhook_links["EEPI_Channel"]
    today = datetime.datetime.today().weekday()
else:
    # Test Channel
    webhook_url = webhook_links["Test_Channel"]
    today = 1

# today = 1
try:
    if today == 0 :
        Lun_Pol(webhook_url)
    elif today == 1 or today == 3 or today == 4:
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        Mar_Jeu_Pol(webhook_url,11,00,is_test,creds)
    elif today == 2:
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        Mer_Pol(webhook_url,11,00,is_test,creds)
    # elif today == 4:
    #     print("Sondage BBQ")
    else :
        print("Pas de sondage")
    print("Done")
except Exception as e:
    print("Une erreur s'est produite !")
    print(e)
