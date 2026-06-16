"""
pedidos_online/auth.py
Páginas de Login y Registro.
"""
import re
import streamlit as st
from db import get_cliente_by_email, crear_cliente, verificar_password, actualizar_cliente
from styles import inject_css, header


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _valid_email(e: str) -> bool:
    return bool(_EMAIL_RE.match(e.strip()))


def page_login():
    inject_css()
    header("FacturApp Móvil", "Pedidos Online")

    st.markdown("### Iniciar sesión")

    negocio_id = st.session_state.get("negocio_id", "")
    email    = st.text_input("📧 Email", placeholder="tu@email.com", key="li_email")
    password = st.text_input("🔒 Contraseña", type="password", key="li_pass")

    if st.button("Entrar →", use_container_width=True):
        if not email or not password:
            st.error("Completá email y contraseña.")
            return
        with st.spinner("Verificando..."):
            cliente = verificar_password(email.strip().lower(), password, negocio_id)
        if cliente:
            st.session_state.cliente = cliente
            st.session_state.page    = "catalogo"
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
        errores = []
        if not nombre.strip():    errores.append("Nombre requerido")
        if not apellido.strip():  errores.append("Apellido requerido")
        if not email.strip() or not _valid_email(email):
            errores.append("Email inválido")
        if not password:          errores.append("Contraseña requerida")
        if password != password2: errores.append("Las contraseñas no coinciden")
        if len(password) < 6:     errores.append("Contraseña mínimo 6 caracteres")

        if errores:
            for e in errores:
                st.error(e)
            return

        negocio_id = st.session_state.get("negocio_id", "")
        if get_cliente_by_email(email.strip().lower(), negocio_id):
            st.error("Ya existe una cuenta con ese email.")
            return

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
                    negocio_id=negocio_id,
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


def page_perfil():
    inject_css()
    header("Mi perfil", "Editá tus datos de entrega")

    cliente = st.session_state.get("cliente", {})
    if not cliente:
        st.session_state.page = "login"
        st.rerun()
        return

    st.markdown("### 👤 Datos personales")

    col1, col2 = st.columns(2)
    with col1:
        nombre   = st.text_input("Nombre *",   value=cliente.get("nombre", ""),   key="pf_nom")
    with col2:
        apellido = st.text_input("Apellido *", value=cliente.get("apellido", ""), key="pf_ap")

    telefono = st.text_input("📱 Teléfono", value=cliente.get("telefono", ""), key="pf_tel")

    st.markdown("**📍 Dirección de entrega** *(Calle, Número, Ciudad, Provincia)*")
    # Separar dirección existente en partes si es posible
    dir_actual = cliente.get("direccion", "") or ""
    partes_dir = [p.strip() for p in dir_actual.split(",") + ["", "", "", ""]]

    calle     = st.text_input("Calle",    value=partes_dir[0], placeholder="San Martín",   key="pf_calle")
    col3, col4 = st.columns([1, 2])
    with col3:
        numero = st.text_input("Número",  value=partes_dir[1], placeholder="1234",         key="pf_num")
    with col4:
        ciudad = st.text_input("Ciudad",  value=partes_dir[2], placeholder="Ramos Mejía",  key="pf_ciu")
    provincia = st.text_input("Provincia", value=partes_dir[3], placeholder="Buenos Aires", key="pf_prov")

    st.markdown("---")
    st.markdown("### 🔒 Cambiar contraseña *(opcional)*")
    st.caption("Dejá los campos vacíos si no querés cambiarla.")
    pass_nueva   = st.text_input("Nueva contraseña", type="password", key="pf_pass1")
    pass_repetir = st.text_input("Repetir contraseña", type="password", key="pf_pass2")

    col_guardar, col_volver = st.columns(2)
    with col_guardar:
        guardar = st.button("💾 Guardar cambios", use_container_width=True, type="primary")
    with col_volver:
        if st.button("← Volver", use_container_width=True):
            st.session_state.page = "catalogo"
            st.rerun()

    if guardar:
        errores = []
        if not nombre.strip():   errores.append("Nombre requerido")
        if not apellido.strip(): errores.append("Apellido requerido")

        # Validar contraseña solo si se completó algún campo
        cambiar_pass = bool(pass_nueva or pass_repetir)
        if cambiar_pass:
            if len(pass_nueva) < 6:
                errores.append("La contraseña debe tener al menos 6 caracteres")
            if pass_nueva != pass_repetir:
                errores.append("Las contraseñas no coinciden")

        if errores:
            for e in errores:
                st.error(e)
        else:
            partes = [calle.strip(), numero.strip(), ciudad.strip(), provincia.strip()]
            direccion = ", ".join(p for p in partes if p)

            datos = {
                "nombre":    nombre.strip(),
                "apellido":  apellido.strip(),
                "telefono":  telefono.strip(),
                "direccion": direccion,
            }

            # Agregar hash de nueva contraseña si se pidió cambio
            if cambiar_pass:
                from db import hash_password
                email = cliente.get("email", "")
                datos["password_hash"] = hash_password(pass_nueva, email)

            with st.spinner("Guardando..."):
                try:
                    cliente_actualizado = actualizar_cliente(cliente["id"], datos)
                    # Actualizar session_state con los nuevos datos
                    st.session_state.cliente = cliente_actualizado
                    st.success("✅ Perfil actualizado correctamente")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error al guardar: {ex}")
