# pages/1_Control_Trabajo.py
import streamlit as st
import speech_recognition as sr # Si es posible

st.title("Productividad y Ambiente (Ambiente 1)")
st.subheader("Control Multimodal de la Estación")

# --- Modalidad Control (Slider y Botón) ---
st.header("Ajuste de Iluminación y Tiempo")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Luz (Control Deslizante)")
    # Slider de intensidad
    intensidad = st.slider(
        "Intensidad de Luz (%)", 0, 100, st.session_state.sim_status["luz_intensidad"]
    )
    if intensidad != st.session_state.sim_status["luz_intensidad"]:
        st.session_state.sim_status["luz_intensidad"] = intensidad
        st.info(f"Comando Simulado: Intensidad {intensidad}%")

with col2:
    st.markdown("#### Temporizador (Entrada de Texto)")
    # Entrada de texto para el tiempo
    tiempo_input = st.text_input(
        "Establecer Timer (min)",
        str(st.session_state.sim_status["timer_minutos"])
    )
    if st.button("Set Timer"):
        try:
            minutos = int(tiempo_input)
            if minutos >= 0:
                st.session_state.sim_status["timer_minutos"] = minutos
                st.success(f"Comando Simulado: Timer fijado a {minutos} minutos. (El LCD en Wokwi debería mostrar {minutos*60}s)")
            else:
                 st.error("El tiempo debe ser un valor positivo.")
        except ValueError:
            st.error("Por favor, introduce un número válido.")

st.markdown("---")

# --- Modalidad Voz (Simulada) ---
st.header("Comando por Voz (Color de Luz)")
st.info(f"Color de Luz Actual: **{st.session_state.sim_status['luz_color']}**")

if st.button("🎙️ Simular Comando de Voz"):
    # En un proyecto real, se usaría sr.recognize_google()
    # Aquí simulamos la transcripción:
    
    opciones = ["luz cálida", "luz roja", "luz azul"]
    
    # Simple selector para la demo, reemplazar con la lógica de SpeechRecognition
    comando_voz = st.selectbox("Selecciona la voz simulada:", opciones)

    comando = comando_voz.lower()

    if "cálida" in comando:
        st.session_state.sim_status["luz_color"] = "Blanco"
        st.success("Voz Reconocida: Luz de ambiente cambiada a BLANCO.")
    elif "roja" in comando:
        st.session_state.sim_status["luz_color"] = "Rojo"
        st.success("Voz Reconocida: Luz de ambiente cambiada a ROJO.")
    elif "azul" in comando:
        st.session_state.sim_status["luz_color"] = "Azul"
        st.success("Voz Reconocida: Luz de ambiente cambiada a AZUL.")
    else:
        st.warning("Comando de voz no reconocido.")
