"""
pedidos_online/catalogo.py  v7
─────────────────────────────────────────────────────────────────────────────
FIXES aplicados:
1. number_input recibe value= explícito desde session_state.
2. tab_keys persistido en session_state para que pedido.py resetee bien.
3. El carrito NO se pisa en cada render.
4. Restaurado render_sticky_footer para el botón fijo al pie de pantalla.
─────────────────────────────────────────────────────────────────────────────
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


def _cant_producto(ean: str, tab_keys: list[str]) -> int:
    """MAX entre todos los tabs del mismo producto (evita doble conteo)."""
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


def _ir_a_carrito(todos_prods: list[dict], tab_keys: list[str]):
    """Construye el carrito y navega a confirmación — todo dentro de Streamlit."""
    st.session_state.carrito = _carrito_desde_state(todos_prods, tab_keys)
    st.session_state.page    = "confirmacion"
    st.rerun()


def _btn_carrito(label: str, key: str, todos_prods: list[dict], tab_keys: list[str]):
    """Botón verde de ver pedido."""
    if st.button(label, key=key, use_container_width=True, type="primary"):
        _ir_a_carrito(todos_prods, tab_keys)


# ─────────────────────────────────────────────────────────────────────────────
# Renderizado de productos
# ─────────────────────────────────────────────────────────────────────────────

def _render_productos(prods: list[dict], tab_key: str, busqueda: str = ""):
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
            widget_key = f"q_{tab_key}_{ean}"

            # FIX: value= explícito desde session_state.
            # Sin esto, al volver del carrito al catálogo el widget
            # se reinicia a 0 aunque la clave ya exista en session_state,
            # porque Streamlit solo garantiza persistencia si el widget
            # se renderizó en el rerun inmediatamente anterior.
            valor_actual = st.session_state.get(widget_key, 0) or 0

            st.number_input(
                label="cantidad",
                min_value=0, max_value=999, step=1,
                value=valor_actual,
                label_visibility="collapsed",
                key=widget_key,
            )

        st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# Página principal
# ─────────────────────────────────────────────────────────────────────────────

def page_catalogo():
    inject_css()

    cliente = st.session_state.get("cliente", {})

    # ── Cargar catálogo (caché de sesión, filtrado por negocio_id) ───────────
    # FIX: "if not in" garantiza que no se pisa la caché en reruns.
    negocio_id = st.session_state.get("negocio_id", "")
    if "productos_cache" not in st.session_state:
        with st.spinner("Cargando catálogo..."):
            st.session_state.productos_cache = get_productos(negocio_id)
            st.session_state.familias_cache  = sorted({
                p["familia"] for p in st.session_state.productos_cache
                if p.get("familia")
            })

    todos_prods = st.session_state.productos_cache
    familias    = st.session_state.familias_cache

    # Tab keys: t0 = Todos, t1..tN = familias
    tab_keys = ["t0"] + [f"t{i+1}" for i in range(len(familias))]

    # FIX: persistir tab_keys en session_state para que pedido.py
    # pueda leer el mismo formato de clave al resetear cantidades.
    st.session_state["tab_keys"] = tab_keys

    # ── Config del negocio ────────────────────────────────────────────────────
    try:
        alias  = st.secrets["negocio"].get("alias",           "mayorista1975")
        numero = st.secrets["negocio"].get("whatsapp_number", "")
    except Exception:
        alias, numero = "mayorista1975", ""

    # ── Hero ──────────────────────────────────────────────────────────────────
    render_hero(n_productos=len(todos_prods), whatsapp_number=numero, alias=alias)

    # ── BOTÓN DE CARRITO SUPERIOR ─────────────────────────────────────────────
    items_top, total_top = _resumen_carrito(todos_prods, tab_keys)
    if items_top > 0:
        st.markdown("")
        _btn_carrito(
            label       = f"🛒  Ver pedido  ({items_top} items)  ·  ${total_top:,.2f}",
            key         = "btn_cart_top",
            todos_prods = todos_prods,
            tab_keys    = tab_keys,
        )
        st.markdown("")

    # ── Buscador ──────────────────────────────────────────────────────────────
    busqueda = st.text_input(
        "buscar",
        placeholder="🔍  Buscar producto...",
        label_visibility="collapsed",
        key="busq_catalogo",
    )

    # ── TABS DE FAMILIAS ──────────────────────────────────────────────────────
    tab_labels = ["🛒 Todos"] + [f"{get_emoji(f)} {f}" for f in familias]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        _render_productos(todos_prods, tab_key="t0", busqueda=busqueda)

    for i, familia in enumerate(familias):
        with tabs[i + 1]:
            prods_fam = [p for p in todos_prods if p.get("familia") == familia]
            _render_productos(prods_fam, tab_key=f"t{i+1}", busqueda=busqueda)

    # ── BOTÓN STICKY AL PIE (estilo PedidoYa) ────────────────────────────────
    # render_sticky_footer usa CSS position:fixed — siempre visible al scrollear.
    # Retorna True si el usuario lo presionó.
    items_bot, total_bot = _resumen_carrito(todos_prods, tab_keys)
    if render_sticky_footer(items_bot, total_bot):
        _ir_a_carrito(todos_prods, tab_keys)

    # ── Footer de sesión ──────────────────────────────────────────────────────
    st.markdown("---")
    col_a, col_b, col_c = st.columns([3, 1, 1])
    with col_a:
        st.caption(f"👤 {cliente.get('nombre','')} {cliente.get('apellido','')}")
    with col_b:
        if st.button("✏️ Perfil", key="btn_perfil", use_container_width=True):
            st.session_state.page = "perfil"
            st.rerun()
    with col_c:
        if st.button("🚪 Salir", key="btn_logout", use_container_width=True):
            for k in ["cliente", "carrito", "productos_cache",
                      "familias_cache", "tab_keys", "pedido_confirmado"]:
                st.session_state.pop(k, None)
            st.session_state.page = "login"
            st.rerun()
