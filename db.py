"""
pedidos_online/db.py
Cliente Supabase singleton con helpers CRUD.
Todas las funciones de datos reciben `negocio_id` para aislar
los datos de cada distribuidor que usa FacturApp.
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


def get_cliente_by_email(email: str, negocio_id: str) -> dict | None:
    sb  = get_supabase()
    res = (sb.table("clientes_app")
             .select("*")
             .eq("email", email)
             .eq("negocio_id", negocio_id)
             .execute())
    return res.data[0] if res.data else None


def crear_cliente(apellido: str, nombre: str, telefono: str,
                  email: str, direccion: str, password: str,
                  negocio_id: str) -> dict:
    sb  = get_supabase()
    row = {
        "apellido":      apellido.strip(),
        "nombre":        nombre.strip(),
        "telefono":      telefono.strip(),
        "email":         email.strip().lower(),
        "direccion":     direccion.strip(),
        "password_hash": hash_password(password, email.strip().lower()),
        "negocio_id":    negocio_id,
    }
    res = sb.table("clientes_app").insert(row).execute()
    return res.data[0]


def verificar_password(email: str, password: str, negocio_id: str) -> dict | None:
    """Retorna el cliente si la contraseña es correcta, None si no."""
    cliente = get_cliente_by_email(email, negocio_id)
    if not cliente:
        return None
    expected = hash_password(password, email.strip().lower())
    return cliente if cliente["password_hash"] == expected else None


# ── Catálogo ─────────────────────────────────────────────────────────────────

def get_productos(negocio_id: str) -> list[dict]:
    sb  = get_supabase()
    res = (sb.table("productos_catalogo")
             .select("ean13,descripcion,familia,p_venta,descuento")
             .eq("negocio_id", negocio_id)
             .eq("activo", True)
             .order("descripcion")
             .execute())
    return res.data or []


def actualizar_cliente(cliente_id: str, datos: dict) -> dict:
    """
    Actualiza campos del cliente en Supabase.
    `datos` puede contener: nombre, apellido, telefono, direccion.
    Retorna el registro actualizado.
    """
    sb = get_supabase()
    campos_permitidos = {"nombre", "apellido", "telefono", "direccion", "password_hash"}
    payload = {
        k: v.strip() if isinstance(v, str) else v
        for k, v in datos.items()
        if k in campos_permitidos and v is not None
    }
    res = sb.table("clientes_app").update(payload).eq("id", cliente_id).execute()
    return res.data[0]


def get_familias(negocio_id: str) -> list[str]:
    productos = get_productos(negocio_id)
    return sorted({p["familia"] for p in productos if p.get("familia")})


# ── Pedidos ──────────────────────────────────────────────────────────────────

def guardar_pedido(cliente_id: str, items: list[dict], total: float,
                   negocio_id: str) -> int:
    """Guarda cabecera + detalles. Retorna el id del pedido creado."""
    sb = get_supabase()

    # Cabecera
    pedido_res = sb.table("pedidos").insert({
        "cliente_id": cliente_id,
        "total":      round(total, 2),
        "estado":     "Pendiente",
        "negocio_id": negocio_id,
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


def get_pedidos_pendientes(negocio_id: str) -> list[dict]:
    """Para FacturApp desktop: devuelve pedidos con estado Pendiente del negocio."""
    sb  = get_supabase()
    res = (sb.table("pedidos")
             .select("*, clientes_app(*), pedido_detalles(*)")
             .eq("estado", "Pendiente")
             .eq("negocio_id", negocio_id)
             .order("created_at")
             .execute())
    return res.data or []


def marcar_pedido_importado(pedido_id: int):
    sb = get_supabase()
    sb.table("pedidos").update({"estado": "Importado"}).eq("id", pedido_id).execute()


def sincronizar_productos(productos: list[dict], negocio_id: str) -> int:
    """Upsert masivo de productos desde SQLite → Supabase, filtrado por negocio."""
    sb   = get_supabase()
    rows = [
        {
            "ean13":       p["ean13"],
            "descripcion": p["descripcion"],
            "familia":     p.get("familia") or p.get("familia_nombre") or "",
            "p_venta":     float(p.get("p_venta") or p.get("precio_venta") or 0),
            "descuento":   float(p.get("descuento") or p.get("descuento_pct") or 0),
            "activo":      True,
            "negocio_id":  negocio_id,
        }
        for p in productos if p.get("ean13")
    ]
    if rows:
        # El upsert usa el índice compuesto uidx_productos_ean13_negocio
        sb.table("productos_catalogo").upsert(
            rows, on_conflict="ean13,negocio_id"
        ).execute()
    return len(rows)
