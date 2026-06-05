"""
pedidos_online/styles.py  v3
CSS mínimo — solo hero header y sticky footer.
El tema dark/light lo maneja Streamlit via config.toml.
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
    "café":          "☕", "té":            "🍵", "te": "🍵",
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


# ── CSS mínimo ────────────────────────────────────────────────────────────────
MINIMAL_CSS = """
<style>
/* Ocultar chrome de Streamlit */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"] { display: none !important; }

/* Quitar padding superior excesivo */
.main .block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 5rem !important;   /* espacio para el sticky footer */
    max-width: 600px !important;
    margin: 0 auto !important;
}

/* Línea decorativa naranja bajo el hero */
.pt-hero-bar {
    height: 3px;
    background: linear-gradient(90deg, #FF6B35, #ff8c00 60%, transparent);
    margin-bottom: 0.8rem;
}

/* Sticky footer */
.sticky-footer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
    padding: 0.65rem 1rem !important;
    border-top: 1px solid rgba(255,107,53,0.2) !important;
    background: rgba(13,13,13,0.96) !important;
    backdrop-filter: blur(10px) !important;
}
.sticky-footer-a {
    display: block;
    background: #22c55e;
    color: #ffffff !important;
    text-align: center;
    border-radius: 14px;
    padding: 0.8rem 1rem;
    font-weight: 900;
    font-size: 1.05rem;
    text-decoration: none !important;
    box-shadow: 0 4px 18px rgba(34,197,94,.35);
}
.sticky-footer-a:hover { background: #16a34a; text-decoration: none; }
</style>
"""


def inject_css():
    st.markdown(MINIMAL_CSS, unsafe_allow_html=True)


def render_hero(n_productos: int, whatsapp_number: str, alias: str):
    st.markdown(
        f"""<div style="padding:1rem 0 0.3rem">
              <div style="font-size:1.6rem;font-weight:900;
                          color:#FF6B35;letter-spacing:1px;
                          text-transform:uppercase">
                📋 Lista de Precios
              </div>
              <div style="font-size:0.75rem;opacity:.6;margin-top:2px">
                Av. Int. Adolfo Arnoldi 1975, San Fernando
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.6rem">
                <span style="border:1px solid #333;border-radius:20px;
                             padding:.2rem .7rem;font-size:.72rem">
                  📦 {n_productos} productos
                </span>
                <span style="border:1px solid #333;border-radius:20px;
                             padding:.2rem .7rem;font-size:.72rem">
                  💳 {alias}
                </span>
                <span style="border:1px solid #333;border-radius:20px;
                             padding:.2rem .7rem;font-size:.72rem">
                  📲 {whatsapp_number}
                </span>
              </div>
            </div>
            <div class="pt-hero-bar"></div>""",
        unsafe_allow_html=True,
    )


def render_sticky_footer(items: int, total: float):
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
    st.markdown(
        f"""<div style="padding:.8rem 0 .5rem">
              <div style="font-size:1.4rem;font-weight:900;color:#FF6B35">
                🛒 {titulo}
              </div>
              <div style="font-size:.75rem;opacity:.5;margin-top:2px">
                {subtitulo}
              </div>
            </div>
            <div class="pt-hero-bar"></div>""",
        unsafe_allow_html=True,
    )
