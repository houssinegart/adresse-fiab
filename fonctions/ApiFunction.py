import requests
import pandas
import streamlit as st

username = st.secrets["username"]
password = st.secrets["password"]

#### API SIG
def get_raw_data_sig(num_voie, nom_voie, code_postal, nom_commune):
    # exemple adresse QPV 8 rue charles baudelaire 93130 Noisy-le-sec / 2 rue max jacob
    nom_voie = nom_voie.replace(" ","%20")
    url = f"https://{username}:{password}@wsa.sig.ville.gouv.fr/service/georeferenceur.json?type_quartier=QP&type_adresse=WSA&adresse[code_postal]={code_postal}&adresse[nom_commune]={nom_commune}&adresse[num_voie]={num_voie}&adresse[nom_voie]={nom_voie}"

    reponse = requests.get(url)
    if reponse.status_code == 200 :
      return reponse.json()
    else :
      return reponse.status_code

def get_data_sig(num_voie, nom_voie, code_postal, nom_commune):

    nom_voie = nom_voie.replace(" ","%20")
    url = f"https://{username}:{password}@wsa.sig.ville.gouv.fr/service/georeferenceur.json?type_quartier=QP&type_adresse=WSA&adresse[code_postal]={code_postal}&adresse[nom_commune]={nom_commune}&adresse[num_voie]={num_voie}&adresse[nom_voie]={nom_voie}"

    reponse = requests.get(url)
    if reponse.status_code == 200 :
        data = reponse.json()
        adresse = data.get("adresse",{}).get("label","")
        code_reponse = data.get("code_reponse","")
        return {"adresse" : adresse, "code_reponse" : code_reponse}
    else :
        return reponse.status_code


def get_clean_adress(adresse):
    ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/'
    params = {
    'q': adresse,
    'limit': 1
    }
    response = requests.get(ADDOK_URL, params=params)
    data = response.json()
    if len(data.get('features')) > 0:
        code_postal = data.get("features",{})[0].get("properties",{}).get("postcode")
        numero = data.get("features",{})[0].get("properties",{}).get("housenumber")
        rue = data.get("features",{})[0].get("properties",{}).get("street")
        nom_commune = data.get("features",{})[0].get("properties",{}).get("city")

        return {
            "num_voie" : numero,
            "nom_voie" : rue,
            "nom_commune" : nom_commune,
            "code_postal" : code_postal,
                }


### fonctions

def appel_api_raw_ban(adresse) :
    ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/'
    params = {
    'q': adresse,
    'limit': 1 # c'est ce paramètre qui permet de chosir combien de résultats on souhaite
    }
    response = requests.get(ADDOK_URL, params=params)
    j = response.json()

    if response.status_code == 200:
      return j
    else :
      print('No result')
      return None

def get_dico_from_data(data):
    features_list = data.get("features", [])
    if features_list :
        score = data.get("features",{})[0].get("properties",{}).get("score","not_found")
        city_code = data.get("features",{})[0].get("properties",{}).get("citycode","not_found")
        code_postal = data.get("features",{})[0].get("properties",{}).get("postcode")
        longitude = data.get("features")[0].get("geometry").get("coordinates")[0]
        latitude = data.get("features")[0].get("geometry").get("coordinates")[1]
        label = data.get("features",{})[0].get("properties",{}).get("label")
        numero = data.get("features",{})[0].get("properties",{}).get("housenumber")
        rue = data.get("features",{})[0].get("properties",{}).get("street")
        context = data.get("features",{})[0].get("properties",{}).get("context")
        nom_commune = data.get("features",{})[0].get("properties",{}).get("city")
        return {
            "score" : round(score,2),
            "code_insee" : city_code,
            "code_postal" : code_postal,
            "label" : label,
            "numero" : numero,
            "rue" : rue,
            "nom_commune" : nom_commune,
            "longitude": longitude,
            "latitude" : latitude
                }
    else :
      return None
