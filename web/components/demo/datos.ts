export type Familia = "Bebidas" | "Almacén" | "Limpieza" | "Golosinas";

export type Producto = {
  ean13: string;
  descripcion: string;
  familia: Familia;
  p_venta: number;
  descuento: number;
};

export const FAMILIAS: Familia[] = ["Almacén", "Bebidas", "Golosinas", "Limpieza"];

export const DISTRIBUIDORA = "Distribuidora del Sur";

export const CLIENTE = {
  nombre: "Marta",
  apellido: "Gómez",
  telefono: "11 4823-1907",
  email: "marta.gomez@correo.com",
  direccion: "Av. Mitre 1520, Avellaneda, Buenos Aires",
};

export const PRODUCTOS: Producto[] = [
  { ean13: "7790895002731", descripcion: "Gaseosa cola 2,25 L × 6", familia: "Bebidas", p_venta: 22800, descuento: 10 },
  {
    ean13: "7790790001648",
    descripcion: "Agua mineral sin gas 2 L × 6",
    familia: "Bebidas",
    p_venta: 9600,
    descuento: 0,
  },
  {
    ean13: "7795147008127",
    descripcion: "Cerveza rubia lata 473 cc × 24",
    familia: "Bebidas",
    p_venta: 43200,
    descuento: 8,
  },
  {
    ean13: "7790336014576",
    descripcion: "Vino tinto malbec 750 cc × 6",
    familia: "Bebidas",
    p_venta: 27000,
    descuento: 0,
  },
  {
    ean13: "7791301009283",
    descripcion: "Jugo en polvo naranja × 20",
    familia: "Bebidas",
    p_venta: 6400,
    descuento: 0,
  },
  { ean13: "7790336002139", descripcion: "Yerba mate 1 kg × 10", familia: "Almacén", p_venta: 52000, descuento: 5 },
  {
    ean13: "7790743006355",
    descripcion: "Aceite de girasol 1,5 L × 12",
    familia: "Almacén",
    p_venta: 46800,
    descuento: 12,
  },
  {
    ean13: "7790060004171",
    descripcion: "Fideos tallarín 500 g × 20",
    familia: "Almacén",
    p_venta: 19800,
    descuento: 0,
  },
  {
    ean13: "7790290011734",
    descripcion: "Arroz largo fino 1 kg × 10",
    familia: "Almacén",
    p_venta: 16500,
    descuento: 0,
  },
  { ean13: "7790360022868", descripcion: "Azúcar 1 kg × 10", familia: "Almacén", p_venta: 13900, descuento: 0 },
  { ean13: "7790290003180", descripcion: "Lavandina 2 L × 8", familia: "Limpieza", p_venta: 10400, descuento: 0 },
  { ean13: "7790500016498", descripcion: "Detergente 750 ml × 12", familia: "Limpieza", p_venta: 21600, descuento: 15 },
  {
    ean13: "7791250160226",
    descripcion: "Papel higiénico 4 rollos × 12",
    familia: "Limpieza",
    p_venta: 28800,
    descuento: 0,
  },
  {
    ean13: "7790290007041",
    descripcion: "Jabón en polvo 800 g × 10",
    familia: "Limpieza",
    p_venta: 33000,
    descuento: 0,
  },
  {
    ean13: "7790040022188",
    descripcion: "Alfajor triple chocolate × 24",
    familia: "Golosinas",
    p_venta: 21600,
    descuento: 10,
  },
  {
    ean13: "7790690005425",
    descripcion: "Caramelos masticables 800 g",
    familia: "Golosinas",
    p_venta: 7900,
    descuento: 0,
  },
  { ean13: "7791604011235", descripcion: "Chicles de menta × 20", familia: "Golosinas", p_venta: 5200, descuento: 0 },
  { ean13: "7790114006793", descripcion: "Chupetín frutal × 48", familia: "Golosinas", p_venta: 9100, descuento: 0 },
];

export const POR_EAN = new Map(PRODUCTOS.map((p) => [p.ean13, p]));

export function precioFinal(p: Pick<Producto, "p_venta" | "descuento">): number {
  if (p.descuento) return Math.round(p.p_venta * (1 - p.descuento / 100) * 100) / 100;
  return p.p_venta;
}

const fmt = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

export function pesos(n: number): string {
  return fmt.format(n);
}

export function normalizar(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}
