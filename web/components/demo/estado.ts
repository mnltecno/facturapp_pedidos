import { CLIENTE, POR_EAN, precioFinal, pesos, type Familia } from "./datos";

export type Linea = { ean13: string; descripcion: string; cantidad: number; precio_unitario: number; subtotal: number };
export type EstadoPedido = "Pendiente" | "Importado" | "Cancelado";

export type PedidoPC = {
  id: number;
  cliente: string;
  hora: string;
  direccion: string;
  lineas: Linea[];
  total: number;
  estado: EstadoPedido;
  nuevo: boolean;
};

export type Pantalla = "catalogo" | "pedido" | "exito";

export type Estado = {
  pantalla: Pantalla;
  direccion: 1 | -1;
  familia: Familia | null;
  busqueda: string;
  carrito: Record<string, number>;
  guardando: boolean;
  confirmado: { id: number; total: number; mensaje: string } | null;
  vistaWhatsApp: boolean;
  pedidos: PedidoPC[];
  siguienteId: number;
};

const PREVIOS: PedidoPC[] = [
  {
    id: 1042,
    cliente: "Ruiz, Hernán",
    hora: "09:12",
    direccion: "Belgrano 845, Lanús",
    lineas: [
      {
        ean13: "7790336002139",
        descripcion: "Yerba mate 1 kg × 10",
        cantidad: 2,
        precio_unitario: 49400,
        subtotal: 98800,
      },
      {
        ean13: "7790060004171",
        descripcion: "Fideos tallarín 500 g × 20",
        cantidad: 3,
        precio_unitario: 19800,
        subtotal: 59400,
      },
    ],
    total: 158200,
    estado: "Importado",
    nuevo: false,
  },
  {
    id: 1041,
    cliente: "Sosa, Daniela",
    hora: "08:47",
    direccion: "San Martín 2210, Quilmes",
    lineas: [
      {
        ean13: "7790895002731",
        descripcion: "Gaseosa cola 2,25 L × 6",
        cantidad: 4,
        precio_unitario: 20520,
        subtotal: 82080,
      },
      {
        ean13: "7790040022188",
        descripcion: "Alfajor triple chocolate × 24",
        cantidad: 1,
        precio_unitario: 19440,
        subtotal: 19440,
      },
    ],
    total: 101520,
    estado: "Importado",
    nuevo: false,
  },
];

export const inicial: Estado = {
  pantalla: "catalogo",
  direccion: 1,
  familia: null,
  busqueda: "",
  carrito: {},
  guardando: false,
  confirmado: null,
  vistaWhatsApp: false,
  pedidos: PREVIOS,
  siguienteId: 1043,
};

export type Accion =
  | { t: "familia"; familia: Familia | null }
  | { t: "buscar"; texto: string }
  | { t: "cantidad"; ean: string; cantidad: number }
  | { t: "ir"; pantalla: Pantalla }
  | { t: "vaciar" }
  | { t: "guardando" }
  | { t: "confirmar"; hora: string }
  | { t: "whatsapp"; abierto: boolean }
  | { t: "otro" }
  | { t: "importar"; id: number }
  | { t: "visto"; id: number }
  | { t: "reiniciar" };

export function lineasDe(carrito: Record<string, number>): Linea[] {
  const out: Linea[] = [];
  for (const [ean, cantidad] of Object.entries(carrito)) {
    const p = POR_EAN.get(ean);
    if (!p || cantidad <= 0) continue;
    const precio = precioFinal(p);
    out.push({
      ean13: ean,
      descripcion: p.descripcion,
      cantidad,
      precio_unitario: precio,
      subtotal: Math.round(precio * cantidad * 100) / 100,
    });
  }
  return out;
}

export function resumen(carrito: Record<string, number>) {
  const lineas = lineasDe(carrito);
  return {
    items: lineas.reduce((a, l) => a + l.cantidad, 0),
    total: Math.round(lineas.reduce((a, l) => a + l.subtotal, 0) * 100) / 100,
  };
}

