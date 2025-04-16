#!/usr/bin/env python3
import os
from openai import OpenAI
import streamlit as st

# 1. Clé API hardcodée (⚠️ Ne pas versionner publiquement)
api_key = OPENAI_KEY
client = OpenAI(api_key=api_key)

# 2. Liste des services
services = [
    "Audit énergétique complet: diagnostic de la consommation et optimisation.",
    "Solutions d’efficacité énergétique (LED, pompes, isolation, CVC).",
    "Installation de panneaux photovoltaïques: conception, pose, maintenance.",
    "Stockage d’énergie par batteries pour lisser la demande.",
    "Bornes de recharge VE: installation & gestion (AC/DC).",
    "Contrats de performance énergétique (CPE) garantissant des économies.",
    "EMS/BMS: supervision & pilotage automatisé de la consommation.",
    "Fourniture d’électricité verte 100 % renouvelable.",
    "Conseil en aides & subventions (CEE, crédits d’impôt).",
    "Programmes de flexibilité & gestion de la demande réseau."
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
    st.image("https://your-domain.com/logo.png", width=150)
    st.title("Ecopillier Sàrl")
    st.write("⚡ Expert en solutions énergétiques")
    st.write("📍 Rue Jean-Charles AMAT 1, 1202 Genève")
    st.write("---")

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
