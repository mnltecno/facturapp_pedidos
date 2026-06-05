"""
pedidos_online/pedido.py
Confirmación de pedido y pantalla de éxito — diseño Parada Técnica.
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

    # ── Info del cliente ──────────────────────────────────────────────────────
    with st.expander("👤 Datos de entrega", expanded=False):
        st.markdown(
            f"**{cliente.get('apellido')}, {cliente.get('nombre')}**  \n"
            f"📱 {cliente.get('telefono','')}  \n"
            f"📍 {cliente.get('direccion','')}"
        )

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

    # Procesar borrados
    for ean in eans_a_borrar:
        del carrito[ean]
        # Resetear el número input en el catálogo
        q_key = f"q_{ean}"
        if q_key in st.session_state:
            st.session_state[q_key] = 0
    if eans_a_borrar:
        st.session_state.carrito = carrito
        st.rerun()

    # ── Total ────────────────────────────────────────────────────────────────
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
            # Resetear todos los inputs del catálogo
            for ean in list(carrito.keys()):
                q_key = f"q_{ean}"
                if q_key in st.session_state:
                    st.session_state[q_key] = 0
            st.session_state.carrito = {}
            st.session_state.page = "catalogo"
            st.rerun()
    with col_b:
        if st.button("← Seguir comprando", use_container_width=True):
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
                # Limpiar carrito e inputs
                for ean in carrito:
                    if f"q_{ean}" in st.session_state:
                        st.session_state[f"q_{ean}"] = 0
                st.session_state.pedido_confirmado = {
                    "id":    pedido_id,
                    "total": round(total, 2),
                    "msg":   _generar_mensaje_whatsapp(cliente, carrito, total),
                }
                st.session_state.carrito = {}
                st.session_state.page = "exito"
                st.rerun()
            except Exception as ex:
                st.error(f"Error al guardar: {ex}")


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
        # Limpiar caché de productos para forzar recarga
        st.session_state.pop("productos_cache", None)
        st.session_state.pop("familias_cache", None)
        st.session_state.pop("pedido_confirmado", None)
        st.session_state.carrito = {}
        st.session_state.page = "catalogo"
        st.rerun()
