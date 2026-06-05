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

/* ── Sticky cart button via CSS anchor+sibling trick ──────────────────── */
/* El span#cart-btn-anchor (invisible) se renderiza inmediatamente antes
   del st.button. El selector + apunta al siguiente .element-container,
   que es exactamente donde Streamlit pone ese button.                   */
.element-container:has(#cart-btn-anchor) + .element-container {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
    padding: 0.6rem 0.8rem 0.7rem !important;
    background: rgba(13,13,13,0.96) !important;
    backdrop-filter: blur(10px) !important;
    border-top: 1px solid #1e1e1e !important;
}
.element-container:has(#cart-btn-anchor) + .element-container .stButton > button {
    border-radius: 14px !important;
    padding: .82rem !important;
    font-size: 1.05rem !important;
    font-weight: 900 !important;
    box-shadow: 0 4px 18px rgba(34,197,94,.4) !important;
    width: 100% !important;
}
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


def render_sticky_footer(items: int, total: float) -> bool:
    """
    Botón fijo al pie de pantalla.
    Usa un <span> ancla invisible + CSS adjacent-sibling selector para
    posicionarlo fixed SIN usar <a href>, evitando la recarga de página
    que borraba el session_state y deslogueaba al usuario.
    Retorna True si el usuario lo presionó.
    """
    if items <= 0:
        return False
    # Espacio extra para que el contenido no quede tapado por el botón fijo
    st.markdown("<div style='height:4.5rem'></div>", unsafe_allow_html=True)
    # Ancla invisible — el CSS la usa para apuntar al stButton siguiente
    st.markdown('<span id="cart-btn-anchor" style="display:none"></span>',
                unsafe_allow_html=True)
    # El button debe ser el elemento Streamlit INMEDIATAMENTE siguiente al anchor
    return st.button(
        f"🛒  Ver pedido ({items} items)  ·  ${total:,.2f}",
        key="btn_sticky_cart",
        use_container_width=True,
        type="primary",
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
