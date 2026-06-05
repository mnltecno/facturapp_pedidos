"""
pedidos_online/catalogo.py  v3
Filtrado por st.tabs nativo — sin CSS forzado en inputs/botones.
"""
import streamlit as st
from db import get_productos
from styles import inject_css, render_hero, render_sticky_footer, get_emoji


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

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


def _render_productos(prods: list[dict], busqueda: str = ""):
    """
    Renderiza filas de productos con selector numérico.
    Las cantidades se guardan automáticamente en st.session_state
    con key=f"q_{ean13}" — persisten al cambiar de tab.
    """
    if busqueda:
        q = busqueda.strip().lower()
        prods = [p for p in prods if q in p["descripcion"].lower()]

    if not prods:
        st.info("Sin productos para este filtro.")
        return

    for p in prods:
        ean    = p["ean13"]
        precio = _precio_final(p["p_venta"], p.get("descuento", 0))
        dto    = p.get("descuento", 0) or 0

        col_desc, col_precio, col_cant = st.columns([5, 2, 2])

        with col_desc:
            st.markdown(f"**{p['descripcion']}**")
            st.caption(f"{get_emoji(p.get('familia',''))} {p.get('familia','')}")

        with col_precio:
            if dto:
                st.markdown(f"**${precio:,.2f}**")
                st.caption(f"-{dto:.0f}%")
            else:
                st.markdown(f"**${precio:,.2f}**")

        with col_cant:
            # value=0 solo se aplica la primera vez que el key no existe
            st.number_input(
                label="cantidad",
                min_value=0, max_value=999, step=1,
                label_visibility="collapsed",
                key=f"q_{ean}",
            )

        st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# Página principal
# ─────────────────────────────────────────────────────────────────────────────

def page_catalogo():
    inject_css()

    cliente = st.session_state.get("cliente", {})

    # ── Cargar productos (caché de sesión para no recargar en cada rerun) ─────
    if "productos_cache" not in st.session_state:
        with st.spinner("Cargando catálogo..."):
            st.session_state.productos_cache = get_productos()
            # Familias únicas, ordenadas, sin vacíos
            fams = sorted({
                p["familia"] for p in st.session_state.productos_cache
                if p.get("familia")
            })
            st.session_state.familias_cache = fams

    todos_prods = st.session_state.productos_cache
    familias    = st.session_state.familias_cache

    # ── Navegación desde el sticky footer (?nav=carrito) ─────────────────────
    if st.query_params.get("nav") == "carrito":
        st.query_params.clear()
        st.session_state.carrito = _carrito_desde_state(todos_prods)
        st.session_state.page    = "confirmacion"
        st.rerun()

    # ── Config del negocio ────────────────────────────────────────────────────
    try:
        alias  = st.secrets["negocio"].get("alias",           "mayorista1975")
        numero = st.secrets["negocio"].get("whatsapp_number", "")
    except Exception:
        alias, numero = "mayorista1975", ""

    # ── Hero ──────────────────────────────────────────────────────────────────
    render_hero(n_productos=len(todos_prods), whatsapp_number=numero, alias=alias)

    # ── Buscador global ───────────────────────────────────────────────────────
    busqueda = st.text_input(
        "buscar",
        placeholder="🔍  Buscar producto...",
        label_visibility="collapsed",
        key="busq_catalogo",
    )

    # ── TABS DE FAMILIAS (nativas Streamlit) ──────────────────────────────────
    # "🛒 Todos" primero, luego una tab por cada familia con su emoji
    tab_labels = ["🛒 Todos"] + [
        f"{get_emoji(f)} {f}" for f in familias
    ]
    tabs = st.tabs(tab_labels)

    # Tab "Todos"
    with tabs[0]:
        _render_productos(todos_prods, busqueda)

    # Una tab por familia
    for i, familia in enumerate(familias):
        with tabs[i + 1]:
            prods_familia = [
                p for p in todos_prods if p.get("familia") == familia
            ]
            _render_productos(prods_familia, busqueda)

    # ── Footer de sesión ──────────────────────────────────────────────────────
    st.markdown("---")
    cols = st.columns([3, 2])
    with cols[0]:
        st.caption(f"👤 {cliente.get('nombre','')} {cliente.get('apellido','')}")
    with cols[1]:
        if st.button("🚪 Salir", key="btn_logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.page = "login"
            st.rerun()

    # ── Sticky footer — siempre fijo al pie ───────────────────────────────────
    items_cart, total_cart = _resumen_carrito(todos_prods)
    render_sticky_footer(items_cart, total_cart)
