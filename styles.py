"""
pedidos_online/styles.py
CSS dark-premium para Parada Técnica — optimizado para mobile.
"""
import streamlit as st

# ── Mapeo de emojis por familia ───────────────────────────────────────────────
EMOJI_FAMILIAS = {
    "agua":          "💧", "aguas":         "💧",
    "gaseosa":       "🥤", "gaseosas":      "🥤",
    "cerveza":       "🍺", "cervezas":      "🍺",
    "vino":          "🍷", "vinos":         "🍷",
    "fernet":        "🥃", "espirituosa":   "🥃", "espirituosas": "🥃",
    "whisky":        "🥃", "ron":           "🥃", "vodka":        "🥃",
    "gin":           "🍸", "sidra":         "🍾", "champagne":    "🥂",
    "jugo":          "🍊", "jugos":         "🍊",
    "energizante":   "⚡", "energizantes":  "⚡",
    "isotónica":     "💪", "isotónicas":    "💪", "isotonicas":   "💪",
    "leche":         "🥛", "lácteo":        "🥛", "lácteos":      "🥛",
    "alimento":      "🍞", "alimentos":     "🍞",
    "snack":         "🍿", "snacks":        "🍿",
    "golosina":      "🍬", "golosinas":     "🍬",
    "galleta":       "🍪", "galletas":      "🍪",
    "yerba":         "🧉", "mate":          "🧉",
    "aceite":        "🫒", "aceites":       "🫒",
    "azúcar":        "🍚", "café":          "☕",
    "té":            "🍵", "te":            "🍵",
    "harina":        "🌾", "arroz":         "🍚",
    "pasta":         "🍝", "fideos":        "🍝",
    "conserva":      "🥫", "conservas":     "🥫",
    "limpieza":      "🧹", "higiene":       "🧴",
    "cigarrillo":    "🚬", "cigarrillos":   "🚬",
    "bebida":        "🥤", "bebidas":       "🥤",
    "agua mineral":  "💧", "sin alcohol":   "🥤",
    "con alcohol":   "🍻", "alcohol":       "🍻",
}

def get_emoji(familia: str) -> str:
    """Devuelve el emoji correspondiente a la familia, o 📦 si no hay mapeo."""
    if not familia:
        return "📦"
    key = familia.strip().lower()
    # Búsqueda exacta
    if key in EMOJI_FAMILIAS:
        return EMOJI_FAMILIAS[key]
    # Búsqueda parcial
    for k, v in EMOJI_FAMILIAS.items():
        if k in key or key in k:
            return v
    return "📦"


