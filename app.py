import pandas as pd
import requests
import streamlit as st
import time
from fonctions import ApiFunction

"# adresses avec API Adresses "

st.markdown("## Rechercher une adresse ")

#vérification du code api SIG
code_secret = st.text_input('🔐 API SIG ', "....", type="password")
code_valide = code_secret==st.secrets["password"]


adresse = st.text_input('adresse à rechercher ', "2 rue max jacob noisy le sec")

# API BAN
data = ApiFunction.appel_api_raw_ban(adresse)
raw_adresse = ApiFunction.get_dico_from_data(data)


####  SIG ######

# normaliser l'adresser avec API BAN puis appel SIG

if code_valide:
    adresse_normalise = ApiFunction.get_clean_adress(adresse)
    reponse_sig = ApiFunction.get_data_sig(**adresse_normalise)



col1, col2 = st.columns(2)

with col1:
   st.header("Reponse API BAN")
   st.json(raw_adresse)

with col2:
    st.header("Réponse API SIG")
    if code_valide :
        st.write(reponse_sig)
    else :
        st.write("renseignez une clé sig valide")



######

st.markdown("## rechercher plusieurs adresses ")

limite_max = 200 # pas plus de 200 lignes par fichier
map = False

uploaded_file = st.file_uploader("insérer un fichier texte avec les adresses à rechercher  ", type = "csv")
button = st.button("🚀 go ! ", type="secondary")

if uploaded_file :
    if button :
        with st.spinner('recherche des adresses en cours ...'):
            df = pd.read_csv(uploaded_file, sep=";")

            nb_lignes = df.shape[0]

            if nb_lignes > limite_max:
                st.markdown(f"Le fichier présente{nb_lignes}, le nombre max de lignes autorisés ({limite_max}) est dépassé.")

            else :
                adresses_a_rechercher = df.iloc[:,0].to_list()
                result = []
                for add in adresses_a_rechercher:
                    data = ApiFunction.appel_api_raw_ban(add)
                    if data :
                        dico = ApiFunction.get_dico_from_data(data)

                        # api sig pour les PQV
                        if code_valide:
                            adresse_normalise = ApiFunction.get_clean_adress(add) # c'est pas terribles mais à optimiser plus tard avec dico
                            reponse_sig = ApiFunction.get_data_sig(**adresse_normalise)
                            qpv = reponse_sig.get("code_reponse")
                            dico["QPV"]=qpv

                        result.append(dico)

                st.success(f'{nb_lignes} lignes chargées ! (max autorisé : {limite_max})')
                result = pd.DataFrame(result)
                map = True
                st.dataframe(result, hide_index=True,height=230)



        st.markdown("# MAP ")

        # Ajout de la colonne couleur
        if map:
            bleu = "#313178"
            rouge = "#c9191e"
            if code_valide:
                result["color"]=result["QPV"].apply(lambda x : rouge if x=="OUI" else bleu)
            else :
                result["color"] = bleu

            st.map( result, latitude='latitude', longitude='longitude', size=60, color = "color")
