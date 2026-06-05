"""
pedidos_online/pedido.py
Confirmación de pedido y pantalla de éxito — diseño Parada Técnica.

FIXES aplicados:
1. q_key usaba formato incorrecto "q_{ean}" en vez de "q_{tab_key}_{ean}".
   Ahora itera sobre tab_keys guardados en session_state para resetear
   TODAS las variantes de clave de cada producto.
2. El carrito se vacía SOLO en dos casos explícitos:
   a) El usuario pulsa "🧹 Vaciar carrito"
   b) El pedido se guarda exitosamente en Supabase
   En cualquier otro caso (error, rerun, navegación) el carrito se preserva.
"""
import urllib.parse
import streamlit as st
from db import guardar_pedido
from styles import inject_css


def _generar_mensaje_whatsapp(cliente: dict, carrito: dict, total: float) -> str:
    nombre_completo = f"{cliente.get('apellido','')}, {cliente.get('nombre','')}"
    lineas = []
    for item in carrito.values():
        lineas.append(
            f"• {item['cantidad']} x {item['descripcion']} "
            f"- ${item['precio_unitario']:,.2f} c/u\n"
            f"  _Subtotal: ${item['subtotal']:,.2f}_"
        )
    return (
        f"📥 *NUEVO PEDIDO ON-LINE*\n"
        f"----------------------------------------\n"
        f"👤 *Cliente:* {nombre_completo}\n"
        f"📱 *Contacto:* {cliente.get('telefono','')}\n"
        f"📧 *Email:* {cliente.get('email','')}\n"
        f"📍 *Dirección (ORS):* {cliente.get('direccion','')}\n"
        f"----------------------------------------\n"
        f"📦 *DETALLE DEL PEDIDO:*\n"
        + "\n".join(lineas) + "\n"
        f"----------------------------------------\n"
        f"💰 *TOTAL A PAGAR: ${total:,.2f}*\n"
        f"----------------------------------------\n"
        f"_Generado automáticamente desde FacturApp Móvil_"
    )


def _resetear_cantidades_catalogo(eans: list[str]) -> None:
    """
    Resetea los number_input del catálogo para los EANs indicados.

    FIX CRÍTICO: el formato de clave es "q_{tab_key}_{ean}", NO "q_{ean}".
    Leemos tab_keys desde session_state (guardado por catalogo.py) para
    resetear todas las variantes (t0, t1, t2, …) de cada producto.
    """
    tab_keys = st.session_state.get("tab_keys", ["t0"])
    for ean in eans:
        for tk in tab_keys:
            widget_key = f"q_{tk}_{ean}"
            if widget_key in st.session_state:
                st.session_state[widget_key] = 0


