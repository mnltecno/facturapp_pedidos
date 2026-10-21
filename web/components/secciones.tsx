import { BotonWhatsApp } from "./boton-whatsapp";
import { Demo } from "./demo/demo";
import { IconoAbajo, IconoCheck } from "./iconos";
import { Marca } from "./marca";
import { Reveal } from "./reveal";

const contenedor = "mx-auto w-full max-w-[1180px] px-4 sm:px-8";

function Ceja({ children }: { children: React.ReactNode }) {
  return (
    <span className="bg-superficie/70 text-gris ring-linea inline-flex items-center gap-2 rounded-full px-3 py-1 text-[11px] font-medium tracking-[0.16em] uppercase ring-1">
      <span className="bg-sello size-1.5 rounded-full" aria-hidden="true" />
      {children}
    </span>
  );
}

export function Encabezado() {
  return (
    <header className={`${contenedor} pt-5 sm:pt-7`}>
      <nav
        aria-label="Principal"
        className="bg-superficie/70 ring-linea flex items-center justify-between rounded-full py-1.5 pr-1.5 pl-4 shadow-[0_1px_0_rgb(255_255_255/0.8)_inset] ring-1"
      >
        <a href="#inicio" className="rounded-full" aria-label="FacturApp, inicio">
          <Marca />
        </a>
        <div className="flex items-center gap-1">
          <a
            href="#demo"
            className="text-tinta-2 hover:text-tinta hidden h-10 items-center rounded-full px-4 text-[14px] font-medium sm:inline-flex"
          >
            Demo
          </a>
          <a
            href="#precio"
            className="text-tinta-2 hover:text-tinta hidden h-10 items-center rounded-full px-4 text-[14px] font-medium sm:inline-flex"
          >
            Precio
          </a>
          <BotonWhatsApp variante="tinta" className="!min-h-10 !text-[14px] [&>span:last-child]:!size-7">
            WhatsApp
          </BotonWhatsApp>
        </div>
      </nav>
    </header>
  );
}

export function Hero() {
  return (
    <section id="inicio" className={`${contenedor} relative pt-20 pb-12 sm:pt-28 sm:pb-16 lg:pt-32`}>
      <div aria-hidden="true" className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[520px] overflow-hidden">
        <div className="absolute inset-0 bg-[repeating-linear-gradient(to_bottom,transparent_0,transparent_31px,var(--linea)_31px,var(--linea)_32px)] [mask-image:radial-gradient(70%_60%_at_50%_10%,black,transparent)]" />
        <div className="bg-sello/25 absolute top-0 left-[8%] h-full w-px [mask-image:linear-gradient(black,transparent)]" />
      </div>

      <div className="grid items-center gap-16 lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)] lg:gap-12">
        <div>
          <div className="entrada" style={{ "--retraso": "0ms" } as React.CSSProperties}>
            <Ceja>Para distribuidoras mayoristas</Ceja>
          </div>
          <h1
            className="entrada mt-7 max-w-[17ch] text-[clamp(2.6rem,6.6vw,5rem)] leading-[0.98] font-semibold tracking-[-0.045em] text-balance"
            style={{ "--retraso": "80ms" } as React.CSSProperties}
          >
            Tus clientes arman el pedido.{" "}
            <span className="text-tinta-2 font-serif font-normal tracking-[-0.02em] italic">Vos no tipeás nada.</span>
          </h1>
          <p
            className="entrada text-gris mt-7 max-w-[34rem] text-[17px] leading-relaxed sm:text-[19px]"
            style={{ "--retraso": "160ms" } as React.CSSProperties}
          >
            FacturApp es el sistema de gestión para tu distribuidora. Cada cliente pide desde el celular, con tus
            precios, y el pedido entra solo a la PC del negocio.
          </p>
          <div
            className="entrada mt-10 flex flex-col items-start gap-4 sm:flex-row sm:items-center"
            style={{ "--retraso": "240ms" } as React.CSSProperties}
          >
            <a
              href="#demo"
              className="group bg-tinta text-papel ease-entrada hover:bg-tinta-2 inline-flex min-h-12 items-center gap-3 rounded-full py-1.5 pr-1.5 pl-5 text-[15px] font-medium shadow-[0_1px_0_rgb(255_255_255/0.12)_inset,0_10px_30px_-12px_rgb(23_22_15/0.45)] transition-[background-color,transform] duration-200 active:scale-[0.98]"
            >
              Probar la demo
              <span className="bg-papel/12 ease-entrada grid size-9 place-items-center rounded-full transition-transform duration-300 group-hover:translate-y-0.5">
                <IconoAbajo size={17} />
              </span>
            </a>
            <div className="flex items-center gap-3">
              <BotonWhatsApp variante="claro" />
            </div>
          </div>
          <p className="entrada text-gris mt-4 text-[13px]" style={{ "--retraso": "300ms" } as React.CSSProperties}>
            Por WhatsApp te contestamos al toque.
          </p>
        </div>
        <PedidoEntrante />
      </div>
    </section>
  );
}

