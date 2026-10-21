import { describe, expect, it } from "vitest";
import {
  ALFABETO,
  esTokenValido,
  firmaInvisible,
  generarToken,
  indicesDeToken,
  payloadClic,
  textoContacto,
  urlWhatsApp,
  utmDeBusqueda,
} from "./contacto";

function decodificar(firma: string): string {
  const cuerpo = firma.slice(1, -1);
  const bits = [...cuerpo].map((c) => (c === "\u200C" ? "1" : "0")).join("");
  let token = "";
  for (let i = 0; i < bits.length; i += 5) token += ALFABETO[parseInt(bits.slice(i, i + 5), 2)];
  return token;
}

describe("alfabeto", () => {
  it("tiene 32 caracteres sin ambiguos", () => {
    expect(ALFABETO).toHaveLength(32);
    expect(new Set(ALFABETO).size).toBe(32);
    for (const c of "IO01") expect(ALFABETO).not.toContain(c);
  });
});

describe("generarToken", () => {
  it("devuelve 6 caracteres del alfabeto", () => {
    for (let i = 0; i < 200; i++) expect(esTokenValido(generarToken())).toBe(true);
  });

  it("mapea cada byte con sus 5 bits bajos", () => {
    const fijo = () => Uint8Array.from([9, 29, 13, 24, 14, 21 + 32 * 5]);
    expect(generarToken(fijo)).toBe("K7P2QX");
  });

  it("usa crypto.getRandomValues por defecto", () => {
    const vistos = new Set(Array.from({ length: 50 }, () => generarToken()));
    expect(vistos.size).toBeGreaterThan(45);
  });
});

describe("firmaInvisible", () => {
  it("vector K7P2QX → índices 9, 29, 13, 24, 14, 21", () => {
    expect(indicesDeToken("K7P2QX")).toEqual([9, 29, 13, 24, 14, 21]);
  });

  it("codifica 30 bits MSB primero entre dos U+2060", () => {
    const firma = firmaInvisible("K7P2QX");
    expect(firma).toHaveLength(32);
    expect(firma[0]).toBe("\u2060");
    expect(firma[31]).toBe("\u2060");
    const bits = [...firma.slice(1, -1)].map((c) => (c === "\u200C" ? "1" : c === "\u200B" ? "0" : "?")).join("");
    expect(bits).toBe("01001" + "11101" + "01101" + "11000" + "01110" + "10101");
  });

  it("se decodifica de vuelta al token", () => {
    for (let i = 0; i < 50; i++) {
      const t = generarToken();
      expect(decodificar(firmaInvisible(t))).toBe(t);
    }
  });

  it("rechaza caracteres fuera del alfabeto", () => {
    expect(() => firmaInvisible("K7P2Q0")).toThrow();
  });
});

describe("textoContacto y urlWhatsApp", () => {
  it("arma el texto exacto del contrato", () => {
    const f = firmaInvisible("K7P2QX");
    expect(textoContacto("K7P2QX")).toBe(
      `Hola${f}, vi la web de FacturApp y quiero saber cómo funciona para mi distribuidora. (web K7P2QX)${f}`,
    );
  });

  it("apunta al número del bot con el texto codificado", () => {
    const url = urlWhatsApp("K7P2QX");
    expect(url.startsWith("https://wa.me/14244475253?text=")).toBe(true);
    const texto = decodeURIComponent(url.split("?text=")[1]);
    expect(texto).toBe(textoContacto("K7P2QX"));
    expect(url).toContain("%E2%81%A0");
  });
});

describe("utm y payload", () => {
  it("lee los utm de la URL de llegada", () => {
    expect(utmDeBusqueda("?utm_source=ig&utm_medium=reel&x=1")).toEqual({
      utm_source: "ig",
      utm_medium: "reel",
      utm_campaign: null,
    });
  });

  it("serializa exactamente las claves del contrato", () => {
    const json = JSON.parse(
      payloadClic({
        token: "K7P2QX",
        pagina: "/",
        demo: true,
        utm_source: "ig",
        utm_medium: null,
        utm_campaign: null,
        referrer: "",
      }),
    );
    expect(Object.keys(json)).toEqual([
      "token",
      "pagina",
      "demo",
      "utm_source",
      "utm_medium",
      "utm_campaign",
      "referrer",
    ]);
  });
});
