import streamlit as st
import cv2
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Conversor de Imagem para Desenho", layout="centered")

st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 2.2em;
            color: #4B8BBE;
        }
        .subtitle {
            text-align: center;
            color: #555;
        }
        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🎨 Conversor de Imagem para Desenho</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transforme suas fotos em desenhos com 1 clique!</div>', unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📷 Envie sua imagem aqui (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

def converter_para_desenho(imagem):
    imagem_rgb = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
    imagem_cinza = cv2.cvtColor(imagem_rgb, cv2.COLOR_BGR2GRAY)
    imagem_invertida = 255 - imagem_cinza
    imagem_suave = cv2.GaussianBlur(imagem_invertida, (21, 21), sigmaX=0, sigmaY=0)
    desenho = cv2.divide(imagem_cinza, 255 - imagem_suave, scale=256.0)
    return desenho

if uploaded_file is not None:
    imagem = Image.open(uploaded_file)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📸 Imagem Original")
        st.image(imagem, use_column_width=True)

    with col2:
        st.subheader("🖊️ Estilo Desenho")
        desenho = converter_para_desenho(imagem)
        st.image(desenho, use_column_width=True, clamp=True)

    resultado = Image.fromarray(desenho)
    buf = io.BytesIO()
    resultado.save(buf, format="PNG")

    st.download_button(
        "⬇️ Baixar Imagem com Efeito Desenho",
        data=buf.getvalue(),
        file_name="desenho.png",
        mime="image/png"
    )

    st.success("Imagem convertida com sucesso!")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>© 2025 - Desenvolvido por Chance Pascoal Fevereiro</div>", unsafe_allow_html=True)
