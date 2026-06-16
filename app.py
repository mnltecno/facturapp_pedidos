"""
pedidos_online/app.py
─────────────────────────────────────────────
FacturApp Pedidos Online — App Móvil Streamlit
─────────────────────────────────────────────
Arquitectura multi-tenant: cada distribuidor tiene su URL única.
Ejemplo: ?negocio=parada-tecnica-a3f8

Ejecución local:
    cd pedidos_online
    streamlit run app.py -- --negocio=mi-negocio-xxxx

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
from auth     import page_login, page_registro, page_perfil
from catalogo import page_catalogo
from pedido   import page_confirmacion, page_exito


# ── Leer negocio_id desde la URL ─────────────────────────────────────────────
# El negocio_id llega como parámetro de URL: ?negocio=parada-tecnica-a3f8
# Se guarda en session_state para no perderlo entre reruns.
# Si no está en la URL ni en la sesión → pantalla de error.

if "negocio_id" not in st.session_state:
    negocio_param = st.query_params.get("negocio", "")
    st.session_state.negocio_id = negocio_param.strip()

negocio_id = st.session_state.negocio_id

if not negocio_id:
    st.error(
        "⚠️ **URL inválida.** Esta app requiere un código de negocio en la URL.\n\n"
        "Pedile a tu proveedor el enlace correcto.\n\n"
        "*Ejemplo: `https://tu-app.streamlit.app?negocio=mi-negocio-xxxx`*"
    )
    st.stop()


# ── Inicializar sesión ────────────────────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "login"

if "cliente" not in st.session_state:
    st.session_state.cliente = None

if "carrito" not in st.session_state:
    st.session_state.carrito = {}


# ── Guardia de autenticación ──────────────────────────────────────────────────

PAGINAS_PUBLICAS = {"login", "registro"}

if st.session_state.cliente is None:
    if st.session_state.page not in PAGINAS_PUBLICAS:
        st.session_state.page = "login"
else:
    if st.session_state.page == "login":
        st.session_state.page = "catalogo"


# ── Router principal ──────────────────────────────────────────────────────────
page = st.session_state.page

RUTAS = {
    "login":        page_login,
    "registro":     page_registro,
    "catalogo":     page_catalogo,
    "confirmacion": page_confirmacion,
    "exito":        page_exito,
    "perfil":       page_perfil,
}

handler = RUTAS.get(page, page_login)
handler()
