import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- 1. Configuración de la Página y Tema ---
# Usa el modo wide para aprovechar mejor el espacio y un tema claro por defecto.
st.set_page_config(
    page_title="Control Remoto MQTT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Muestra la versión de Python en un área pequeña (opcional, para depuración)
st.sidebar.caption(f"🐍 Python: {platform.python_version()}")

# --- 2. Variables Globales y de Sesión ---
# Inicializa el estado para el cliente MQTT una sola vez
if 'mqtt_client' not in st.session_state:
    st.session_state.mqtt_client = None

broker = "broker.mqttdashboard.com"
port = 1883
client_id = "Pablo_Maza"
topic_control = "pablocontrol"
topic_sensors = "Sensores" # Tópico de ejemplo para recibir datos

# --- 3. Funciones de Callback MQTT ---
def on_publish(client, userdata, result):
    # print("el dato ha sido publicado \n") # No se muestra en la web app, pero útil para terminal
    st.toast("✅ Comando enviado con éxito.", icon='📡')

def on_message(client, userdata, message):
    # La función on_message se ejecuta en un hilo separado
    # En Streamlit, actualizar la UI desde otro hilo requiere un enfoque más complejo,
    # pero para el feedback básico, podemos guardar el mensaje.
    payload = str(message.payload.decode("utf-8"))
    st.session_state.last_message = payload # Guarda el último mensaje recibido
    st.toast(f"📥 Nuevo mensaje: {payload}", icon='📊')

def connect_mqtt():
    """Conecta el cliente MQTT si no está conectado."""
    if st.session_state.mqtt_client is not None:
        try:
            st.session_state.mqtt_client.disconnect() # Desconecta el anterior si existe
        except:
            pass
            
    try:
        client = paho.Client(client_id)
        client.on_publish = on_publish
        client.on_message = on_message
        client.connect(broker, port)
        client.loop_start() # Inicia el hilo para escuchar mensajes
        st.session_state.mqtt_client = client
        st.toast(f"🔗 Conectado a {broker}:{port}", icon='✅')
        return client
    except Exception as e:
        st.error(f"❌ Error al conectar a MQTT: {e}")
        st.session_state.mqtt_client = None
        return None

def publish_mqtt(topic, payload):
    """Publica un mensaje, asegurando que el cliente esté conectado."""
    if st.session_state.mqtt_client is None:
        connect_mqtt()

    if st.session_state.mqtt_client:
        message = json.dumps(payload)
        st.session_state.mqtt_client.publish(topic, message)
    else:
        st.error("No se pudo publicar: Cliente MQTT no está conectado.")


# --- 4. Interfaz de Usuario (UI) ---

# Título y Header con diseño moderno y colores
st.title("💡 Panel de Control MQTT Minimalista")
st.markdown("---") # Separador minimalista

# Contenedor para la conexión (puede ser opcionalmente una barra lateral)
col_conn, col_status = st.columns([1, 4])
with col_conn:
    if st.button("🔌 Conectar/Reconectar", type="primary"):
        connect_mqtt()

with col_status:
    if st.session_state.mqtt_client:
        st.success(f"**Estado:** CONECTADO a **{broker}**")
    else:
        st.warning(f"**Estado:** DESCONECTADO (Intenta Conectar)")
        
st.markdown("---")

# Uso de Tabs para separar el control digital y el analógico
tab1, tab2 = st.tabs(["🚦 Control de Actuadores (Digital)", "🎚️ Control Analógico (Slider)"])

# --- TAB 1: Control Digital (ON/OFF) ---
with tab1:
    st.header("Control de Luces y Actuadores")
    st.markdown("Usa los botones para enviar comandos **ON** u **OFF** al tópico **`pablocontrol`**.")

    col_on, col_off = st.columns(2)
    
    with col_on:
        # Botón ON con color verde (success) y grande
        if st.button('✨ ENCENDER LUCES (ON)', key='btn_on', use_container_width=True, type="primary"):
            act1 = "enciende las luces"
            publish_mqtt(topic_control, {"Act1": act1})
            st.info(f"Comando Digital: **{act1}**")

    with col_off:
        # Botón OFF con color rojo (danger) y grande
        if st.button('🌑 APAGAR LUCES (OFF)', key='btn_off', use_container_width=True, type="secondary"):
            act1 = "apaga las luces"
            publish_mqtt(topic_control, {"Act1": act1})
            st.info(f"Comando Digital: **{act1}**")

    # Muestra un separador
    st.markdown("<br><br>", unsafe_allow_html=True)
    
# --- TAB 2: Control Analógico (Slider) ---
with tab2:
    st.header("Ajuste de Valor Analógico")
    st.markdown("Selecciona un valor y envíalo como JSON al tópico **`pablocontrol`**.")
    
    # Slider con color vivo (usa st.slider por defecto)
    values = st.slider(
        'Rango de Valores (0.0 a 100.0)',
        0.0, 100.0, 50.0, # min, max, valor inicial
        step=0.5,
        format='%.1f'
    )
    
    st.metric(label="Valor Seleccionado", value=f"{values:.1f}")

    # Botón de envío, con color secundario para diferenciarse
    if st.button('📤 Enviar Valor Analógico', key='btn_analog', use_container_width=True, type="primary"):
        publish_mqtt(topic_control, {"Analog": float(values)})
        st.info(f"Comando Analógico: **{values:.1f}**")

st.markdown("---")

# --- 5. Área de Feedback y Mensajes Recibidos ---
st.header("Recibir Datos (Sensores)")
st.markdown("Esta área mostrará el último mensaje recibido en el tópico **`Sensores`**.")

# Inicializa y muestra el último mensaje
if 'last_message' not in st.session_state:
    st.session_state.last_message = "Esperando mensajes..."
    
# Botón para suscribirse al tópico
if st.session_state.mqtt_client:
    if st.button("Suscribirse a Sensores", key='btn_subscribe'):
        st.session_state.mqtt_client.subscribe(topic_sensors)
        st.toast(f"📢 Suscrito al tópico: {topic_sensors}", icon='✅')

st.markdown(f"**Último Mensaje Recibido:**")
st.code(st.session_state.last_message, language='json')
