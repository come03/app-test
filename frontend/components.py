import streamlit as st
import requests

st.title("Prévision de la Demande")
st.write("Entrez le nom du produit et les ventes passées.")

product_name = st.text_input("Nom du produit")
sales_data = st.text_area("Ventes passées (séparées par des virgules)")

if st.button("Prédire"):
    try:
        sales_list = [int(x.strip()) for x in sales_data.split(",") if x.strip().isdigit()]
        if not sales_list:
            st.error("Merci d'entrer des valeurs numériques.")
        else:
            response = requests.post("http://localhost:8000/predict/", json={
                "product_name": product_name,
                "past_sales": sales_list
            })
            if response.status_code == 200:
                forecast = response.json()["forecast"]
                st.success(f"Prévision de la demande pour {product_name} : {forecast} unités")
            else:
                st.error("Erreur lors de la prédiction.")
    except Exception as e:
        st.error(f"Erreur : {e}")