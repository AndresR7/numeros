# pip install tensorflow==2.17.0
# pip install streamlit
# pip install streamlit-drawable-canvas

import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import os

# Mostrar logo
st.image('logo.gif', width="container")  # Usar "container" en lugar de use_container_width

# Título
st.title("ALFREDO DIAZ CLARO 2024")

# Lista de modelos disponibles
modelos_disponibles = ['numerosD1.keras', 'numerosC2.keras', 'numerosC3.keras']

# Función para cargar modelos con verificación
def load_model_from_file(modelo_path):
    if not os.path.exists(modelo_path):
        st.error(f"❌ Archivo no encontrado: {modelo_path}")
        return None
    try:
        modelobien = load_model(modelo_path)
        modelobien.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy']
        )
        return modelobien
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo '{modelo_path}': {e}")
        return None

# Cargar los modelos
modelo_d1 = load_model_from_file('numerosD1.keras')
modelo_c2 = load_model_from_file('numerosC2.keras')
modelo_c3 = load_model_from_file('numerosC3.keras')

# Verificar si todos los modelos se cargaron correctamente
if not all([modelo_d1, modelo_c2, modelo_c3]):
    st.stop()  # Detiene la ejecución si faltan modelos

# Lienzo para dibujar
st.title("🖌️ Dibuja un número")
canvas_result = st_canvas(
    fill_color="white",
    stroke_width=10,
    stroke_color="black",
    background_color="white",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)

# Mostrar mensaje personalizado según la probabilidad
def mostrar_mensaje(probabilidad, modelo_nombre):
    if probabilidad < 0.8:
        return f" ({modelo_nombre}): ❗ No identificado adecuadamente, intenta nuevamente"
    else:
        return f" ({modelo_nombre}): ✅ Alta confianza ({probabilidad:.2f})"

# Botón de predicción
if st.button("Predecir"):
    if canvas_result.image_data is not None:
        # Procesar la imagen
        img = Image.fromarray(canvas_result.image_data.astype('uint8'))
        img = img.convert('L')  # Escala de grises
        img = img.resize((28, 28))  # Redimensionar a 28x28

        img_array = np.array(img)
        img_array = 255 - img_array  # Invertir colores
        img_array = img_array.reshape((1, 28, 28, 1)) / 255.0  # Normalizar

        with st.spinner('🔍 Realizando predicciones...'):
            # Modelo D1
            prediction_d1 = modelo_d1.predict(img_array)
            predicted_class_d1 = np.argmax(prediction_d1)
            predicted_probability_d1 = np.max(prediction_d1)

            # Modelo C2
            prediction_c2 = modelo_c2.predict(img_array)
            predicted_class_c2 = np.argmax(prediction_c2)
            predicted_probability_c2 = np.max(prediction_c2)

            # Modelo C3
            prediction_c3 = modelo_c3.predict(img_array)
            predicted_class_c3 = np.argmax(prediction_c3)
            predicted_probability_c3 = np.max(prediction_c3)

        # Mostrar resultados en columnas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🧠 Modelo D1")
            st.write(f"Predicción: {predicted_class_d1}" + mostrar_mensaje(predicted_probability_d1, "D1"))

        with col2:
            st.subheader("🧠 Modelo C2")
            st.write(f"Predicción: {predicted_class_c2}" + mostrar_mensaje(predicted_probability_c2, "C2"))

        with col3:
            st.subheader("🧠 Modelo C3")
            st.write(f"Predicción: {predicted_class_c3}" + mostrar_mensaje(predicted_probability_c3, "C3"))

    else:
        st.warning("⚠️ Por favor, dibuja un número antes de predecir.")
