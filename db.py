"""
pedidos_online/db.py
Cliente Supabase singleton con helpers CRUD.
"""
import hashlib
import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_supabase() -> Client:
    """Instancia única del cliente Supabase (cacheada por Streamlit)."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


# ── Auth helpers ─────────────────────────────────────────────────────────────

def hash_password(password: str, salt: str = "") -> str:
    """SHA-256 del password + salt (email como salt)."""
    raw = f"{password}{salt}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def get_cliente_by_email(email: str) -> dict | None:
    sb = get_supabase()
    res = sb.table("clientes_app").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None


def crear_cliente(apellido: str, nombre: str, telefono: str,
                  email: str, direccion: str, password: str) -> dict:
    sb = get_supabase()
    row = {
        "apellido":      apellido.strip(),
        "nombre":        nombre.strip(),
        "telefono":      telefono.strip(),
        "email":         email.strip().lower(),
        "direccion":     direccion.strip(),
        "password_hash": hash_password(password, email.strip().lower()),
    }
    res = sb.table("clientes_app").insert(row).execute()
    return res.data[0]


def verificar_password(email: str, password: str) -> dict | None:
    """Retorna el cliente si la contraseña es correcta, None si no."""
    cliente = get_cliente_by_email(email)
    if not cliente:
        return None
    expected = hash_password(password, email.strip().lower())
    return cliente if cliente["password_hash"] == expected else None


# ── Catálogo ─────────────────────────────────────────────────────────────────

def get_productos() -> list[dict]:
    sb = get_supabase()
    res = (sb.table("productos_catalogo")
             .select("ean13,descripcion,familia,p_venta,descuento")
             .eq("activo", True)
             .order("descripcion")
             .execute())
    return res.data or []


def get_familias() -> list[str]:
    productos = get_productos()
    familias = sorted({p["familia"] for p in productos if p.get("familia")})
    return familias


# ── Pedidos ──────────────────────────────────────────────────────────────────

def guardar_pedido(cliente_id: str, items: list[dict], total: float) -> int:
    """Guarda cabecera + detalles. Retorna el id del pedido creado."""
    sb = get_supabase()

    # Cabecera
    pedido_res = sb.table("pedidos").insert({
        "cliente_id": cliente_id,
        "total":      round(total, 2),
        "estado":     "Pendiente",
    }).execute()
    pedido_id = pedido_res.data[0]["id"]

    # Detalles en batch
    detalles = [
        {
            "pedido_id":       pedido_id,
            "ean13":           it["ean13"],
            "descripcion":     it["descripcion"],
            "cantidad":        it["cantidad"],
            "precio_unitario": round(it["precio_unitario"], 2),
            "subtotal":        round(it["subtotal"], 2),
        }
        for it in items
    ]
    sb.table("pedido_detalles").insert(detalles).execute()
    return pedido_id


def get_pedidos_pendientes() -> list[dict]:
    """Para FacturApp desktop: devuelve pedidos con estado Pendiente."""
    sb = get_supabase()
    res = (sb.table("pedidos")
             .select("*, clientes_app(*), pedido_detalles(*)")
             .eq("estado", "Pendiente")
             .order("created_at")
             .execute())
    return res.data or []


def marcar_pedido_importado(pedido_id: int):
    sb = get_supabase()
    sb.table("pedidos").update({"estado": "Importado"}).eq("id", pedido_id).execute()


def sincronizar_productos(productos: list[dict]):
    """Upsert masivo de productos desde SQLite → Supabase."""
    sb = get_supabase()
    rows = [
        {
            "ean13":       p["ean13"],
            "descripcion": p["descripcion"],
            "familia":     p.get("familia") or p.get("familia_nombre") or "",
            "p_venta":     float(p.get("p_venta") or p.get("precio_venta") or 0),
            "descuento":   float(p.get("descuento") or p.get("descuento_pct") or 0),
            "activo":      True,
        }
        for p in productos if p.get("ean13")
    ]
    if rows:
        sb.table("productos_catalogo").upsert(rows).execute()
    return len(rows)
