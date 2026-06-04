"""
pedidos_online/catalogo.py
Página de catálogo + carrito interactivo.
"""
import streamlit as st
from db import get_productos, get_familias
from styles import inject_css, header


def _fmt_precio(precio: float, descuento: float) -> str:
    if descuento and descuento > 0:
        final = precio * (1 - descuento / 100)
        return f"${final:,.2f}  <span style='color:#f59e0b;font-size:.75rem'>(-{descuento:.0f}%)</span>"
    return f"${precio:,.2f}"


def _precio_final(precio: float, descuento: float) -> float:
    if descuento and descuento > 0:
        return round(precio * (1 - descuento / 100), 2)
    return round(precio, 2)


def page_catalogo():
    inject_css()

    cliente = st.session_state.get("cliente", {})
    carrito = st.session_state.setdefault("carrito", {})

    header(
        "Catálogo",
        f"Hola, {cliente.get('nombre', '')} 👋"
    )

    # ── Barra de búsqueda ────────────────────────────────────────────────────
    col_b, col_f = st.columns([3, 2])
    with col_b:
        busqueda = st.text_input("🔍 Buscar producto", placeholder="Descripción...",
                                 label_visibility="collapsed", key="busq")
    with col_f:
        familias = ["Todas"] + get_familias()
        familia_sel = st.selectbox("Familia", familias, label_visibility="collapsed", key="fam")

    # ── Cargar productos ──────────────────────────────────────────────────────
    with st.spinner("Cargando catálogo..."):
        productos = get_productos()

    # Filtrar
    if busqueda:
        q = busqueda.lower()
        productos = [p for p in productos if q in p["descripcion"].lower()]
    if familia_sel and familia_sel != "Todas":
        productos = [p for p in productos if p.get("familia") == familia_sel]

    if not productos:
        st.info("No se encontraron productos.")
    else:
        st.markdown(f"**{len(productos)} productos**")

        for prod in productos:
            ean    = prod["ean13"]
            precio = _precio_final(prod["p_venta"], prod["descuento"])
            en_carrito = carrito.get(ean, {}).get("cantidad", 0)

            with st.container():
                c1, c2 = st.columns([4, 3])
                with c1:
                    st.markdown(
                        f"**{prod['descripcion']}**  \n"
                        f"<span style='color:#888;font-size:.75rem'>{prod.get('familia','')}</span>  \n"
                        f"<span style='color:#4ade80;font-size:1rem;font-weight:700'>${precio:,.2f}</span>"
                        + (f"  <span style='color:#f59e0b;font-size:.72rem'>(-{prod['descuento']:.0f}%)</span>"
                           if prod.get("descuento") else ""),
                        unsafe_allow_html=True,
                    )
                with c2:
                    cant_key = f"cant_{ean}"
                    if cant_key not in st.session_state:
                        st.session_state[cant_key] = en_carrito if en_carrito else 1

                    cant = st.number_input(
                        "Cant.", min_value=0, max_value=999,
                        value=st.session_state[cant_key],
                        key=cant_key, label_visibility="collapsed",
                        step=1
                    )
                    if cant > 0:
                        carrito[ean] = {
                            "ean13":           ean,
                            "descripcion":     prod["descripcion"],
                            "cantidad":        cant,
                            "precio_unitario": precio,
                            "subtotal":        round(precio * cant, 2),
                        }
                    elif ean in carrito:
                        del carrito[ean]

                st.divider()

    st.session_state.carrito = carrito

    # ── Botón flotante de carrito ─────────────────────────────────────────────
    items_total = sum(v["cantidad"] for v in carrito.values())
    monto_total = sum(v["subtotal"] for v in carrito.values())

    if items_total > 0:
        st.markdown(
            f'<div class="carrito-badge">🛒 {items_total} items — ${monto_total:,.2f}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        if st.button(f"🛒 Ver carrito y confirmar ({items_total} items)",
                     use_container_width=True, type="primary"):
            st.session_state.page = "confirmacion"
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        for k in ["cliente", "carrito", "page"]:
            st.session_state.pop(k, None)
        st.session_state.page = "login"
        st.rerun()
