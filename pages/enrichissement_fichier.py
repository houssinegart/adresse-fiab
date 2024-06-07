import pandas as pd
import requests
import streamlit as st
import time
from fonctions import ApiFunction

"# adresses avec API Adresses "

st.markdown("## Rechercher une adresse ")


adresse = st.text_input('adresse à rechercher ', "2 rue max jacob noisy le sec")

# API BAN
data = ApiFunction.appel_api_raw_ban(adresse)
raw_adresse = ApiFunction.get_dico_from_data(data)


st.header("Reponse API BAN")
if len(adresse)>0:
    st.json(raw_adresse)





######

st.markdown("## rechercher plusieurs adresses ")

limite_max = 10000 # pas plus de 200 lignes par fichier
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
                new_col = ["ban_score","ban_label","ban_numero","ban_rue","ban_code_postal","ban_nom_commune","latitude","longitude"]
                for col in new_col:
                    df[col]=None

                for index, row in df.iterrows():
                    # pause tous les 40 appels
                    if index % 40 == 0 and index != 0:
                        time.sleep(2)
                        st.write(f"{index + 1} adresses traitées ...")
                    adresse = str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4])



                    data = ApiFunction.appel_api_raw_ban(adresse)
                    if data :
                        dico = ApiFunction.get_dico_from_data(data)
                        for col in new_col:
                            df.at[index, col] = dico.get(col)

                for index, row in df.iterrows():
                    depart_init = str(row[3])[0:2]
                    depart_ban = str(row["ban_code_postal"])[0:2]
                    if depart_init != depart_ban :
                        adresse = str(row[1]) + " " + str(row[2]) + " " + str(row[4])
                        data = ApiFunction.appel_api_raw_ban(adresse)
                        if data :
                            dico = ApiFunction.get_dico_from_data(data)
                            for col in new_col:
                                df.at[index, col] = dico.get(col)


                st.success(f'{nb_lignes} lignes chargées ! (max autorisé : {limite_max})')

                map = True
                st.dataframe(df, hide_index=True,height=230)



        st.markdown("# MAP ")

        # Ajout de la colonne couleur
        if map:
            bleu = "#313178"
            rouge = "#c9191e"
            df["color"] = bleu

            st.map( df, latitude='latitude', longitude='longitude', size=60, color = "color")
