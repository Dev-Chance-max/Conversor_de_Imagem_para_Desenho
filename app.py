import streamlit as st
import cv2
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Conversor para Desenho", layout="centered")

st.title("🎨 Conversor de Imagem para Desenho (Sketch Effect)")
st.write("Envie uma imagem e veja a mágica acontecer!")

uploaded_file = st.file_uploader("📷 Envie sua imagem", type=["jpg", "jpeg", "png"])

def converter_para_desenho(imagem):
    imagem_rgb = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
    imagem_cinza = cv2.cvtColor(imagem_rgb, cv2.COLOR_BGR2GRAY)
    imagem_invertida = 255 - imagem_cinza
    imagem_suave = cv2.GaussianBlur(imagem_invertida, (21, 21), sigmaX=0, sigmaY=0)
    desenho = cv2.divide(imagem_cinza, 255 - imagem_suave, scale=256.0)
    return desenho

if uploaded_file is not None:
    imagem = Image.open(uploaded_file)
    st.image(imagem, caption="Imagem Original", use_column_width=True)

    desenho = converter_para_desenho(imagem)
    st.image(desenho, caption="Imagem Estilo Desenho", use_column_width=True, clamp=True)

    # Download da imagem convertida
    resultado = Image.fromarray(desenho)
    buf = io.BytesIO()
    resultado.save(buf, format="PNG")
    byte_imagem = buf.getvalue()

    st.download_button("⬇️ Baixar Imagem Estilo Desenho", data=byte_imagem, file_name="desenho.png", mime="image/png")
