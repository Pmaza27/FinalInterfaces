# app.py
import streamlit as st
import time

# Inicialización de Estados Simulados
if 'sim_status' not in st.session_state:
    st.session_state.sim_status = {
        "luz_intensidad": 50,  # 0-100
        "luz_color": "Blanco", # Blanco, Rojo, Azul
        "timer_minutos": 0,    # 0-60
        "alarma_estado": "Desarmada", # Armada, Desarmada, Activada
        "sensibilidad": 5     # 1-10
    }

st.set_page_config(layout="wide", page_title="Estación de Trabajo Multimodal")
st.title("💡 Estación de Trabajo y Alarma Multimodal")

# --- Barra Lateral de Estado y Enlace ---
st.sidebar.title("Estado Simulado 🖥️")
st.sidebar.markdown(
    """
    **Para la demostración, el estado en Wokwi
    (el 'mundo físico') debe reflejar estos valores.**
    """
)

st.sidebar.subheader("Ambiente de Trabajo")
st.sidebar.text(f"Intensidad Luz: {st.session_state.sim_status['luz_intensidad']}%")
st.sidebar.text(f"Color Luz: {st.session_state.sim_status['luz_color']}")
st.sidebar.text(f"Timer: {st.session_state.sim_status['timer_minutos']} min")

st.sidebar.subheader("Ambiente de Seguridad")
st.sidebar.text(f"Alarma: {st.session_state.sim_status['alarma_estado']}")
st.sidebar.text(f"Sensibilidad: {st.session_state.sim_status['sensibilidad']}")

# ¡IMPORTANTE! Reemplaza este enlace por el de tu proyecto Wokwi
WOKWI_URL = "https://wokwi.com/projects/YOUR_WOKWI_PROJECT_ID" 
st.sidebar.link_button("Ver Simulación Wokwi", WOKWI_URL)

st.info("Utiliza el menú de la izquierda para navegar entre las páginas (Control y Seguridad).")