function PedidoEntrante() {
  const lineas: [string, string, string][] = [
    ["Yerba mate 1 kg × 10", "4", "$ 197.600"],
    ["Lavandina 2 L × 8", "3", "$ 31.200"],
    ["Aceite de girasol 1,5 L × 12", "2", "$ 82.368"],
  ];
  return (
    <div
      className="entrada relative mx-auto w-full max-w-[420px] lg:mr-0"
      style={{ "--retraso": "420ms" } as React.CSSProperties}
      aria-hidden="true"
    >
      <div className="bg-superficie/60 ring-linea absolute inset-x-6 -bottom-3 h-full rounded-[1.75rem] ring-1" />
      <div className="bg-tinta/[0.05] ring-linea relative rounded-[1.9rem] p-1.5 ring-1">
        <div className="bg-superficie rounded-[calc(1.9rem-6px)] p-5 shadow-[0_1px_0_rgb(255_255_255/0.9)_inset,0_30px_60px_-36px_rgb(23_22_15/0.4)] sm:p-6">
          <div className="flex items-center justify-between">
            <span className="text-gris flex items-center gap-2 text-[12.5px] font-medium">
              <span className="relative grid size-2 place-items-center">
                <span className="bg-pendiente/50 absolute size-2 rounded-full motion-safe:animate-ping motion-safe:[animation-iteration-count:3]" />
                <span className="bg-pendiente size-1.5 rounded-full" />
              </span>
              Pedido online nuevo
            </span>
            <span className="cifra text-gris-suave text-[12px]">hace un momento</span>
          </div>
          <div className="mt-5 flex items-baseline justify-between gap-4">
            <span className="cifra font-mono text-[15px] font-medium">#1043</span>
            <span className="text-tinta-2 truncate text-[14px]">Almacén de Marta · Avellaneda</span>
          </div>
          <ul className="border-linea-fuerte mt-4 border-t border-dashed">
            {lineas.map(([d, c, t]) => (
              <li key={d} className="cifra border-linea flex items-baseline gap-3 border-b py-2.5 text-[13.5px]">
                <span className="text-gris w-6 shrink-0">{c}×</span>
                <span className="min-w-0 flex-1 truncate">{d}</span>
                <span className="font-medium">{t}</span>
              </li>
            ))}
          </ul>
          <div className="mt-4 flex items-center justify-between">
            <span className="bg-pendiente-suave text-pendiente inline-flex h-7 items-center rounded-full px-2.5 text-[12px] font-medium">
              Pendiente
            </span>
            <span className="cifra text-[22px] font-semibold tracking-[-0.03em]">$ 311.168</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function Burbuja({
  children,
  lado = "izq",
  className = "",
}: {
  children: React.ReactNode;
  lado?: "izq" | "der";
  className?: string;
}) {
  return (
    <div
      className={`w-fit max-w-[88%] rounded-2xl px-3.5 py-2 text-[13.5px] leading-snug shadow-[0_1px_0.5px_rgb(0_0_0/0.08)] ${
        lado === "izq" ? "bg-superficie rounded-tl-md" : "ml-auto rounded-tr-md bg-[#e3efd9]"
      } ${className}`}
    >
      {children}
    </div>
  );
}

export function AntesAhora() {
  const lineas = [
    ["7790290003180", "Lavandina 2 L × 8", "3"],
    ["7790743006355", "Aceite de girasol 1,5 L × 12", "2"],
    ["7790336002139", "Yerba mate 1 kg × 10", "4"],
    ["7790060004171", "Fideos tallarín 500 g × 20", "5"],
  ];
  return (
    <section className={`${contenedor} py-24 sm:py-32`} aria-labelledby="t-antes">
      <Reveal className="max-w-2xl">
        <h2
          id="t-antes"
          className="text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.02] font-semibold tracking-[-0.04em] text-balance"
        >
          Se terminó pasar pedidos a mano.
        </h2>
      </Reveal>

      <div className="mt-14 grid gap-6 md:grid-cols-2 md:gap-8">
        <Reveal retraso={60}>
          <article className="bg-papel-hondo/70 ring-linea h-full rounded-[2rem] p-1.5 ring-1">
            <div className="flex h-full flex-col rounded-[calc(2rem-6px)] bg-[#e9e3d6] p-6 sm:p-8">
              <p className="text-gris text-[12px] font-medium tracking-[0.16em] uppercase">Antes</p>
              <div className="mt-6 space-y-2.5" aria-hidden="true">
                <Burbuja>
                  <span className="flex items-center gap-2.5">
                    <span className="bg-tinta text-papel grid size-7 place-items-center rounded-full">
                      <svg width="10" height="10" viewBox="0 0 10 10" fill="currentColor">
                        <path d="M2 1.2v7.6L8.6 5z" />
                      </svg>
                    </span>
                    <span className="flex h-5 items-center gap-[2px]">
                      {[6, 12, 8, 16, 10, 18, 7, 14, 9, 15, 6, 11, 8, 13, 5, 10].map((h, i) => (
                        <span key={i} className="bg-tinta/45 w-[2.5px] rounded-full" style={{ height: h }} />
                      ))}
                    </span>
                    <span className="cifra text-gris text-[12px]">0:47</span>
                  </span>
                </Burbuja>
                <Burbuja className="rotate-[-1.2deg]">
                  <span className="block h-24 w-44 rounded-lg bg-[repeating-linear-gradient(to_bottom,#f7f3ea_0,#f7f3ea_13px,#d9d1c0_13px,#d9d1c0_14px)] p-2">
                    <span className="bg-tinta/25 block h-1.5 w-24 rounded" />
                    <span className="bg-tinta/20 mt-2.5 block h-1.5 w-32 rounded" />
                    <span className="bg-tinta/25 mt-2.5 block h-1.5 w-20 rounded" />
                    <span className="bg-tinta/15 mt-2.5 block h-1.5 w-28 rounded" />
                  </span>
                  <span className="text-gris mt-1.5 block text-[12px]">la lista de esta semana</span>
                </Burbuja>
                <Burbuja>mandame lo mismo que la otra vez pero 2 más de lavandina</Burbuja>
                <Burbuja>¿el aceite sigue al mismo precio?</Burbuja>
              </div>
              <p className="text-tinta-2 mt-auto pt-8 text-[15px] leading-relaxed">
                Audios, fotos de listas y mensajes sueltos. Alguien los pasa a mano, se escapa una cantidad o un código,
                y a veces piden con la lista vieja.
              </p>
            </div>
          </article>
        </Reveal>

        <Reveal retraso={140}>
          <article className="bg-tinta/[0.04] ring-linea h-full rounded-[2rem] p-1.5 ring-1">
            <div className="bg-superficie flex h-full flex-col rounded-[calc(2rem-6px)] p-6 shadow-[0_1px_0_rgb(255_255_255/0.9)_inset] sm:p-8">
              <div className="flex items-center justify-between">
                <p className="text-gris text-[12px] font-medium tracking-[0.16em] uppercase">Ahora</p>
                <span className="bg-pendiente-suave text-pendiente inline-flex h-7 items-center rounded-full px-2.5 text-[12px] font-medium">
                  Pendiente
                </span>
              </div>
              <div className="ring-linea mt-6 rounded-2xl ring-1">
                <div className="border-linea-fuerte flex items-baseline justify-between border-b border-dashed px-4 py-3">
                  <span className="cifra font-mono text-[13px] font-medium">Pedido #1043</span>
                  <span className="text-gris text-[12px]">Gómez, Marta</span>
                </div>
                <table className="w-full text-[13px]">
                  <caption className="sr-only">Ejemplo de pedido ordenado</caption>
                  <thead className="sr-only">
                    <tr>
                      <th scope="col">Código</th>
                      <th scope="col">Producto</th>
                      <th scope="col">Cantidad</th>
                    </tr>
                  </thead>
                  <tbody className="cifra">
                    {lineas.map(([ean, d, c]) => (
                      <tr key={ean} className="border-linea border-b last:border-0">
                        <td className="text-gris-suave hidden py-2.5 pl-4 font-mono text-[11.5px] sm:table-cell">
                          {ean}
                        </td>
                        <td className="py-2.5 pr-2 pl-4 sm:pl-3">{d}</td>
                        <td className="py-2.5 pr-4 text-right font-medium">× {c}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-tinta-2 mt-auto pt-8 text-[15px] leading-relaxed">
                El cliente elige de tu catálogo, con el precio de hoy. El pedido llega con código, cantidad y total,
                listo para importar.
              </p>
            </div>
          </article>
        </Reveal>
      </div>
    </section>
  );
}

export function SeccionDemo() {
  return (
    <section
      id="demo"
      className="border-linea bg-papel-hondo/45 scroll-mt-4 border-y py-24 sm:py-32"
      aria-labelledby="t-demo"
    >
      <div className={contenedor}>
        <Reveal className="max-w-2xl">
          <Ceja>Demo</Ceja>
          <h2
            id="t-demo"
            className="mt-6 text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.02] font-semibold tracking-[-0.04em] text-balance"
          >
            Probalo como lo haría <span className="font-serif font-normal tracking-[-0.01em] italic">tu cliente.</span>
          </h2>
          <p className="text-gris mt-5 max-w-xl text-[17px] leading-relaxed">
            Armá un pedido en el teléfono y mirá cómo llega a la PC del negocio. Tu cliente se registra una sola vez con
            su mail; acá ya entramos por él.
          </p>
        </Reveal>
        <div className="mt-6">
          <Demo />
        </div>
      </div>
    </section>
  );
}

const PUNTOS = [
  {
    t: "Un link propio",
    d: "Cada distribuidora tiene el suyo. El cliente lo abre en el celular y pide cuando quiere, sin bajar nada de ningún store.",
  },
  { t: "Precios al día", d: "Cambiás un precio en FacturApp y el catálogo del celular ya muestra el nuevo." },
  {
    t: "De pendiente a importado",
    d: "Los pedidos online llegan como pendientes. Los importás y quedan cargados en el sistema.",
  },
  { t: "Listo para el reparto", d: "La dirección de cada cliente se usa para armar la hoja de ruta." },
];

export function ComoLlega() {
  return (
    <section className={`${contenedor} py-24 sm:py-32`} aria-labelledby="t-como">
      <div className="grid gap-14 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)] lg:gap-20">
        <Reveal>
          <h2
            id="t-como"
            className="text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.02] font-semibold tracking-[-0.04em] text-balance"
          >
            Tu PC manda el catálogo.{" "}
            <span className="text-tinta-2 font-serif font-normal tracking-[-0.01em] italic">
              El celular devuelve pedidos.
            </span>
          </h2>
          <Diagrama />
        </Reveal>
        <dl className="grid content-start gap-x-10 sm:grid-cols-2">
          {PUNTOS.map((p, i) => (
            <Reveal key={p.t} retraso={i * 60} className="border-linea-fuerte border-t py-7">
              <dt className="text-[17px] font-semibold tracking-[-0.02em]">{p.t}</dt>
              <dd className="text-gris mt-2 text-[15px] leading-relaxed">{p.d}</dd>
            </Reveal>
          ))}
        </dl>
      </div>
    </section>
  );
}

function Diagrama() {
  return (
    <figure className="mt-12">
      <svg viewBox="0 0 420 150" className="h-auto w-full max-w-[460px]" role="img" aria-labelledby="diag-t">
        <title id="diag-t">La PC envía catálogo y precios al celular; el celular devuelve los pedidos a la PC.</title>
        <g fill="none" stroke="var(--tinta)" strokeWidth="1.4">
          <rect x="8" y="34" width="112" height="72" rx="10" fill="var(--superficie)" />
          <path d="M48 122h32M64 106v16" />
          <rect x="336" y="22" width="60" height="106" rx="14" fill="var(--superficie)" />
          <path d="M358 116h16" />
        </g>
        <path className="trazo-flujo" d="M132 58 H322" stroke="var(--tinta)" strokeWidth="1.4" fill="none" />
        <path
          d="m316 53 7 5-7 5"
          stroke="var(--tinta)"
          strokeWidth="1.4"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path className="trazo-flujo" d="M322 92 H132" stroke="var(--sello)" strokeWidth="1.4" fill="none" />
        <path
          d="m138 87-7 5 7 5"
          stroke="var(--sello)"
          strokeWidth="1.4"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <text x="227" y="48" textAnchor="middle" fontSize="11" fill="var(--gris)" fontFamily="var(--font-geist)">
          catálogo y precios
        </text>
        <text x="227" y="112" textAnchor="middle" fontSize="11" fill="var(--sello)" fontFamily="var(--font-geist)">
          pedidos
        </text>
        <text
          x="64"
          y="74"
          textAnchor="middle"
          fontSize="12"
          fontWeight="600"
          fill="var(--tinta)"
          fontFamily="var(--font-geist)"
        >
          FacturApp
        </text>
        <text x="366" y="78" textAnchor="middle" fontSize="10.5" fill="var(--gris)" fontFamily="var(--font-geist)">
          cliente
        </text>
      </svg>
    </figure>
  );
}

const CONDICIONES = [
  "Un solo pago. No es un abono mensual.",
  "Soporte incluido y en persona: te atienden Miguel y Manuel, no un call center.",
  "Licencia para una PC.",
  "Después del pago, Miguel coordina la instalación con vos.",
];

export function Precio() {
  return (
    <section id="precio" className={`${contenedor} scroll-mt-4 pb-24 sm:pb-32`} aria-labelledby="t-precio">
      <Reveal>
        <div className="bg-tinta/[0.04] ring-linea rounded-[2.25rem] p-1.5 ring-1">
          <div className="bg-superficie grid gap-10 rounded-[calc(2.25rem-6px)] p-7 shadow-[0_1px_0_rgb(255_255_255/0.9)_inset,0_40px_80px_-60px_rgb(23_22_15/0.4)] sm:p-12 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)] lg:gap-16 lg:p-16">
            <div>
              <h2
                id="t-precio"
                className="text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.02] font-semibold tracking-[-0.04em]"
              >
                Se paga <span className="font-serif font-normal italic">una vez.</span>
              </h2>
              <p className="mt-8 flex items-baseline gap-3">
                <span className="cifra text-[clamp(3.2rem,9vw,5.4rem)] leading-none font-semibold tracking-[-0.05em]">
                  $300.000
                </span>
              </p>
              <p className="text-gris mt-3 text-[15px]">Pesos argentinos.</p>
              <div className="mt-9">
                <BotonWhatsApp>Consultar por WhatsApp</BotonWhatsApp>
              </div>
            </div>
            <ul className="self-end">
              {CONDICIONES.map((c) => (
                <li
                  key={c}
                  className="border-linea flex gap-4 border-t py-5 text-[16px] leading-relaxed first:border-t-0 lg:first:border-t"
                >
                  <span className="bg-listo-suave text-listo mt-1 grid size-6 shrink-0 place-items-center rounded-full">
                    <IconoCheck size={14} />
                  </span>
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Reveal>
    </section>
  );
}

export function Cierre() {
  return (
    <section id="contacto" className={`${contenedor} pb-24 text-center sm:pb-32`} aria-labelledby="t-cierre">
      <Reveal className="mx-auto max-w-2xl">
        <h2
          id="t-cierre"
          className="text-[clamp(2.2rem,5.4vw,4rem)] leading-[1] font-semibold tracking-[-0.045em] text-balance"
        >
          Contanos cómo trabaja{" "}
          <span className="font-serif font-normal tracking-[-0.01em] italic">tu distribuidora.</span>
        </h2>
        <p className="text-gris mx-auto mt-6 max-w-md text-[17px] leading-relaxed">
          Escribinos por WhatsApp y vemos juntos si FacturApp te sirve.
        </p>
        <div className="mt-10 flex flex-col items-center gap-3">
          <BotonWhatsApp />
          <span className="text-gris text-[13px]">Te contestamos al toque.</span>
        </div>
      </Reveal>
    </section>
  );
}

export function Pie() {
  return (
    <footer className="border-linea border-t">
      <div
        className={`${contenedor} flex flex-col items-start justify-between gap-5 py-10 pb-[max(2.5rem,env(safe-area-inset-bottom))] sm:flex-row sm:items-center`}
      >
        <div>
          <Marca />
          <p className="text-gris mt-2 text-[13px]">Sistema de gestión para distribuidoras.</p>
        </div>
        <BotonWhatsApp variante="texto">Hablar por WhatsApp</BotonWhatsApp>
      </div>
    </footer>
  );
}
