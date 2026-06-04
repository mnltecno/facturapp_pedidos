"""
pedidos_online/pedido.py
Páginas de confirmación de pedido y pantalla de éxito con WhatsApp.
"""
import urllib.parse
import streamlit as st
from db import guardar_pedido
from styles import inject_css, header


def _generar_mensaje_whatsapp(cliente: dict, carrito: dict, total: float) -> str:
    """Genera el texto del mensaje de WhatsApp con formato exacto."""
    nombre_completo = f"{cliente['apellido']}, {cliente['nombre']}"
    detalle_lineas  = []
    for item in carrito.values():
        linea = (
            f"• {item['cantidad']} x {item['descripcion']} "
            f"- ${item['precio_unitario']:,.2f} c/u\n"
            f"  _Subtotal: ${item['subtotal']:,.2f}_"
        )
        detalle_lineas.append(linea)
    detalle = "\n".join(detalle_lineas)

    msg = (
        f"📥 *NUEVO PEDIDO ON-LINE*\n"
        f"----------------------------------------\n"
        f"👤 *Cliente:* {nombre_completo}\n"
        f"📱 *Contacto:* {cliente.get('telefono','')}\n"
        f"📧 *Email:* {cliente.get('email','')}\n"
        f"📍 *Dirección (ORS):* {cliente.get('direccion','')}\n"
        f"----------------------------------------\n"
        f"📦 *DETALLE DEL PEDIDO:*\n"
        f"{detalle}\n"
        f"----------------------------------------\n"
        f"💰 *TOTAL A PAGAR: ${total:,.2f}*\n"
        f"----------------------------------------\n"
        f"_Generado automáticamente desde FacturApp Móvil_"
    )
    return msg


def page_confirmacion():
    inject_css()
    header("Confirmar pedido", "Revisá tu carrito")

    cliente = st.session_state.get("cliente", {})
    carrito = st.session_state.get("carrito", {})

    if not carrito:
        st.warning("El carrito está vacío.")
        if st.button("← Volver al catálogo"):
            st.session_state.page = "catalogo"
            st.rerun()
        return

    # ── Datos del cliente ─────────────────────────────────────────────────────
    with st.expander("👤 Datos de entrega", expanded=True):
        st.markdown(
            f"**{cliente.get('apellido')}, {cliente.get('nombre')}**  \n"
            f"📱 {cliente.get('telefono','')}  \n"
            f"📍 {cliente.get('direccion','')}"
        )

    # ── Resumen del carrito ───────────────────────────────────────────────────
    st.markdown("### 📦 Detalle del pedido")
    total = 0.0
    for item in carrito.values():
        st.markdown(
            f"""<div class="cart-item">
                <div>
                    <div class="ci-desc">{item['descripcion']}</div>
                    <div class="ci-sub">{item['cantidad']} x ${item['precio_unitario']:,.2f}</div>
                </div>
                <div class="ci-total">${item['subtotal']:,.2f}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        total += item["subtotal"]

    st.markdown(
        f"""<div class="total-bar">
            <div class="label">TOTAL A PAGAR</div>
            <div class="amount">${total:,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Observaciones opcionales ─────────────────────────────────────────────
    obs = st.text_area("📝 Observaciones (opcional)", placeholder="Aclaraciones para el pedido...",
                       key="obs_pedido", height=80)
    st.session_state["obs_pedido_val"] = obs

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Seguir comprando", use_container_width=True):
            st.session_state.page = "catalogo"
            st.rerun()
    with col2:
        if st.button("✅ Confirmar pedido", use_container_width=True, type="primary"):
            with st.spinner("Guardando pedido..."):
                try:
                    pedido_id = guardar_pedido(
                        cliente_id=cliente["id"],
                        items=list(carrito.values()),
                        total=total,
                    )
                    st.session_state.pedido_confirmado = {
                        "id":    pedido_id,
                        "total": total,
                        "msg":   _generar_mensaje_whatsapp(cliente, carrito, total),
                    }
                    st.session_state.carrito = {}
                    st.session_state.page = "exito"
                    st.rerun()
                except Exception as ex:
                    st.error(f"Error al guardar el pedido: {ex}")


def page_exito():
    inject_css()
    header("¡Pedido enviado!", "FacturApp Móvil")

    info    = st.session_state.get("pedido_confirmado", {})
    cliente = st.session_state.get("cliente", {})

    try:
        numero_ws = st.secrets["negocio"]["whatsapp_number"]
    except Exception:
        numero_ws = ""

    st.markdown(
        f"""<div class="success-box">
            <div style="font-size:2.5rem">✅</div>
            <div style="font-size:1.2rem;font-weight:700;margin-top:.5rem">
                Pedido #{info.get('id','')} enviado
            </div>
            <div style="font-size:.9rem;opacity:.8;margin-top:.3rem">
                Total: <strong>${info.get('total',0):,.2f}</strong>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("### Próximo paso: confirmá por WhatsApp")
    st.info("Tocá el botón para enviar el detalle del pedido al negocio por WhatsApp.")

    if numero_ws:
        msg_encoded = urllib.parse.quote(info.get("msg", ""))
        wa_url = f"https://wa.me/{numero_ws}?text={msg_encoded}"
        st.markdown(
            f'<div class="btn-whatsapp"><a href="{wa_url}" target="_blank" '
            f'style="text-decoration:none;color:white;font-weight:700;'
            f'display:block;text-align:center;background:#25d366;padding:.8rem 1rem;'
            f'border-radius:12px;font-size:1.05rem">'
            f'📲 Enviar por WhatsApp</a></div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("Número de WhatsApp no configurado en secrets.toml")

    st.markdown("---")
    if st.button("🛒 Hacer otro pedido", use_container_width=True):
        st.session_state.pop("pedido_confirmado", None)
        for k in list(st.session_state.keys()):
            if k.startswith("cant_"):
                del st.session_state[k]
        st.session_state.page = "catalogo"
        st.rerun()
