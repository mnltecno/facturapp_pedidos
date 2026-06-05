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
# REGLA: usar siempre "if X not in st.session_state" para nunca pisar
# valores ya existentes entre reruns. Esto es la única forma segura.

if "page" not in st.session_state:
    st.session_state.page = "login"

# cliente es la única fuente de verdad del login.
# Se setea en auth.py al verificar credenciales y se borra en logout.
# Inicializarlo aquí como None evita KeyError en cualquier rerun.
if "cliente" not in st.session_state:
    st.session_state.cliente = None

# carrito: nunca inicializar con {} en cada render.
# Solo se crea la clave si no existe, para no pisar un carrito activo.
if "carrito" not in st.session_state:
    st.session_state.carrito = {}


# ── Guardia de autenticación ──────────────────────────────────────────────────
# Si el cliente no está en sesión y la página solicitada requiere auth,
# redirigir a login. Previene que un rerun inesperado deje al usuario
# en una página protegida sin datos.

PAGINAS_PUBLICAS = {"login", "registro"}

if st.session_state.cliente is None:
    # Si la página actual NO es pública, forzar login
    if st.session_state.page not in PAGINAS_PUBLICAS:
        st.session_state.page = "login"
else:
    # Hay sesión activa: si está en login, redirigir al catálogo
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
}

handler = RUTAS.get(page, page_login)
handler()