def page_confirmacion():
    inject_css()

    cliente = st.session_state.get("cliente", {})
    carrito = st.session_state.get("carrito", {})

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='padding:1.2rem 1.2rem .5rem;"
        "font-size:1.4rem;font-weight:900;color:#FF6B35'>🛒 Mi pedido</div>",
        unsafe_allow_html=True,
    )

    if not carrito:
        st.info("El carrito está vacío.")
        if st.button("← Volver al catálogo", use_container_width=True):
            st.session_state.page = "catalogo"
            st.rerun()
        return

    # ── Aviso si falta dirección ──────────────────────────────────────────────
    if not cliente.get("direccion"):
        st.warning(
            "⚠️ **Sin dirección registrada.** La Hoja de Ruta (ORS) necesita "
            "tu dirección para funcionar.",
            icon="📍",
        )
        if st.button("✏️ Completar dirección en mi perfil", use_container_width=True):
            st.session_state.page = "perfil"
            st.rerun()

    # ── Info del cliente ──────────────────────────────────────────────────────
    with st.expander("👤 Datos de entrega", expanded=False):
        st.markdown(
            f"**{cliente.get('apellido')}, {cliente.get('nombre')}**  \n"
            f"📱 {cliente.get('telefono','')}  \n"
            f"📍 {cliente.get('direccion') or '*(sin dirección)*'}"
        )
        if st.button("✏️ Editar perfil", key="btn_editar_perfil", use_container_width=False):
            st.session_state.page = "perfil"
            st.rerun()

    # ── Items del carrito ─────────────────────────────────────────────────────
    total = 0.0
    eans_a_borrar = []

    for ean, item in list(carrito.items()):
        col1, col2, col3 = st.columns([5, 2, 1])
        with col1:
            st.markdown(
                f"<div style='font-weight:600;font-size:.88rem;color:#f0f0f0'>"
                f"{item['descripcion']}</div>"
                f"<div style='font-size:.75rem;color:#666'>"
                f"{item['cantidad']} x ${item['precio_unitario']:,.2f}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<div style='font-weight:800;color:#22c55e;font-size:.95rem;"
                f"text-align:right;padding-top:.2rem'>"
                f"${item['subtotal']:,.2f}</div>",
                unsafe_allow_html=True,
            )
        with col3:
            if st.button("🗑️", key=f"del_{ean}", help="Quitar"):
                eans_a_borrar.append(ean)

        st.markdown(
            "<hr style='margin:.2rem 0;border-color:#1e1e1e'>",
            unsafe_allow_html=True,
        )
        total += item["subtotal"]

    # Procesar borrados — resetea las claves correctas del catálogo
    if eans_a_borrar:
        for ean in eans_a_borrar:
            carrito.pop(ean, None)
        _resetear_cantidades_catalogo(eans_a_borrar)   # FIX: usa tab_keys
        st.session_state.carrito = carrito
        st.rerun()

    # ── Total ─────────────────────────────────────────────────────────────────
    st.markdown(
        f"""<div class="cart-total">
              <div class="ct-label">TOTAL A PAGAR</div>
              <div class="ct-amount">${total:,.2f}</div>
            </div>""",
        unsafe_allow_html=True,
    )

    # ── Observaciones ─────────────────────────────────────────────────────────
    obs = st.text_area(
        "📝 Observaciones (opcional)",
        placeholder="Indicaciones para la entrega...",
        key="obs_pedido", height=70,
    )

    # ── Acciones ──────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 Vaciar carrito", use_container_width=True):
            # Resetea TODAS las claves q_{tab_key}_{ean} del catálogo
            _resetear_cantidades_catalogo(list(carrito.keys()))  # FIX
            st.session_state.carrito = {}
            st.session_state.page = "catalogo"
            st.rerun()
    with col_b:
        if st.button("← Seguir comprando", use_container_width=True):
            # NO vaciamos el carrito: el usuario quiere agregar más cosas
            st.session_state.page = "catalogo"
            st.rerun()

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    if st.button("✅  Confirmar pedido", use_container_width=True, type="primary"):
        with st.spinner("Guardando pedido..."):
            try:
                pedido_id = guardar_pedido(
                    cliente_id=cliente["id"],
                    items=list(carrito.values()),
                    total=round(total, 2),
                )
                # FIX: resetear con la función correcta (usa tab_keys)
                _resetear_cantidades_catalogo(list(carrito.keys()))

                # Guardar info para página de éxito ANTES de vaciar carrito
                st.session_state.pedido_confirmado = {
                    "id":    pedido_id,
                    "total": round(total, 2),
                    "msg":   _generar_mensaje_whatsapp(cliente, carrito, total),
                }

                # Vaciar el carrito SOLO tras confirmación exitosa en Supabase
                st.session_state.carrito = {}
                st.session_state.page = "exito"
                st.rerun()

            except Exception as ex:
                # El carrito NO se vacía si hubo error
                st.error(f"Error al guardar: {ex}")
                st.warning("Tu carrito fue conservado. Podés intentar de nuevo.")


def page_exito():
    inject_css()

    info    = st.session_state.get("pedido_confirmado", {})
    try:
        numero_ws = st.secrets["negocio"]["whatsapp_number"]
    except Exception:
        numero_ws = ""

    st.markdown(
        f"""<div style='text-align:center;padding:2rem 1.2rem 1rem'>
              <div style='font-size:3.5rem'>✅</div>
              <div style='font-size:1.5rem;font-weight:900;color:#FF6B35;margin:.5rem 0'>
                ¡Pedido enviado!</div>
              <div style='color:#888;font-size:.9rem'>
                Pedido #{info.get('id','')} registrado correctamente</div>
              <div style='font-size:1.3rem;font-weight:800;color:#22c55e;margin:.8rem 0'>
                Total: ${info.get('total', 0):,.2f}</div>
            </div>""",
        unsafe_allow_html=True,
    )

    st.info("📲 Tocá el botón para confirmar el pedido por WhatsApp al negocio.")

    if numero_ws:
        msg_encoded = urllib.parse.quote(info.get("msg", ""))
        wa_url = f"https://wa.me/{numero_ws}?text={msg_encoded}"
        st.markdown(
            f"""<div style='padding:.5rem 1.2rem'>
                  <a href="{wa_url}" target="_blank"
                     style="display:block;background:#25d366;color:#fff;
                            text-align:center;border-radius:14px;
                            padding:.85rem;font-weight:900;font-size:1.1rem;
                            text-decoration:none;
                            box-shadow:0 4px 20px rgba(37,211,102,.3)">
                    📲 Enviar por WhatsApp
                  </a>
                </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    if st.button("🛒 Hacer otro pedido", use_container_width=True):
        # NO llamar st.rerun() aquí — el click del botón YA dispara un rerun.
        # Un st.rerun() adicional dentro del handler genera un doble-rerun en
        # Streamlit Cloud que puede cortar la sesión WebSocket en mobile y
        # resetear cliente a None, causando el logout inesperado.
        # Como este botón es el último elemento de la función, no hay nada
        # más que renderizar: el rerun natural del click se encarga de todo.
        for k in ["productos_cache", "familias_cache", "pedido_confirmado"]:
            st.session_state.pop(k, None)
        st.session_state.carrito = {}
        st.session_state.page = "catalogo"
