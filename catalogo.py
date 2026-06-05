"""
pedidos_online/catalogo.py
Catálogo Parada Técnica — diseño dark premium.
"""
import streamlit as st
from db import get_productos, get_familias
from styles import inject_css, render_hero, get_emoji


# ────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────

def _precio_final(p_venta: float, descuento: float) -> float:
    if descuento:
        return round(p_venta * (1 - descuento / 100), 2)
    return round(p_venta, 2)


def _carrito_desde_state(productos_db: list[dict]) -> dict:
    """Construye el carrito leyendo los session_state de cada input de cantidad."""
    carrito = {}
    for p in productos_db:
        ean  = p["ean13"]
        cant = st.session_state.get(f"q_{ean}", 0)
        if cant and cant > 0:
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
    """Retorna (total_items, total_$) del carrito actual."""
    items = total = 0
    for p in productos_db:
        cant = st.session_state.get(f"q_{p['ean13']}", 0) or 0
        if cant > 0:
            items += cant
            total += _precio_final(p["p_venta"], p.get("descuento", 0)) * cant
    return items, round(total, 2)


# ────────────────────────────────────────────────────────────────────────────
# Página principal del catálogo
# ────────────────────────────────────────────────────────────────────────────

def page_catalogo():
    inject_css()

    cliente = st.session_state.get("cliente", {})

    # ── Cargar datos (cacheados en session para no recargar en cada rerun) ──
    if "productos_cache" not in st.session_state:
        with st.spinner("Cargando catálogo..."):
            st.session_state.productos_cache  = get_productos()
            st.session_state.familias_cache   = sorted(
                {p["familia"] for p in st.session_state.productos_cache if p.get("familia")}
            )

    todos_prods = st.session_state.productos_cache
    familias    = st.session_state.familias_cache

    # ── Leer config del negocio ──────────────────────────────────────────────
    try:
        alias   = st.secrets["negocio"].get("alias",            "mayorista1975")
        numero  = st.secrets["negocio"].get("whatsapp_number",  "")
    except Exception:
        alias, numero = "mayorista1975", ""

    # ── Resumen carrito ──────────────────────────────────────────────────────
    items_cart, total_cart = _resumen_carrito(todos_prods)

    # ── HERO ─────────────────────────────────────────────────────────────────
    render_hero(
        n_productos    = len(todos_prods),
        whatsapp_number= numero,
        alias          = alias,
        items_carrito  = items_cart,
        total_carrito  = total_cart,
    )

    # ── Buscador ─────────────────────────────────────────────────────────────
    busqueda = st.text_input(
        "buscar", placeholder="🔍  Buscar producto...",
        label_visibility="collapsed", key="busq_catalogo"
    )

    # ── Filtros por familia (pills) ───────────────────────────────────────────
    opciones_pills = ["🛒 Todos"] + [f"{get_emoji(f)} {f}" for f in familias]

    try:
        # st.pills disponible en Streamlit >= 1.38
        sel_pill = st.pills(
            "Familia", opciones_pills,
            selection_mode="single",
            default="🛒 Todos",
            label_visibility="collapsed",
            key="pill_familia",
        )
        familia_activa = (
            None if (not sel_pill or sel_pill == "🛒 Todos")
            else sel_pill.split(" ", 1)[-1].strip()
        )
    except AttributeError:
        # Fallback para versiones antiguas
        sel_idx = st.radio(
            "Familia", range(len(opciones_pills)),
            format_func=lambda i: opciones_pills[i],
            horizontal=True, index=0,
            label_visibility="collapsed", key="radio_familia",
        )
        familia_activa = (
            None if sel_idx == 0
            else opciones_pills[sel_idx].split(" ", 1)[-1].strip()
        )

    # ── Filtrar productos ─────────────────────────────────────────────────────
    prods = todos_prods
    if familia_activa:
        prods = [p for p in prods if p.get("familia") == familia_activa]
    if busqueda:
        q = busqueda.strip().lower()
        prods = [p for p in prods if q in p["descripcion"].lower()
                 or q in (p.get("familia") or "").lower()]

    # ── Header sección ────────────────────────────────────────────────────────
    fam_label = familia_activa or "Todos los productos"
    st.markdown(
        f"<div style='padding:.5rem 1.2rem .2rem;"
        f"font-size:.8rem;color:#555;font-weight:600;text-transform:uppercase;"
        f"letter-spacing:.5px'>{fam_label} — {len(prods)} artículos</div>",
        unsafe_allow_html=True,
    )

    # ── Lista de productos ────────────────────────────────────────────────────
    if not prods:
        st.info("No hay productos para este filtro.")
    else:
        for p in prods:
            ean    = p["ean13"]
            precio = _precio_final(p["p_venta"], p.get("descuento", 0))
            q_key  = f"q_{ean}"

            col_info, col_precio, col_cant = st.columns([5, 2, 2])

            with col_info:
                st.markdown(
                    f"<div style='padding:.45rem 0'>"
                    f"<div style='font-weight:600;font-size:.88rem;color:#f0f0f0;"
                    f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>"
                    f"{p['descripcion']}</div>"
                    f"<div style='font-size:.7rem;color:#555;margin-top:1px'>"
                    f"{get_emoji(p.get('familia',''))} {p.get('familia','')}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            with col_precio:
                st.markdown(
                    f"<div style='padding:.55rem 0;font-weight:800;font-size:.95rem;"
                    f"color:#22c55e;text-align:right'>${precio:,.2f}"
                    + (f"<div style='font-size:.65rem;color:#f59e0b'>-{p['descuento']:.0f}%</div>"
                       if p.get("descuento") else "")
                    + "</div>",
                    unsafe_allow_html=True,
                )

            with col_cant:
                # value=0 solo se aplica la primera vez (si el key no existe aún)
                st.number_input(
                    "cant", min_value=0, max_value=999,
                    step=1, label_visibility="collapsed",
                    key=q_key,
                )

            st.markdown(
                "<hr style='margin:0;border-color:#1e1e1e'>",
                unsafe_allow_html=True,
            )

    # ── Botón fijo de carrito ─────────────────────────────────────────────────
    # Recalcular después de renderizar los inputs
    items_cart2, total_cart2 = _resumen_carrito(todos_prods)

    if items_cart2 > 0:
        st.markdown("<div style='height:4rem'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""<div class="carrito-sticky">
                  <div style="display:flex;align-items:center;
                              justify-content:space-between;gap:.5rem">
                    <span style="font-size:.8rem;color:#666">
                      {items_cart2} artículos seleccionados
                    </span>
                  </div>
                </div>""",
            unsafe_allow_html=True,
        )
        if st.button(
            f"🛒  Ver pedido  ·  ${total_cart2:,.2f}",
            use_container_width=True,
            type="primary",
            key="btn_ver_carrito",
        ):
            # Construir carrito antes de navegar
            st.session_state.carrito = _carrito_desde_state(todos_prods)
            st.session_state.page = "confirmacion"
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        nombre = cliente.get("nombre", "")
        st.markdown(
            f"<div style='font-size:.75rem;color:#555'>👤 {nombre}</div>",
            unsafe_allow_html=True,
        )
    with col_b:
        if st.button("Cerrar sesión", key="btn_logout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.page = "login"
            st.rerun()
