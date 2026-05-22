%%writefile app.py

import streamlit as st
import pandas as pd
import base64

# ---------------- CONFIG PAGE ----------------
st.set_page_config(
    page_title="Calcul du trajet",
    layout="wide"
)

# ---------------- IMAGE FOND ----------------
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

page_bg_img = f"""
<style>

/* IMAGE FOND */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{get_base64('Photo.png')}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

/* ESPACE HAUT */
.block-container {{
    padding-top: 5rem;
}}

/* TITRE */
h1 {{
    text-align: center;
    color: #111827;
    font-size: 85px;
    font-weight: 900;

    margin-top: 40px;
    margin-bottom: 100px;
}}

/* LABELS */
label, p {{

    font-size: 30px !important;
    color: black !important;
    font-weight: 500 !important;
     margin-left: -300px;
}}

/* SELECTBOX */
.stSelectbox > div > div {{
    font-size: 20px !important;
    min-height: 35px;
    border-radius: 25px;
    background-color: rgba(255,255,255,0.95);

    width: 1100px;
    margin-left: -300px;

    display: flex;
    align-items: center;

    border: 3px solid #d1d5db;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

/* TEXTE INTERNE */
.stSelectbox div[data-baseweb="select"] * {{
    font-size: 20px !important;
}}
/* ALIGNEMENT LISTE DÉROULANTE */
div[data-baseweb="popover"] {{
    margin-left: -300px !important;
}}
/* LARGEUR MENU */
div[data-baseweb="select"] {{
    width: 1000px !important;
}}
/* MENU DÉROULANT EN BAS */
div[data-baseweb="popover"] {{
    top: auto !important;
    bottom: auto !important;
}}
/* LISTE DÉROULANTE */
div[data-baseweb="popover"] {{
    width: 850px !important;
    margin-left: -300px !important;
}}

div[role="listbox"] {{
    width: 850px !important;
    max-width: 850px !important;

    border-radius: 20px !important;
    overflow-x: hidden !important;
}}
/* OPTIONS */
div[role="option"] {{
    font-size: 28px !important;
    padding: 18px 25px !important;
}}
/* BOUTON CALCULER */
.stButton > button {{
    width: 300px;
    height: 50px;

    font-size: 5px !important;
    font-weight: bold;

    border-radius: 25px;
    border: none;

    background-color: transparent;
    color: #1e3a8a;

    display: block;
    margin-left: 400px !important;

    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin-top: 40px;
}}

/* HOVER */
.stButton > button:hover {{
    background-color: rgba(255,255,255,0.2);
    color: #111827;

    border: 3px solid #111827;
}}
/* RESULTATS */
.result-box {{
    background-color: rgba(255,255,255,0.85);

    width: 260px;
    height: 220px;

    border-radius: 25px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    text-align: center;

    padding: 20px;

    margin: auto;

    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

/* DISTANCE */
.distance-text {{
    color: #007BFF;
    font-size: 30px;
    font-weight: bold;
}}

/* PEAGE */
.peage-text {{
    color: #28A745;
    font-size: 30px;
    font-weight: bold;
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------------- LECTURE EXCEL ----------------
df = pd.read_excel("Trajets.xlsx")

# ---------------- LISTE DES SITES ----------------
sites = sorted(set(df["Départ"]).union(set(df["Arrivée"])))

# ---------------- CENTRAGE ----------------
col1, col2, col3 = st.columns([1.5,2,1.5])

with col2:

    # ---------------- TITRE ----------------
    st.title("Calcul du trajet")

    # ---------------- DEPART ----------------
    depart = st.selectbox(
    "Départ",
    sites,
    index=None,
    placeholder="Choisir un site"
)
    # ESPACE
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
# ---------------- ARRIVEE ----------------
    arrivee = st.selectbox(
    "Arrivée",
    sites,
    index=None,
    placeholder="Choisir un site"
)
 # ---------------- BOUTON ----------------
calcul = st.button("Afficher le trajet")

# ---------------- RECHERCHE ----------------
if calcul and depart and arrivee:

    resultat = df[
        (df["Départ"] == depart) &
        (df["Arrivée"] == arrivee)
    ]

    # ---------------- RESULTAT ----------------
    if not resultat.empty:

        c1, espace, c2 = st.columns([1,0.1,1])

        # ---------- DISTANCE ----------
        with c1:
            st.markdown(
                f"""
                <div class="result-box">
                <h2>Distance</h2>

                <span class="distance-text">
                {resultat.iloc[0]['Distance']} km
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ---------- PEAGE ----------
        with c2:
            st.markdown(
                f"""
                <div class="result-box">
                <h2>Péage</h2>

                <span class="peage-text">
                {resultat.iloc[0]['Peage']}
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.error("Trajet introuvable")