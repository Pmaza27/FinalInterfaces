# pages/2_Seguridad.py
import streamlit as st

st.title("Alarma y Seguridad (Ambiente 2)")
st.subheader("Control Multimodal de la Alarma")

# --- Modalidad Botón ---
st.header("Armado/Desarmado Rápido")
alarma_actual = st.session_state.sim_status["alarma_estado"]

col_armar, col_desarmar = st.columns(2)

with col_armar:
    if col_armar.button("🛡️ Armar Sistema", type="primary"):
        st.session_state.sim_status["alarma_estado"] = "Armada"
        st.success("Comando Simulado: Sistema de Alarma ARMADO. (El Buzzer en Wokwi debería estar SILENCIADO)")
with col_desarmar:
    if col_desarmar.button("🔓 Desarmar Sistema"):
        st.session_state.sim_status["alarma_estado"] = "Desarmada"
        st.success("Comando Simulado: Sistema DESARMADO.")

st.markdown("---")

# --- Modalidad Texto (Código de Desactivación) ---
st.header("Desactivación por Código")
codigo_input = st.text_input("Ingresa el código secreto para Desactivar:", type="password")

if st.button("Verificar Código", key="btn_codigo"):
    CODIGO_SECRETO = "9876"
    
    if codigo_input == CODIGO_SECRETO:
        st.session_state.sim_status["alarma_estado"] = "Desarmada"
        st.success("Código Correcto. Alarma DESARMADA.")
    else:
        # Simula la activación del Buzzer si está armada
        if st.session_state.sim_status["alarma_estado"] == "Armada":
            st.session_state.sim_status["alarma_estado"] = "Activada"
            st.error("Código Incorrecto. 🚨 Alarma ACTIVADA. (El Buzzer en Wokwi debería sonar)")
        else:
            st.warning("Código Incorrecto.")

st.markdown("---")

# --- Modalidad Número (Sensibilidad) ---
st.header("Ajuste de Sensibilidad")

sensibilidad_input = st.number_input(
    "Ajuste de Sensibilidad del Sensor (1 = Baja, 10 = Alta)",
    min_value=1,
    max_value=10,
    value=st.session_state.sim_status["sensibilidad"],
    step=1
)

if sensibilidad_input != st.session_state.sim_status["sensibilidad"]:
    st.session_state.sim_status["sensibilidad"] = sensibilidad_input
    if sensibilidad_input <= 3:
        sens = "Baja"
    elif sensibilidad_input <= 7:
        sens = "Media"
    else:
        sens = "Alta"
    st.success(f"Comando Simulado: Sensibilidad fijada a {sens} ({sensibilidad_input}).")
