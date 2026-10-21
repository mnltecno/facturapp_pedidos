import { cacheLife } from "next/cache";
import { ImageResponse } from "next/og";

export const alt = "FacturApp: tus clientes arman el pedido, vos no tipeás nada.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

type Fuente = { name: string; data: ArrayBuffer; style: "normal" | "italic"; weight: 400 | 600 };

// Satori necesita TTF/OTF. Pedido a la API de Google sin user-agent moderno,
// devuelve TTF. Si la red falla en el build, la imagen sale con la fuente por
// defecto en vez de romper el build.
async function fuente(familia: string, texto: string, estilo: string): Promise<ArrayBuffer | null> {
  "use cache";
  cacheLife("max");
  try {
    const css = await (
      await fetch(`https://fonts.googleapis.com/css2?family=${familia}:${estilo}&text=${encodeURIComponent(texto)}`)
    ).text();
    const url = css.match(/src: url\((.+?)\) format\('(?:opentype|truetype)'\)/)?.[1];
    if (!url) return null;
    return await (await fetch(url)).arrayBuffer();
  } catch {
    return null;
  }
}

export default async function Imagen() {
  const linea1 = "Tus clientes arman el pedido.";
  const linea2 = "Vos no tipeás nada.";
  const chico = "FacturApp · Pedidos online para distribuidoras";
  const [sans, serif] = await Promise.all([
    fuente("Geist", linea1 + chico, "wght@600"),
    fuente("Instrument+Serif", linea2, "ital@1"),
  ]);
  const fonts: Fuente[] = [];
  if (sans) fonts.push({ name: "Geist", data: sans, style: "normal", weight: 600 });
  if (serif) fonts.push({ name: "Instrument Serif", data: serif, style: "italic", weight: 400 });

  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "72px 80px",
        background: "#f3f0e8",
        backgroundImage:
          "repeating-linear-gradient(to bottom, transparent 0, transparent 47px, rgba(23,22,15,0.07) 47px, rgba(23,22,15,0.07) 48px)",
        color: "#17160f",
        fontFamily: "Geist",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <svg width="56" height="56" viewBox="0 0 32 32">
          <rect width="32" height="32" rx="9" fill="#17160f" />
          <path d="M10 8.5h12v15.2l-2-1.4-2 1.4-2-1.4-2 1.4-2-1.4-2 1.4z" fill="#f3f0e8" />
          <path d="M13 13h6M13 16.5h4" stroke="#17160f" strokeWidth="1.6" strokeLinecap="round" />
          <circle cx="21.5" cy="21.5" r="3.2" fill="#b23a1c" />
        </svg>
        <span style={{ fontSize: 30, fontWeight: 600, letterSpacing: "-0.03em" }}>FacturApp</span>
      </div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <span style={{ fontSize: 84, fontWeight: 600, letterSpacing: "-0.045em", lineHeight: 1 }}>{linea1}</span>
        <span
          style={{
            fontSize: 96,
            fontFamily: "Instrument Serif",
            fontStyle: "italic",
            color: "#3a382e",
            lineHeight: 1.05,
            marginTop: 8,
          }}
        >
          {linea2}
        </span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 26, color: "#625e52" }}>
        <span style={{ width: 12, height: 12, borderRadius: 999, background: "#b23a1c" }} />
        {chico}
      </div>
    </div>,
    { ...size, fonts },
  );
}
