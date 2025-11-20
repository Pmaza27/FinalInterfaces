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

# --- Configuración de la Página y Tema Moderno ---
st.set_page_config(
    page_title="Control por Voz MQTT",
    layout="centered", # Centered para un look enfocado y minimalista
    initial_sidebar_state="collapsed"
)

# --- Funciones de Callback (Funcionalidad Inalterada) ---
def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    st.toast("✅ Comando enviado por MQTT.", icon='📡') # Añadido toast para feedback visual
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    # Mantenemos el st.write para mantener la funcionalidad, pero con estilo de código
    st.code(message_received, language='json')
    

# --- Configuración MQTT (Funcionalidad Inalterada) ---
broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("Pablo_Maza")
client1.on_message = on_message


# --- Interfaz de Usuario (UI) - Diseño Mejorado ---

# Título Principal con Alto Contraste
st.title("🗣️ Interfaces Multimodales")
st.header("⚡️ CONTROL POR VOZ: Envío de Comandos")
st.markdown("---") # Separador minimalista

# Centrar la imagen y darle un contexto
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
try:
    image = Image.open('voice_ctrl.jpg')
    with col_img2:
        st.image(image, width=150, caption="Micrófono Activo") # Reducción de tamaño para minimalismo
except FileNotFoundError:
    with col_img2:
        st.warning("⚠️ No se encontró la imagen 'voice_ctrl.jpg'")
        st.markdown("

[Image of microphone icon]
")
        

st.markdown("<br>", unsafe_allow_html=True) # Espacio

# Instrucción clara y vívida
st.info("📢 **INSTRUCCIÓN:** Pulsa el botón para iniciar la escucha de tu comando.")

# --- Botón de Reconocimiento de Voz (Bokeh) - Diseño Mejorado ---

# Estilo moderno, grande y con color vivo (similar al 'primary' de Streamlit)
stt_button = Button(
    label=" 🎤 INICIAR ESCUCHA ", 
    width=350, 
    height=70,
    button_type="primary" # Color azul/vivo para el botón principal
)

# El código JavaScript se mantiene EXÁCTAMENTE igual
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

# Centrar el botón Bokeh
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


# --- Procesamiento del Resultado y Envío MQTT (Funcionalidad Inalterada) ---
if result:
    if "GET_TEXT" in result:
        comando = result.get("GET_TEXT").strip()
        
        # Muestra el resultado de forma destacada (Alto Contraste)
        st.markdown("---")
        st.subheader("✅ Comando Detectado:")
        st.success(f"**Tu voz dice:** *{comando}*")

        # --- Lógica MQTT Original (Funcionalidad NO CAMBIADA) ---
        client1= paho.Client("Pablo_Maza") # Vuelve a crear el cliente (como en el original)
        client1.on_publish = on_publish # Asigna el callback
        client1.connect(broker,port)
        
        message =json.dumps({"Act1":comando})
        ret= client1.publish("pablocontrol", message)
        
        st.caption(f"Mensaje JSON enviado a 'pablocontrol': `{message}`")


    # --- Lógica de Creación de Directorio (Funcionalidad Inalterada) ---
    try:
        os.mkdir("temp")
    except:
        pass