// Mismo formato que _generar_mensaje_whatsapp de pedido.py.
export function mensajeWhatsApp(lineas: Linea[], total: number): string {
  const detalle = lineas
    .map(
      (l) => `• ${l.cantidad} x ${l.descripcion} - ${pesos(l.precio_unitario)} c/u\n  _Subtotal: ${pesos(l.subtotal)}_`,
    )
    .join("\n");
  const sep = "----------------------------------------";
  return [
    "📥 *NUEVO PEDIDO ON-LINE*",
    sep,
    `👤 *Cliente:* ${CLIENTE.apellido}, ${CLIENTE.nombre}`,
    `📱 *Contacto:* ${CLIENTE.telefono}`,
    `📧 *Email:* ${CLIENTE.email}`,
    `📍 *Dirección:* ${CLIENTE.direccion}`,
    sep,
    "📦 *DETALLE DEL PEDIDO:*",
    detalle,
    sep,
    `💰 *TOTAL A PAGAR: ${pesos(total)}*`,
    sep,
    "_Generado automáticamente desde FacturApp Móvil_",
  ].join("\n");
}

const ORDEN: Record<Pantalla, number> = { catalogo: 0, pedido: 1, exito: 2 };

export function reductor(s: Estado, a: Accion): Estado {
  const n = reducir(s, a);
  if (n.pantalla === s.pantalla) return n;
  return { ...n, direccion: ORDEN[n.pantalla] >= ORDEN[s.pantalla] ? 1 : -1 };
}

function reducir(s: Estado, a: Accion): Estado {
  switch (a.t) {
    case "familia":
      return { ...s, familia: a.familia };
    case "buscar":
      return { ...s, busqueda: a.texto };
    case "cantidad": {
      const carrito = { ...s.carrito };
      const c = Math.max(0, Math.min(999, Math.round(a.cantidad)));
      if (c === 0) delete carrito[a.ean];
      else carrito[a.ean] = c;
      const pantalla = s.pantalla === "pedido" && Object.keys(carrito).length === 0 ? "pedido" : s.pantalla;
      return { ...s, carrito, pantalla };
    }
    case "ir":
      return { ...s, pantalla: a.pantalla, vistaWhatsApp: false };
    case "vaciar":
      return { ...s, carrito: {}, pantalla: "catalogo" };
    case "guardando":
      return { ...s, guardando: true };
    case "confirmar": {
      const lineas = lineasDe(s.carrito);
      if (!lineas.length) return { ...s, guardando: false };
      const total = Math.round(lineas.reduce((x, l) => x + l.subtotal, 0) * 100) / 100;
      const id = s.siguienteId;
      const pedido: PedidoPC = {
        id,
        cliente: `${CLIENTE.apellido}, ${CLIENTE.nombre}`,
        hora: a.hora,
        direccion: CLIENTE.direccion,
        lineas,
        total,
        estado: "Pendiente",
        nuevo: true,
      };
      return {
        ...s,
        guardando: false,
        carrito: {},
        pantalla: "exito",
        confirmado: { id, total, mensaje: mensajeWhatsApp(lineas, total) },
        pedidos: [pedido, ...s.pedidos.map((p) => ({ ...p, nuevo: false }))],
        siguienteId: id + 1,
      };
    }
    case "whatsapp":
      return { ...s, vistaWhatsApp: a.abierto };
    case "otro":
      return { ...s, pantalla: "catalogo", confirmado: null, vistaWhatsApp: false, busqueda: "", familia: null };
    case "importar":
      return {
        ...s,
        pedidos: s.pedidos.map((p) => (p.id === a.id && p.estado === "Pendiente" ? { ...p, estado: "Importado" } : p)),
      };
    case "visto":
      return { ...s, pedidos: s.pedidos.map((p) => (p.id === a.id ? { ...p, nuevo: false } : p)) };
    case "reiniciar":
      return inicial;
  }
}
