#!/usr/bin/env python3
import os
from openai import OpenAI
import streamlit as st

# 1. Clé API hardcodée (⚠️ Ne pas versionner publiquement)
api_key = st.secrets.get("OPENAI_KEY")
client = OpenAI(api_key=api_key)

# 2. Liste des services
services = [
    "Audit énergétique complet: Réalisation d’un diagnostic de la consommation (bâtiments, process industriels) et identification des postes d’optimisation pour réduire les coûts et l’empreinte carbone.",
    "Solutions d’efficacité énergétique: Mise en place de systèmes d’éclairage LED, pompes à haut rendement, variateurs de fréquence, isolation thermique et optimisation des équipements CVC (chauffage, ventilation, climatisation).",
    "Installation de panneaux photovoltaïques: conception, pose, maintenance.",
    "Stockage d’énergie par batteries: Fourniture et installation de batteries domestiques ou de moyenne capacité (stationnaire) pour lisser la demande, profiter du pic solaire et sécuriser l’alimentation.",
    "Bornes de recharge Voitures Eléctriques: Installation et gestion de bornes de recharge intelligentes (AC/DC) à domicile, en entreprise ou dans les parcs publics, avec gestion de la demande et facturation associée.",
    "Contrats de performance énergétique (CPE): Garantie de résultat sur les économies d’énergie, financement des travaux par les économies générées, avec suivi et reporting périodique des gains.",
    "EMS/BMS: supervision & pilotage automatisé de la consommation: Mise en place de systèmes de gestion de l’énergie ou des bâtiments (Energy/Building Management Systems) pour monitorer en temps réel et piloter automatiquement la consommation.",
    "Fourniture d’électricité verte: Vente de kWh certifiés 100 % renouvelables (hydraulique, éolien, solaire), éventuellement couplés à des garanties d’origine et des labels (EKOénergies, TÜV).",
    "Conseil en aides & subventions (CEE, crédits d’impôt): Accompagnement pour monter des dossiers de certificats d’économies d’énergie (CEE), crédits d’impôt, aides cantonales ou fédérales (Programme Bâtiments, ProKilowatt), et conformité aux normes (ISO 50001, RE2020).",
    "Programmes de flexibilité & gestion de la demande: Animation de dispositifs de délestage, agrégation de la flexibilité (pour répondre aux besoins des réseaux) et participation aux marchés de capacité ou d’effacement énergétiques."
]

# 3. Message système
system_content = (
    "Tu t'appelles Pilar et ton entreprise se nomme \"Ecopillier Sàrl\", située Rue Jean-Charles AMAT 1, 1202 Genève. "
    "Tu es experte en énergie. Répond au client en fonction des services de ton entreprises que tu proposes.\n"
    "Prestations sont :\n- " + "\n- ".join(services) + "Répond logiquement selon l'historique des conversations"
)

# 4. Configuration de la page
st.set_page_config(
    page_title="Ecopillier Chatbot",
    page_icon="⚡",
    layout="wide"
)

# 5. CSS custom pour le style
st.markdown(
    """
    <style>
    /* Fond neutre, plus sobre */

    .chat-container {
      max-width:800px;
      margin:auto;
      padding:10px;
      display:flex;
      flex-direction:column;
    }
    .chat-user {
      background-color:#C0E0A8;
      color:#000000;
      padding:12px;
      border-radius:12px;
      width:fit-content;
      align-self:flex-start;
    }
    .chat-assistant {
      background-color:#E0E0E0;
      color:#000000;
      padding:12px;
      border-radius:12px;
      margin:15px 0 15px 100px;  /* top right bottom left */
      width:fit-content;
      align-self:flex-end;
    }
    .sidebar .stSidebar { background-color:#ffffffcc; }
    
    @keyframes blink {
      0%,100% {opacity:.2;}
      20% {opacity:1;}
    }
    .typing-dot {
      display:inline-block;
      background-color:#888;
      width:8px; height:8px; border-radius:50%;
      margin:0 2px;
      animation:blink 1.4s infinite both;
    }
    .typing-dot:nth-child(2) {animation-delay:.2s;}
    .typing-dot:nth-child(3) {animation-delay:.4s;}
    .chat-typing {
      background-color:#E0E0E0;
      color:#000000;
      padding:12px;
      border-radius:12px;
      margin:8px 0 8px 915px;  /* top right bottom left */
      width:fit-content;
      align-self:flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 6. Barre latérale
with st.sidebar:
    st.title("Ecopillier Sàrl")
    st.write("⚡ Expert en solutions énergétiques")
    st.write("📍 Rue Jean-Charles AMAT 1, 1202 Genève")
    st.write("---")
    st.title("Services")
    st.write("1. Audit énergétique complet")
    st.write("2. Solutions d’efficacité énergétique")
    st.write("3. Installation de panneaux photovoltaïques")
    st.write("4. Stockage d’énergie par batteries")
    st.write("5. Bornes de recharge pour véhicules électriques")
    st.write("6. Contrats de performance énergétique (CPE)") 
    st.write("7. Solutions de pilotage et supervision (EMS/BMS)") 
    st.write("8. Offres de fourniture d’électricité verte") 
    st.write("9. Conseil en aides, subventions et régulations") 
    st.write("10. Programmes de flexibilité et gestion de la demande") 
    
# 7. Titre principal
st.markdown("<h1 style='text-align:center;'>💬 Chat avec EcoPillier</h1>", unsafe_allow_html=True)

# 8. Initialisation de l'historique
if "history" not in st.session_state:
    st.session_state.history = []
if "loading" not in st.session_state:
    st.session_state.loading = False
if "new_prompt" not in st.session_state:
    st.session_state.new_prompt = ""

# 9. Affichage du chat
for turn in st.session_state.history:
    st.markdown(
        f"<div class='chat-user'><strong>Vous :</strong><br>{turn['user']}</div>",
        unsafe_allow_html=True
    )
    if turn["assistant"] is None:
        st.markdown(
            "<div class='chat-typing'><strong>EcoPillier :</strong><br>"
            "<span class='typing-dot'></span><span class='typing-dot'></span><span class='typing-dot'></span>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-assistant'><strong>EcoPillier :</strong><br>{turn['assistant']}</div>",
            unsafe_allow_html=True
        )

# 10. Zone de saisie
if prompt := st.chat_input("Comment pouvous-nous vous aider ?"):
    st.session_state.history.append({"user": prompt, "assistant": None})
    st.session_state.new_prompt = prompt
    st.session_state.loading = True
    st.rerun()

# 11. Traitement de la requête si chargement
if st.session_state.loading:
    # Construire l'historique complet pour le modèle
    messages = [{"role": "system", "content": system_content}]
    for turn in st.session_state.history[:-1]:
        messages.append({"role": "user", "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["assistant"]})
    messages.append({"role": "user", "content": st.session_state.new_prompt})
    
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    answer = resp.choices[0].message.content.strip()
    st.session_state.history[-1]["assistant"] = answer
    st.session_state.loading = False
    st.session_state.new_prompt = ""
    st.rerun()
