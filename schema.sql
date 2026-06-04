-- ============================================================
-- FacturApp Pedidos Online — Schema Supabase
-- Ejecutar en el SQL Editor de Supabase (una sola vez)
-- ============================================================

-- 1. Catálogo de productos (sincronizado desde FacturApp)
CREATE TABLE IF NOT EXISTS productos_catalogo (
    ean13       TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    familia     TEXT,
    p_venta     REAL NOT NULL DEFAULT 0,
    descuento   REAL NOT NULL DEFAULT 0,
    activo      BOOLEAN DEFAULT TRUE,
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Clientes / usuarios de la app móvil
CREATE TABLE IF NOT EXISTS clientes_app (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apellido      TEXT NOT NULL,
    nombre        TEXT NOT NULL,
    telefono      TEXT,
    email         TEXT UNIQUE NOT NULL,
    direccion     TEXT,           -- formato ORS: "Calle, Número, Ciudad, Provincia"
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Cabecera de pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id         BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    cliente_id UUID REFERENCES clientes_app(id) ON DELETE SET NULL,
    total      REAL NOT NULL DEFAULT 0,
    estado     TEXT NOT NULL DEFAULT 'Pendiente'  -- Pendiente | Importado | Cancelado
);

-- 4. Líneas de pedido
CREATE TABLE IF NOT EXISTS pedido_detalles (
    id              BIGSERIAL PRIMARY KEY,
    pedido_id       BIGINT REFERENCES pedidos(id) ON DELETE CASCADE,
    ean13           TEXT NOT NULL,
    descripcion     TEXT NOT NULL,
    cantidad        INTEGER NOT NULL DEFAULT 1,
    precio_unitario REAL NOT NULL,
    subtotal        REAL NOT NULL
);

-- ── Índices útiles ───────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_pedidos_estado    ON pedidos(estado);
CREATE INDEX IF NOT EXISTS idx_pedidos_cliente   ON pedidos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_detalles_pedido   ON pedido_detalles(pedido_id);
CREATE INDEX IF NOT EXISTS idx_catalogo_familia  ON productos_catalogo(familia);

-- ── Row Level Security (recomendado para producción) ─────────
-- Habilitar RLS y crear políticas según tu configuración de Supabase.
-- Por ahora dejamos deshabilitado para simplificar el desarrollo:
ALTER TABLE productos_catalogo DISABLE ROW LEVEL SECURITY;
ALTER TABLE clientes_app       DISABLE ROW LEVEL SECURITY;
ALTER TABLE pedidos            DISABLE ROW LEVEL SECURITY;
ALTER TABLE pedido_detalles    DISABLE ROW LEVEL SECURITY;
