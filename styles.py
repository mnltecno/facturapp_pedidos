"""
pedidos_online/styles.py
CSS mobile-first inyectado en Streamlit.
"""

MOBILE_CSS = """
<style>
/* ── Ocultar chrome de Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Layout base ── */
.main .block-container {
    padding: 0.8rem 1rem 4rem 1rem;
    max-width: 480px;
    margin: 0 auto;
}

/* ── Tipografía ── */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

/* ── Header de app ── */
.app-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    padding: 1rem 1.2rem 0.8rem;
    border-radius: 0 0 18px 18px;
    margin: -0.8rem -1rem 1.2rem -1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.app-header h1 { font-size: 1.2rem; margin: 0; font-weight: 700; }
.app-header .sub { font-size: 0.75rem; opacity: 0.7; margin-top: 2px; }

/* ── Tarjeta de producto ── */
.prod-card {
    background: #1e1e2e;
    border: 1px solid #2d2d4e;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    transition: border-color 0.2s;
}
.prod-card:hover { border-color: #5865f2; }
.prod-info { flex: 1; }
.prod-info .desc { font-weight: 600; font-size: 0.9rem; color: #e0e0e0; }
.prod-info .fam  { font-size: 0.72rem; color: #888; margin-top: 2px; }
.prod-info .precio { font-size: 1rem; font-weight: 700; color: #4ade80; margin-top: 4px; }
.prod-info .dto  { font-size: 0.72rem; color: #f59e0b; }

/* ── Carrito flotante ── */
.carrito-badge {
    position: fixed;
    bottom: 1.2rem;
    right: 1rem;
    background: #5865f2;
    color: white;
    border-radius: 50px;
    padding: 0.7rem 1.3rem;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px rgba(88,101,242,0.5);
    cursor: pointer;
    z-index: 999;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Item de carrito ── */
.cart-item {
    background: #1e1e2e;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cart-item .ci-desc { font-size: 0.88rem; font-weight: 600; color: #e0e0e0; }
.cart-item .ci-sub  { font-size: 0.8rem; color: #888; }
.cart-item .ci-total{ font-weight: 700; color: #4ade80; font-size: 0.95rem; }

/* ── Total ── */
.total-bar {
    background: linear-gradient(135deg, #5865f2, #7c3aed);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1rem 0;
}
.total-bar .label { color: rgba(255,255,255,0.8); font-size: 0.9rem; }
.total-bar .amount { color: white; font-size: 1.5rem; font-weight: 800; }

/* ── Botones ── */
.stButton > button {
    width: 100%;
    border-radius: 12px !important;
    padding: 0.7rem 1rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.2s;
}
.btn-whatsapp > button {
    background: #25d366 !important;
    color: white !important;
    border: none !important;
    font-size: 1.1rem !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div { border-radius: 10px !important; }

/* ── Alerts ── */
.success-box {
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid #4ade80;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    color: #4ade80;
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)


def header(titulo: str, subtitulo: str = ""):
    import streamlit as st
    st.markdown(
        f'''<div class="app-header">
            <div>
                <h1>🛒 {titulo}</h1>
                <div class="sub">{subtitulo}</div>
            </div>
        </div>''',
        unsafe_allow_html=True,
    )
