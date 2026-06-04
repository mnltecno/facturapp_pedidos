"""
pedidos_online/app.py
─────────────────────────────────────────────
FacturApp Pedidos Online — App Móvil Streamlit
─────────────────────────────────────────────
Ejecución:
    cd pedidos_online
    streamlit run app.py

Deploy (Streamlit Cloud):
    Subir esta carpeta a GitHub, conectar en share.streamlit.io
    y configurar .streamlit/secrets.toml en el dashboard.
"""
import streamlit as st

st.set_page_config(
    page_title="FacturApp Pedidos",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Importar páginas ──────────────────────────────────────────────────────────
from auth     import page_login, page_registro
from catalogo import page_catalogo
from pedido   import page_confirmacion, page_exito


# ── Inicializar sesión ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "login"


# ── Router principal ──────────────────────────────────────────────────────────
page = st.session_state.page

# Si hay sesión activa y el cliente está en session_state, ir al catálogo
if page == "login" and st.session_state.get("cliente"):
    st.session_state.page = "catalogo"
    page = "catalogo"

RUTAS = {
    "login":        page_login,
    "registro":     page_registro,
    "catalogo":     page_catalogo,
    "confirmacion": page_confirmacion,
    "exito":        page_exito,
}

handler = RUTAS.get(page, page_login)
handler()
