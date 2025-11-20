import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator
import platform # Importamos platform de nuevo para consistencia

# --- 1. Configuración de la Página y Tema ---
st.set_page_config(
    page_title="Control por Voz MQTT",
    layout="centered", # Centered funciona mejor para interfaces modales/por voz
    initial_sidebar_state="collapsed"
)

# --- 2. Variables y Estado de Sesión ---
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None

broker = "broker.mqttdashboard.com"
port = 1883
client_id = "Pablo_Maza_Voz"
topic_control = "pablocontrol"

# --- 3. Funciones de Callback y Conexión MQTT ---
def on_publish(client, userdata, result):
    # Función de callback de publicación modernizada
    st.toast("✅ Comando de voz enviado por MQTT.", icon='📡')

def connect_mqtt():
    """Conecta el cliente MQTT si no está conectado."""
    if st.session_state.mqtt_client is not None:
        try:
            st.session_state.mqtt_client.disconnect()
        except:
            pass
            
    try:
        client = paho.Client(client_id)
        client.on_publish = on_publish
        # Opcional: client.on_message se puede dejar si se planea recibir feedback
        # client.on_message = on_message 
        client.connect(broker, port)
        client.loop_start() 
        st.session_state.mqtt_client = client
        st.toast(f"🔗 Conectado a MQTT para Control por Voz.", icon='✅')
        return client
    except Exception as e:
        st.error(f"❌ Error al conectar a MQTT: {e}")
        st.session_state.mqtt_client = None
        return None

# Conectar al cargar la página si no está conectado
if st.session_state.mqtt_client is None:
    connect_mqtt()

# --- 4. Interfaz de Usuario (UI) ---

st.title("🗣️ Interfaz Multimodal: Control por Voz")
st.markdown("---")

# Uso de columnas para centrar la imagen y el botón
col1, col2, col3 = st.columns([1, 2, 1])

# Imagen de control por voz (Asegúrate de que 'voice_ctrl.jpg' exista)
try:
    image = Image.open('voice_ctrl.jpg')
    with col2:
        st.image(image, width=200)
except FileNotFoundError:
    with col2:
        st.warning("⚠️ No se encontró la imagen 'voice_ctrl.jpg'")
        st.markdown("

[Image of microphone icon]
")


st.markdown("<br>", unsafe_allow_html=True) # Espacio

# Mensaje de instrucción con color
st.info("🎙️ **Toca el botón** y **habla claramente** para enviar comandos MQTT.")

# --- 5. Botón de Reconocimiento de Voz (Bokeh) ---

# Estilo moderno y vivo para el botón Bokeh (similar al 'primary' de Streamlit)
stt_button = Button(
    label=" 🔴 INICIAR ESCUCHA ", 
    width=300, 
    height=60,
    button_type="success" # Usa un color vibrante (primary/success/danger)
)

# El código JavaScript se mantiene igual para la funcionalidad
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false; // Cambiado a false para una sola frase
    recognition.interimResults = false; // Cambiado a false para resultados finales más rápidos
 
    recognition.onstart = function() {
        // Alerta simple o cambio de estado visual (no se muestra bien en Streamlit)
        console.log('Escuchando...');
    };

    recognition.onresult = function (e) {
        var final_value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                final_value += e.results[i][0].transcript;
            }
        }
        if ( final_value != "") {
            // Envía solo el resultado final
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: final_value}));
        }
    }
    
    recognition.onerror = function(e) {
        console.error('Error de reconocimiento de voz:', e.error);
    };

    recognition.start();
    // Añadir un temporizador de parada después de un tiempo para evitar escuchar indefinidamente
    setTimeout(function() {
        recognition.stop();
    }, 5000); // Para después de 5 segundos
    """))

# Centrar el botón Bokeh con columnas
col_btn1, col_btn2, col_btn3 = st.columns([1, 3, 1])
with col_btn2:
    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=100,
        debounce_time=0
    )


# --- 6. Procesamiento del Resultado y Envío MQTT ---
if result:
    if "GET_TEXT" in result:
        comando = result.get("GET_TEXT").strip()
        
        st.markdown("---")
        st.subheader("📝 Comando Detectado")
        
        # Muestra el comando de forma destacada
        st.success(f"**Comando de Voz:** *{comando}*")
        
        # Intenta publicar el mensaje
        if st.session_state.mqtt_client:
            message_payload = {"VoiceCommand": comando}
            try:
                # El cliente ya está conectado y en session_state
                client = st.session_state.mqtt_client
                client.on_publish = on_publish # Asegurar el callback
                
                message = json.dumps(message_payload)
                client.publish(topic_control, message)
                
                st.info(f"Comando enviado a **{topic_control}**: `{message}`")
            except Exception as e:
                st.error(f"❌ Error al publicar: {e}")
                
        else:
            st.warning("🔌 Cliente MQTT no conectado. Intenta reconectar.")
            connect_mqtt()

# --- 7. Tarea opcional (creación de directorio) ---
# Esto es opcional y puede ser eliminado si no se usa para gTTS/guardado
try:
    if not os.path.exists("temp"):
        os.mkdir("temp")
except Exception as e:
    # Capturar el error de la creación del directorio, aunque no es crítico para la UI
    st.caption(f"Error al crear directorio 'temp': {e}")

st.markdown("---")
st.caption(f"ID del Cliente MQTT: {client_id}")
