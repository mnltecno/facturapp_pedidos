import { esTokenValido, generarToken, payloadClic, URL_CLIC, urlWhatsApp, utmDeBusqueda, type Utm } from "./contacto";

const CLAVE_TOKEN = "fa_token";
const CLAVE_UTM = "fa_utm";
const CLAVE_DEMO = "fa_demo";

const memoria: Record<string, string> = {};

function leer(clave: string): string | null {
  try {
    const v = window.sessionStorage.getItem(clave);
    if (v !== null) return v;
  } catch {}
  return memoria[clave] ?? null;
}

function guardar(clave: string, valor: string) {
  memoria[clave] = valor;
  try {
    window.sessionStorage.setItem(clave, valor);
  } catch {}
}

export function tokenVisitante(): string {
  const guardado = leer(CLAVE_TOKEN);
  if (esTokenValido(guardado)) return guardado;
  const nuevo = generarToken();
  guardar(CLAVE_TOKEN, nuevo);
  return nuevo;
}

// Los utm de la URL de llegada se pierden si el visitante navega por anclas o
// recarga sin query: se guardan al entrar y sólo los pisa otra llegada con utm.
export function registrarLlegada() {
  const utm = utmDeBusqueda(window.location.search);
  const traeUtm = Boolean(utm.utm_source || utm.utm_medium || utm.utm_campaign);
  if (!traeUtm && leer(CLAVE_UTM) !== null) return;
  guardar(CLAVE_UTM, JSON.stringify(utm));
}

function utmGuardados(): Utm {
  try {
    const v = leer(CLAVE_UTM);
    if (v) return JSON.parse(v) as Utm;
  } catch {}
  return utmDeBusqueda(window.location.search);
}

export function marcarDemoUsada() {
  if (leer(CLAVE_DEMO) === "1") return;
  guardar(CLAVE_DEMO, "1");
}

export function demoUsada(): boolean {
  return leer(CLAVE_DEMO) === "1";
}

function avisarClic(token: string) {
  try {
    const body = payloadClic({
      token,
      pagina: window.location.pathname,
      demo: demoUsada(),
      ...utmGuardados(),
      referrer: document.referrer,
    });
    if (typeof navigator.sendBeacon === "function") {
      navigator.sendBeacon(URL_CLIC, body);
      return;
    }
    void fetch(URL_CLIC, { method: "POST", keepalive: true, mode: "no-cors", body }).catch(() => {});
  } catch {}
}

// Se reescribe el href dentro del click: el navegador lee el href recién al
// ejecutar la acción por defecto, así se abre la pestaña nueva sin window.open
// (que los bloqueadores de popups cortan en algunos celulares).
export function alClicContacto(e: { currentTarget: HTMLAnchorElement }) {
  try {
    const token = tokenVisitante();
    e.currentTarget.href = urlWhatsApp(token);
    avisarClic(token);
  } catch {}
}
