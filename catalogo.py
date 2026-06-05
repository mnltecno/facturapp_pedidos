"""
pedidos_online/catalogo.py  v2
Sticky footer + contraste corregido + navegación por query params.
"""
import streamlit as st
from db import get_productos, get_familias
from styles import inject_css, render_hero, render_sticky_footer, get_emoji


def _precio_final(p_venta: float, descuento: float) -> float:
    if descuento:
        return round(p_venta * (1 - descuento / 100), 2)
    return round(p_venta, 2)


def _carrito_desde_state(productos_db: list[dict]) -> dict:
    carrito = {}
    for p in productos_db:
        ean  = p["ean13"]
        cant = st.session_state.get(f"q_{ean}", 0) or 0
        if cant > 0:
            precio = _precio_final(p["p_venta"], p.get("descuento", 0))
            carrito[ean] = {
                "ean13":           ean,
                "descripcion":     p["descripcion"],
                "cantidad":        cant,
                "precio_unitario": precio,
                "subtotal":        round(precio * cant, 2),
            }
    return carrito


def _resumen_carrito(productos_db: list[dict]) -> tuple[int, float]:
    items = total = 0
    for p in productos_db:
        cant = st.session_state.get(f"q_{p['ean13']}", 0) or 0
        if cant > 0:
            items += cant
            total += _precio_final(p["p_venta"], p.get("descuento", 0)) * cant
    return items, round(total, 2)


def page_catalogo():
    inject_css()

    cliente    = st.session_state.get("cliente", {})

    # ── Cargar productos (caché de sesión) ────────────────────────────────────
    if "productos_cache" not in st.session_state:
        with st.spinner("Cargando catálogo..."):
            st.session_state.productos_cache = get_productos()
            st.session_state.familias_cache  = sorted(
                {p["familia"] for p in st.session_state.productos_cache
                 if p.get("familia")}
            )
    todos_prods = st.session_state.productos_cache
    familias    = st.session_state.familias_cache

    # ── Navegación desde el sticky footer (query param ?nav=carrito) ──────────
    nav = st.query_params.get("nav", "")
    if nav == "carrito":
        st.query_params.clear()
        st.session_state.carrito = _carrito_desde_state(todos_prods)
        st.session_state.page    = "confirmacion"
        st.rerun()

    # ── Config negocio ────────────────────────────────────────────────────────
    try:
        alias  = st.secrets["negocio"].get("alias",            "mayorista1975")
        numero = st.secrets["negocio"].get("whatsapp_number",  "")
    except Exception:
        alias, numero = "mayorista1975", ""

    # ── HERO ─────────────────────────────────────────────────────────────────
    render_hero(n_productos=len(todos_prods), whatsapp_number=numero, alias=alias)

    # ── Buscador ─────────────────────────────────────────────────────────────
    busqueda = st.text_input(
        "buscar", placeholder="🔍  Buscar producto...",
        label_visibility="collapsed", key="busq_catalogo",
    )

    # ── Filtros por familia ───────────────────────────────────────────────────
    opciones = ["🛒 Todos"] + [f"{get_emoji(f)} {f}" for f in familias]
    try:
        sel = st.pills(
            "Familia", opciones,
            selection_mode="single",
            default="🛒 Todos",
            label_visibility="collapsed",
            key="pill_familia",
        )
        familia_activa = (
            None if (not sel or sel == "🛒 Todos")
            else sel.split(" ", 1)[-1].strip()
        )
    except AttributeError:
        idx = st.radio(
            "Familia", range(len(opciones)),
            format_func=lambda i: opciones[i],
            horizontal=True, index=0,
            label_visibility="collapsed",
            key="radio_familia",
        )
        familia_activa = None if idx == 0 else opciones[idx].split(" ", 1)[-1].strip()

    # ── Filtrar ───────────────────────────────────────────────────────────────
    prods = todos_prods
    if familia_activa:
        prods = [p for p in prods if p.get("familia") == familia_activa]
    if busqueda:
        q = busqueda.strip().lower()
        prods = [p for p in prods
                 if q in p["descripcion"].lower()
                 or q in (p.get("familia") or "").lower()]

    fam_label = familia_activa or "Todos los productos"
    st.markdown(
        f"<div style='padding:.4rem 0 .2rem;font-size:.75rem;color:#555;"
        f"font-weight:600;text-transform:uppercase;letter-spacing:.5px'>"
        f"{fam_label} — {len(prods)} artículos</div>",
        unsafe_allow_html=True,
    )

    # ── Lista de productos ────────────────────────────────────────────────────
    if not prods:
        st.info("Sin resultados para este filtro.")
    else:
        for p in prods:
            ean    = p["ean13"]
            precio = _precio_final(p["p_venta"], p.get("descuento", 0))

            col_info, col_precio, col_cant = st.columns([5, 2, 2])

            with col_info:
                dto_html = (
                    f"<span style='font-size:.65rem;color:#f59e0b'> -"
                    f"{p['descuento']:.0f}%</span>"
                    if p.get("descuento") else ""
                )
                st.markdown(
                    f"<div style='padding:.4rem 0'>"
                    f"<div style='font-weight:600;font-size:.86rem;color:#f0f0f0'>"
                    f"{p['descripcion']}</div>"
                    f"<div style='font-size:.68rem;color:#555;margin-top:1px'>"
                    f"{get_emoji(p.get('familia',''))} {p.get('familia','')}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            with col_precio:
                st.markdown(
                    f"<div style='padding:.5rem 0;font-weight:800;font-size:.9rem;"
                    f"color:#22c55e;text-align:right'>${precio:,.2f}{dto_html}</div>",
                    unsafe_allow_html=True,
                )

            with col_cant:
                # value=0 solo aplica en la primera render (si el key no existe)
                st.number_input(
                    "cant", min_value=0, max_value=999,
                    step=1, label_visibility="collapsed",
                    key=f"q_{ean}",
                )

            st.markdown(
                "<hr style='margin:.1rem 0;border-color:#1a1a1a'>",
                unsafe_allow_html=True,
            )

    # ── Footer de sesión ──────────────────────────────────────────────────────
    st.markdown(
        f"<div style='padding:.5rem 0;font-size:.75rem;color:#444'>"
        f"👤 {cliente.get('nombre','')} {cliente.get('apellido','')}</div>",
        unsafe_allow_html=True,
    )
    if st.button("🚪 Cerrar sesión", key="btn_logout"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state.page = "login"
        st.rerun()

    # ── STICKY FOOTER (siempre al final, fijo en pantalla) ────────────────────
    items_cart, total_cart = _resumen_carrito(todos_prods)
    render_sticky_footer(items_cart, total_cart)
