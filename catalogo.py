"""
pedidos_online/catalogo.py  v4
Claves únicas por tab (q_t{idx}_{ean}) — sin DuplicateElementKey.
El carrito toma el MAX entre todos los tabs para cada producto.
"""
import streamlit as st
from db import get_productos
from styles import inject_css, render_hero, render_sticky_footer, get_emoji


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de precio
# ─────────────────────────────────────────────────────────────────────────────

def _precio_final(p_venta: float, descuento: float) -> float:
    if descuento:
        return round(p_venta * (1 - descuento / 100), 2)
    return round(p_venta, 2)


# ─────────────────────────────────────────────────────────────────────────────
# Carrito: lee TODAS las tabs y toma el MAX por producto
# (evita doble-conteo cuando el mismo ean aparece en "Todos" y en su familia)
# ─────────────────────────────────────────────────────────────────────────────

def _cant_producto(ean: str, tab_keys: list[str]) -> int:
    """Devuelve la cantidad máxima registrada para un producto en cualquier tab."""
    return max(
        (st.session_state.get(f"q_{tk}_{ean}", 0) or 0 for tk in tab_keys),
        default=0,
    )


def _resumen_carrito(todos_prods: list[dict], tab_keys: list[str]) -> tuple[int, float]:
    items = total = 0
    for p in todos_prods:
        cant = _cant_producto(p["ean13"], tab_keys)
        if cant > 0:
            items += cant
            total += _precio_final(p["p_venta"], p.get("descuento", 0)) * cant
    return items, round(total, 2)


def _carrito_desde_state(todos_prods: list[dict], tab_keys: list[str]) -> dict:
    carrito = {}
    for p in todos_prods:
        ean  = p["ean13"]
        cant = _cant_producto(ean, tab_keys)
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


# ─────────────────────────────────────────────────────────────────────────────
# Renderizado de productos en una tab
# ─────────────────────────────────────────────────────────────────────────────

def _render_productos(prods: list[dict], tab_key: str, busqueda: str = ""):
    """
    Renderiza productos con key=f"q_{tab_key}_{ean}" — ÚNICO por tab.
    El tab_key es un string corto (t0, t1, t2, …) sin caracteres especiales.
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
            st.markdown(f"**${precio:,.2f}**")
            if dto:
                st.caption(f"-{dto:.0f}%")

        with col_cant:
            # Clave ÚNICA: tab_key + ean — resuelve el DuplicateElementKey
            st.number_input(
                label="cantidad",
                min_value=0, max_value=999, step=1,
                label_visibility="collapsed",
                key=f"q_{tab_key}_{ean}",
            )

        st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# Página principal
# ─────────────────────────────────────────────────────────────────────────────

def page_catalogo():
    inject_css()

    cliente = st.session_state.get("cliente", {})

    # ── Cargar productos (caché de sesión) ────────────────────────────────────
    if "productos_cache" not in st.session_state:
        with st.spinner("Cargando catálogo..."):
            st.session_state.productos_cache = get_productos()
            st.session_state.familias_cache  = sorted({
                p["familia"] for p in st.session_state.productos_cache
                if p.get("familia")
            })

    todos_prods = st.session_state.productos_cache
    familias    = st.session_state.familias_cache

    # ── Lista de tab_keys: "t0" = Todos, "t1".."tN" = familias ───────────────
    # Se guarda en session_state para que _carrito_desde_state la use
    # desde la navegación por query_params (antes de que se recreen los tabs)
    tab_keys = ["t0"] + [f"t{i+1}" for i in range(len(familias))]
    st.session_state["tab_keys"] = tab_keys

    # ── Navegación desde sticky footer (?nav=carrito) ─────────────────────────
    if st.query_params.get("nav") == "carrito":
        st.query_params.clear()
        st.session_state.carrito = _carrito_desde_state(todos_prods, tab_keys)
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

    # ── TABS DINÁMICAS ────────────────────────────────────────────────────────
    tab_labels = ["🛒 Todos"] + [f"{get_emoji(f)} {f}" for f in familias]
    tabs = st.tabs(tab_labels)

    # Tab "Todos" — tab_key = "t0"
    with tabs[0]:
        _render_productos(todos_prods, tab_key="t0", busqueda=busqueda)

    # Tabs por familia — tab_key = "t1", "t2", …
    for i, familia in enumerate(familias):
        with tabs[i + 1]:
            prods_fam = [p for p in todos_prods if p.get("familia") == familia]
            _render_productos(prods_fam, tab_key=f"t{i+1}", busqueda=busqueda)

    # ── Footer de sesión ──────────────────────────────────────────────────────
    st.markdown("---")
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.caption(f"👤 {cliente.get('nombre','')} {cliente.get('apellido','')}")
    with col_b:
        if st.button("🚪 Salir", key="btn_logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.page = "login"
            st.rerun()

    # ── Sticky footer ─────────────────────────────────────────────────────────
    items_cart, total_cart = _resumen_carrito(todos_prods, tab_keys)
    render_sticky_footer(items_cart, total_cart)