DARK_CSS = """
<style>
/* ═══════════════════════════════════════════════
   RESET & BASE
════════════════════════════════════════════════ */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background-color: #0d0d0d !important;
    color: #f0f0f0 !important;
    font-family: 'Segoe UI', 'Inter', sans-serif !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ═══════════════════════════════════════════════
   HERO HEADER
════════════════════════════════════════════════ */
.pt-hero {
    background: #0d0d0d;
    padding: 1.4rem 1.2rem 1rem;
    border-bottom: 1px solid #222;
    position: sticky;
    top: 0;
    z-index: 100;
}
.pt-hero-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}
.pt-title {
    font-size: 1.7rem;
    font-weight: 900;
    color: #FF6B35;
    letter-spacing: 1px;
    line-height: 1.1;
    text-transform: uppercase;
}
.pt-subtitle {
    font-size: 0.75rem;
    color: #888;
    margin-top: 3px;
}
.pt-btn-pedido {
    background: #22c55e;
    color: white !important;
    border: none;
    border-radius: 22px;
    padding: 0.55rem 1.1rem;
    font-weight: 800;
    font-size: 0.9rem;
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 4px 15px rgba(34,197,94,0.35);
}
.pt-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}
.pt-capsule {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: #ccc;
    white-space: nowrap;
}

/* ═══════════════════════════════════════════════
   BARRA DE BÚSQUEDA
════════════════════════════════════════════════ */
.search-wrap {
    padding: 0.8rem 1.2rem 0;
    background: #0d0d0d;
}
.stTextInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input::placeholder { color: #555 !important; }
.stTextInput > div > div > input:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 2px rgba(255,107,53,.2) !important;
}

/* ═══════════════════════════════════════════════
   FILTROS — PILLS / RADIO
════════════════════════════════════════════════ */
.filtros-wrap {
    padding: 0.8rem 1.2rem 0;
    overflow-x: auto;
    white-space: nowrap;
    background: #0d0d0d;
}

/* Streamlit pills widget */
[data-testid="stPills"] {
    gap: 0.4rem !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
}
[data-testid="stPills"] button {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 20px !important;
    color: #ccc !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 0.9rem !important;
    white-space: nowrap !important;
    transition: all .18s !important;
}
[data-testid="stPills"] button[aria-pressed="true"],
[data-testid="stPills"] button[data-active="true"] {
    background: #FF6B35 !important;
    border-color: #FF6B35 !important;
    color: #fff !important;
    font-weight: 700 !important;
}
[data-testid="stPills"] button:hover {
    border-color: #FF6B35 !important;
    color: #FF6B35 !important;
}

/* ═══════════════════════════════════════════════
   PRODUCTOS
════════════════════════════════════════════════ */
.prods-wrap {
    padding: 0.8rem 1.2rem 5rem;
}
.prod-row {
    background: #1a1a1a;
    border: 1px solid #252525;
    border-radius: 12px;
    padding: 0.75rem 0.9rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
    transition: border-color .18s;
}
.prod-row:hover { border-color: #333; }
.prod-info { flex: 1; min-width: 0; }
.prod-desc {
    font-weight: 600;
    font-size: 0.88rem;
    color: #f0f0f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.prod-fam {
    font-size: 0.7rem;
    color: #666;
    margin-top: 2px;
}
.prod-precio {
    font-weight: 800;
    font-size: 1rem;
    color: #22c55e;
    white-space: nowrap;
    margin-right: 0.5rem;
    min-width: 70px;
    text-align: right;
}
.prod-input > div > div > input {
    width: 72px !important;
    text-align: center !important;
    background: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}

/* ═══════════════════════════════════════════════
   CARRITO STICKY BOTTOM
════════════════════════════════════════════════ */
.carrito-sticky {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0d0d0d;
    border-top: 1px solid #1e1e1e;
    padding: 0.7rem 1.2rem;
    z-index: 200;
}
.cart-btn {
    background: #22c55e;
    color: #fff;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1.5rem;
    font-size: 1.05rem;
    font-weight: 800;
    width: 100%;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(34,197,94,.35);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    text-decoration: none;
}
.cart-btn:hover { background: #16a34a; }

/* ═══════════════════════════════════════════════
   CARRITO — PÁGINA
════════════════════════════════════════════════ */
.cart-header {
    padding: 1.2rem 1.2rem 0;
    font-size: 1.3rem;
    font-weight: 800;
    color: #FF6B35;
}
.cart-item-row {
    background: #1a1a1a;
    border: 1px solid #252525;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    margin: 0.5rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.ci-info { flex: 1; }
.ci-desc { font-weight: 600; font-size: 0.88rem; color: #f0f0f0; }
.ci-sub  { font-size: 0.75rem; color: #666; margin-top: 2px; }
.ci-price { font-weight: 800; color: #22c55e; white-space: nowrap; }
.ci-del  { background: none; border: none; font-size: 1.1rem;
           cursor: pointer; color: #555; padding: 0; }
.ci-del:hover { color: #ef4444; }

.cart-total {
    margin: 0.8rem 1.2rem;
    background: linear-gradient(135deg, #FF6B35, #ff8c00);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ct-label { color: rgba(255,255,255,.8); font-size: .9rem; font-weight: 600; }
.ct-amount { color: #fff; font-size: 1.6rem; font-weight: 900; }

/* ═══════════════════════════════════════════════
   STREAMLIT OVERRIDES
════════════════════════════════════════════════ */
/* Botones globales */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all .18s !important;
}
/* Number input */
[data-testid="stNumberInput"] input {
    background: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 700 !important;
    text-align: center !important;
}
[data-testid="stNumberInput"] button {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    color: #fff !important;
    border-radius: 6px !important;
}
/* Dividers */
hr { border-color: #1e1e1e !important; }
/* Spinner */
.stSpinner > div { border-color: #FF6B35 transparent transparent !important; }
/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
</style>
"""


def inject_css():
    st.markdown(DARK_CSS, unsafe_allow_html=True)


def render_hero(n_productos: int, whatsapp_number: str, alias: str,
                items_carrito: int, total_carrito: float):
    """Renderiza el header hero con stats y botón de carrito."""
    cart_txt = f"🛒 {items_carrito} items · ${total_carrito:,.0f}" if items_carrito else "🛒 Mi pedido"
    st.markdown(
        f"""<div class="pt-hero">
              <div class="pt-hero-top">
                <div>
                  <div class="pt-title">📋 Lista de Precios</div>
                  <div class="pt-subtitle">Av. Int. Adolfo Arnoldi 1975, San Fernando</div>
                </div>
              </div>
              <div class="pt-stats">
                <span class="pt-capsule">📦 {n_productos} productos</span>
                <span class="pt-capsule">💳 Alias: {alias}</span>
                <span class="pt-capsule">📲 WA: {whatsapp_number}</span>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )


def header(titulo: str, subtitulo: str = ""):
    """Header simple para las páginas de login y registro."""
    import streamlit as st
    st.markdown(
        f"""<div style="background:#0d0d0d;padding:1.4rem 1.2rem 1rem;
                        border-bottom:1px solid #222;margin-bottom:1rem">
              <div style="font-size:1.5rem;font-weight:900;color:#FF6B35;
                          text-transform:uppercase;letter-spacing:1px">
                🛒 {titulo}
              </div>
              <div style="font-size:.78rem;color:#666;margin-top:3px">
                {subtitulo}
              </div>
            </div>""",
        unsafe_allow_html=True,
    )
