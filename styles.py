"""
pedidos_online/styles.py
CSS dark-premium — Parada Técnica. v2 (sticky footer + fix inputs)
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
    "general":       "📦",
}

def get_emoji(familia: str) -> str:
    if not familia:
        return "📦"
    key = familia.strip().lower()
    if key in EMOJI_FAMILIAS:
        return EMOJI_FAMILIAS[key]
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
    font-family: 'Segoe UI','Inter',sans-serif !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    /* Espacio al fondo para que el sticky footer no tape contenido */
    padding-bottom: 5rem !important;
}

/* ═══════════════════════════════════════════════
   INPUTS NUMÉRICOS — CORRECCIÓN CONTRASTE
   (iOS Safari requiere -webkit-text-fill-color)
════════════════════════════════════════════════ */
input,
input[type="number"],
input[type="text"],
input[type="password"],
input[type="email"] {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #FF6B35 !important;
}

[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 700 !important;
    text-align: center !important;
    caret-color: #FF6B35 !important;
}

[data-testid="stNumberInput"] button {
    background: #2a2a2a !important;
    border: 1px solid #444 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-radius: 6px !important;
}

.stTextInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    -webkit-text-fill-color: #f0f0f0 !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input::placeholder {
    color: #555 !important;
    -webkit-text-fill-color: #555 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 2px rgba(255,107,53,.2) !important;
}

/* Password / textarea */
.stTextArea textarea {
    background: #1a1a1a !important;
    color: #f0f0f0 !important;
    -webkit-text-fill-color: #f0f0f0 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
}

/* ═══════════════════════════════════════════════
   BOTONES — CORRECCIÓN CONTRASTE
════════════════════════════════════════════════ */
.stButton > button {
    background: #1e1e1e !important;
    color: #f0f0f0 !important;
    -webkit-text-fill-color: #f0f0f0 !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all .18s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #2a2a2a !important;
    border-color: #444 !important;
}
/* Botón primary (verde) */
.stButton > button[kind="primary"] {
    background: #22c55e !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(34,197,94,.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #16a34a !important;
}

/* ═══════════════════════════════════════════════
   HERO HEADER
════════════════════════════════════════════════ */
.pt-hero {
    background: #0d0d0d;
    padding: 1.2rem 1rem 0.8rem;
    border-bottom: 1px solid #1e1e1e;
}
.pt-title {
    font-size: 1.6rem;
    font-weight: 900;
    color: #FF6B35;
    letter-spacing: 1px;
    text-transform: uppercase;
    line-height: 1.1;
}
.pt-subtitle {
    font-size: 0.73rem;
    color: #666;
    margin-top: 3px;
}
.pt-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.7rem;
}
.pt-capsule {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 0.28rem 0.75rem;
    font-size: 0.72rem;
    color: #ccc;
    white-space: nowrap;
}

/* ═══════════════════════════════════════════════
   FILTROS — PILLS
════════════════════════════════════════════════ */
[data-testid="stPills"] {
    gap: 0.35rem !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
}
[data-testid="stPills"] button {
    background: #1e1e1e !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 20px !important;
    color: #bbb !important;
    -webkit-text-fill-color: #bbb !important;
    font-size: 0.8rem !important;
    padding: 0.32rem 0.85rem !important;
    white-space: nowrap !important;
    transition: all .18s !important;
}
[data-testid="stPills"] button[aria-pressed="true"] {
    background: #FF6B35 !important;
    border-color: #FF6B35 !important;
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
    font-weight: 700 !important;
}
[data-testid="stPills"] button:hover {
    border-color: #FF6B35 !important;
    color: #FF6B35 !important;
    -webkit-text-fill-color: #FF6B35 !important;
}

/* ═══════════════════════════════════════════════
   STICKY FOOTER — BOTÓN VER PEDIDO
════════════════════════════════════════════════ */
.sticky-footer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
    background: rgba(13,13,13,0.97) !important;
    border-top: 1px solid #1e1e1e !important;
    padding: 0.7rem 1rem !important;
    backdrop-filter: blur(8px) !important;
}
.sticky-footer-a {
    display: block !important;
    background: #22c55e !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-align: center !important;
    border-radius: 14px !important;
    padding: 0.85rem 1rem !important;
    font-weight: 900 !important;
    font-size: 1.05rem !important;
    text-decoration: none !important;
    box-shadow: 0 4px 20px rgba(34,197,94,.4) !important;
    letter-spacing: 0.3px !important;
}
.sticky-footer-a:hover {
    background: #16a34a !important;
    text-decoration: none !important;
}

/* ═══════════════════════════════════════════════
   CARRITO ITEMS
════════════════════════════════════════════════ */
.cart-total {
    margin: 0.8rem 0;
    background: linear-gradient(135deg, #FF6B35, #ff8c00);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ct-label  { color: rgba(255,255,255,.8); font-size:.9rem; font-weight:600; }
.ct-amount { color: #fff; font-size: 1.6rem; font-weight: 900; }

/* ═══════════════════════════════════════════════
   OTROS OVERRIDES
════════════════════════════════════════════════ */
hr { border-color: #1e1e1e !important; }
[data-testid="stSelectbox"] > div > div {
    background: #1a1a1a !important;
    color: #f0f0f0 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
}
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
</style>
"""


def inject_css():
    st.markdown(DARK_CSS, unsafe_allow_html=True)


def render_hero(n_productos: int, whatsapp_number: str, alias: str):
    st.markdown(
        f"""<div class="pt-hero">
              <div class="pt-title">📋 Lista de Precios</div>
              <div class="pt-subtitle">Av. Int. Adolfo Arnoldi 1975, San Fernando</div>
              <div class="pt-stats">
                <span class="pt-capsule">📦 {n_productos} productos</span>
                <span class="pt-capsule">💳 Alias: {alias}</span>
                <span class="pt-capsule">📲 WA: {whatsapp_number}</span>
              </div>
            </div>""",
        unsafe_allow_html=True,
    )


def render_sticky_footer(items: int, total: float):
    """Barra fija en el fondo de pantalla con el botón de confirmar pedido."""
    if items <= 0:
        return
    st.markdown(
        f"""<div class="sticky-footer">
              <a href="?nav=carrito" target="_self" class="sticky-footer-a">
                🛒&nbsp; Ver pedido ({items} items) &nbsp;·&nbsp; ${total:,.2f}
              </a>
            </div>""",
        unsafe_allow_html=True,
    )


def header(titulo: str, subtitulo: str = ""):
    """Header simple para login/registro."""
    st.markdown(
        f"""<div style="background:#0d0d0d;padding:1.2rem 1rem 1rem;
                        border-bottom:1px solid #1e1e1e;margin-bottom:1rem">
              <div style="font-size:1.4rem;font-weight:900;color:#FF6B35;
                          text-transform:uppercase;letter-spacing:1px">
                🛒 {titulo}
              </div>
              <div style="font-size:.75rem;color:#666;margin-top:3px">
                {subtitulo}
              </div>
            </div>""",
        unsafe_allow_html=True,
    )
