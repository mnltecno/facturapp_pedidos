"""
pedidos_online/auth.py
Páginas de Login y Registro.
"""
import re
import streamlit as st
from db import get_cliente_by_email, crear_cliente, verificar_password
from styles import inject_css, header


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _valid_email(e: str) -> bool:
    return bool(_EMAIL_RE.match(e.strip()))


def page_login():
    inject_css()
    header("FacturApp Móvil", "Pedidos Online")

    st.markdown("### Iniciar sesión")

    email    = st.text_input("📧 Email", placeholder="tu@email.com", key="li_email")
    password = st.text_input("🔒 Contraseña", type="password", key="li_pass")

    if st.button("Entrar →", use_container_width=True):
        if not email or not password:
            st.error("Completá email y contraseña.")
            return
        with st.spinner("Verificando..."):
            cliente = verificar_password(email.strip().lower(), password)
        if cliente:
            st.session_state.cliente   = cliente
            st.session_state.page      = "catalogo"
            st.rerun()
        else:
            st.error("Email o contraseña incorrectos.")

    st.divider()
    st.markdown("¿No tenés cuenta?")
    if st.button("Registrarme", use_container_width=True):
        st.session_state.page = "registro"
        st.rerun()


def page_registro():
    inject_css()
    header("Nuevo cliente", "Crear cuenta")

    st.markdown("### Crear cuenta")

    col1, col2 = st.columns(2)
    with col1:
        nombre   = st.text_input("Nombre *", key="rg_nom")
    with col2:
        apellido = st.text_input("Apellido *", key="rg_ap")

    email    = st.text_input("📧 Email *", placeholder="tu@email.com", key="rg_em")
    telefono = st.text_input("📱 Teléfono", placeholder="Ej: 1134567890", key="rg_tel")

    st.markdown("**📍 Dirección** *(formato: Calle, Número, Ciudad, Provincia)*")
    calle     = st.text_input("Calle",     placeholder="San Martín",       key="rg_calle")
    col3, col4 = st.columns([1, 2])
    with col3:
        numero    = st.text_input("Número", placeholder="1234",            key="rg_num")
    with col4:
        ciudad    = st.text_input("Ciudad", placeholder="Ramos Mejía",     key="rg_ciu")
    provincia = st.text_input("Provincia", placeholder="Buenos Aires",     key="rg_prov")

    password  = st.text_input("🔒 Contraseña *", type="password", key="rg_pass")
    password2 = st.text_input("🔒 Repetir contraseña *", type="password", key="rg_pass2")

    if st.button("Crear cuenta →", use_container_width=True):
        # Validaciones
        errores = []
        if not nombre.strip():   errores.append("Nombre requerido")
        if not apellido.strip(): errores.append("Apellido requerido")
        if not email.strip() or not _valid_email(email):
            errores.append("Email inválido")
        if not password:         errores.append("Contraseña requerida")
        if password != password2: errores.append("Las contraseñas no coinciden")
        if len(password) < 6:    errores.append("Contraseña mínimo 6 caracteres")

        if errores:
            for e in errores:
                st.error(e)
            return

        # Verificar si ya existe
        if get_cliente_by_email(email.strip().lower()):
            st.error("Ya existe una cuenta con ese email.")
            return

        # Armar dirección ORS
        partes = [calle.strip(), numero.strip(), ciudad.strip(), provincia.strip()]
        direccion = ", ".join(p for p in partes if p)

        with st.spinner("Creando cuenta..."):
            try:
                cliente = crear_cliente(
                    apellido=apellido,
                    nombre=nombre,
                    telefono=telefono,
                    email=email.strip().lower(),
                    direccion=direccion,
                    password=password,
                )
                st.session_state.cliente = cliente
                st.session_state.page    = "catalogo"
                st.rerun()
            except Exception as ex:
                st.error(f"Error al crear la cuenta: {ex}")

    st.divider()
    if st.button("← Ya tengo cuenta", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
