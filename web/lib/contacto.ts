// Contrato fijo con el bot de WhatsApp: el backend decodifica la firma invisible
// y el token entre paréntesis. Cambiar el alfabeto, el orden de bits, los
// caracteres o el texto rompe la atribución del lead sin ningún error visible.

export const ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
export const LARGO_TOKEN = 6;
export const NUMERO_WHATSAPP = "14244475253";
export const URL_CLIC = "https://apex-manager-three.vercel.app/api/facturapp/clic";

const MARCA = "\u2060";
const BIT_0 = "\u200B";
const BIT_1 = "\u200C";

export function generarToken(aleatorio: (bytes: Uint8Array) => Uint8Array = (b) => crypto.getRandomValues(b)): string {
  const bytes = aleatorio(new Uint8Array(LARGO_TOKEN));
  let token = "";
  // 256 es múltiplo de 32: el & 31 no sesga ninguna letra.
  for (const b of bytes) token += ALFABETO[b & 31];
  return token;
}

export function esTokenValido(token: unknown): token is string {
  return typeof token === "string" && token.length === LARGO_TOKEN && [...token].every((c) => ALFABETO.includes(c));
}

export function indicesDeToken(token: string): number[] {
  return [...token].map((c) => {
    const i = ALFABETO.indexOf(c);
    if (i < 0) throw new Error(`Carácter fuera del alfabeto: ${c}`);
    return i;
  });
}

export function firmaInvisible(token: string): string {
  const bits = indicesDeToken(token)
    .map((i) => i.toString(2).padStart(5, "0"))
    .join("");
  return MARCA + [...bits].map((b) => (b === "1" ? BIT_1 : BIT_0)).join("") + MARCA;
}

export function textoContacto(token: string): string {
  const firma = firmaInvisible(token);
  return (
    "Hola" +
    firma +
    ", vi la web de FacturApp y quiero saber cómo funciona para mi distribuidora. (web " +
    token +
    ")" +
    firma
  );
}

export function urlWhatsApp(token: string): string {
  return `https://wa.me/${NUMERO_WHATSAPP}?text=${encodeURIComponent(textoContacto(token))}`;
}

export type Utm = {
  utm_source: string | null;
  utm_medium: string | null;
  utm_campaign: string | null;
};

export function utmDeBusqueda(search: string): Utm {
  const p = new URLSearchParams(search);
  return {
    utm_source: p.get("utm_source"),
    utm_medium: p.get("utm_medium"),
    utm_campaign: p.get("utm_campaign"),
  };
}

export type PayloadClic = Utm & {
  token: string;
  pagina: string;
  demo: boolean;
  referrer: string;
};

export function payloadClic(datos: PayloadClic): string {
  return JSON.stringify({
    token: datos.token,
    pagina: datos.pagina,
    demo: datos.demo,
    utm_source: datos.utm_source,
    utm_medium: datos.utm_medium,
    utm_campaign: datos.utm_campaign,
    referrer: datos.referrer,
  });
}
