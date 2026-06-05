"""
auth.py — Módulo de autenticación para Parada Técnica
Valida credenciales contra Supabase y escribe en st.session_state
de forma segura, sin pisar datos ya existentes.
"""

import streamlit as st
from supabase import create_client, Client


# ---------------------------------------------------------------------------
# Conexión con Supabase (singleton cacheado a nivel de recurso)
# ---------------------------------------------------------------------------

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Crea el cliente de Supabase una sola vez por proceso.
    st.cache_resource NO se borra con reruns, sólo cuando
    el servidor se reinicia — ideal para conexiones.
    """
    url: str = st.secrets["supabase"]["url"]
    key: str = st.secrets["supabase"]["key"]
    return create_client(url, key)


# ---------------------------------------------------------------------------
# Inicialización de claves de sesión (llamar desde app.py, solo una vez)
# ---------------------------------------------------------------------------

def init_auth_state() -> None:
    """
    Inicializa las claves de autenticación en session_state
    SOLO si aún no existen. Nunca sobreescribe valores ya seteados.
    Llamar al inicio de app.py antes de cualquier renderizado.
    """
    defaults = {
        "logged_in": False,
        "cliente_data": None,
        "auth_error": "",
    }
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


# ---------------------------------------------------------------------------
# Lógica de login / logout
# ---------------------------------------------------------------------------

def login(telefono: str, password: str) -> bool:
    """
    Valida el cliente contra la tabla 'clientes' en Supabase.
    Guarda los datos del cliente en session_state si es válido.

    Parámetros
    ----------
    telefono : str  — número de teléfono ingresado por el usuario
    password : str  — contraseña / PIN ingresado

    Retorna
    -------
    bool — True si login exitoso, False si falló
    """
    supabase = get_supabase_client()
    st.session_state["auth_error"] = ""

    try:
        response = (
            supabase.table("clientes")
            .select("*")
            .eq("telefono", telefono.strip())
            .eq("password", password.strip())  # ajustá el campo según tu esquema
            .single()
            .execute()
        )

        if response.data:
            st.session_state["logged_in"] = True
            st.session_state["cliente_data"] = response.data
            return True
        else:
            st.session_state["auth_error"] = "Teléfono o contraseña incorrectos."
            return False

    except Exception as e:
        st.session_state["auth_error"] = f"Error de conexión: {e}"
        return False


def logout() -> None:
    """
    Cierra la sesión limpiando TODAS las claves relevantes,
    incluido el carrito, de forma explícita y controlada.
    """
    keys_to_clear = [
        "logged_in",
        "cliente_data",
        "auth_error",
        "carrito",
        "cantidades",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    # Re-inicializar estado base para que la app no explote
    init_auth_state()


# ---------------------------------------------------------------------------
# Widget de login (UI)
# ---------------------------------------------------------------------------

def mostrar_login() -> None:
    """
    Renderiza el formulario de login.
    Usa st.form para que Streamlit no haga rerun en cada keystroke.
    """
    st.title("🔧 Parada Técnica")
    st.subheader("Ingresá para hacer tu pedido")

    with st.form("form_login", clear_on_submit=False):
        telefono = st.text_input("Teléfono", placeholder="Ej: 1134567890")
        password = st.text_input("Contraseña / PIN", type="password")
        submitted = st.form_submit_button("Ingresar")

    if submitted:
        if not telefono or not password:
            st.warning("Completá todos los campos.")
        else:
            with st.spinner("Verificando..."):
                login(telefono, password)

    if st.session_state.get("auth_error"):
        st.error(st.session_state["auth_error"])
