"use client";

import { alClicContacto } from "@/lib/contacto-navegador";
import { NUMERO_WHATSAPP } from "@/lib/contacto";
import { IconoChat, IconoFlecha } from "./iconos";

type Variante = "tinta" | "claro" | "texto";

const estilos: Record<Variante, string> = {
  tinta:
    "bg-tinta text-papel shadow-[0_1px_0_rgb(255_255_255/0.12)_inset,0_10px_30px_-12px_rgb(23_22_15/0.45)] hover:bg-tinta-2",
  claro:
    "bg-superficie text-tinta ring-1 ring-linea-fuerte shadow-[0_1px_0_rgb(255_255_255/0.9)_inset,0_8px_24px_-14px_rgb(23_22_15/0.25)] hover:ring-tinta/30",
  texto: "text-tinta hover:text-tinta-2",
};

export function BotonWhatsApp({
  variante = "tinta",
  children = "Hablar por WhatsApp",
  className = "",
}: {
  variante?: Variante;
  children?: React.ReactNode;
  className?: string;
}) {
  if (variante === "texto") {
    return (
      <a
        href={`https://wa.me/${NUMERO_WHATSAPP}`}
        target="_blank"
        rel="noopener noreferrer"
        onClick={alClicContacto}
        className={`group inline-flex items-center gap-1.5 text-sm font-medium underline-offset-4 hover:underline ${estilos.texto} ${className}`}
      >
        {children}
        <IconoFlecha
          size={14}
          className="ease-entrada transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-px"
        />
      </a>
    );
  }
  const fondoIcono = variante === "tinta" ? "bg-papel/12 text-papel" : "bg-tinta text-papel";
  return (
    <a
      href={`https://wa.me/${NUMERO_WHATSAPP}`}
      target="_blank"
      rel="noopener noreferrer"
      onClick={alClicContacto}
      className={`group ease-entrada inline-flex min-h-12 items-center gap-3 rounded-full py-1.5 pr-1.5 pl-5 text-[15px] font-medium tracking-[-0.01em] transition-[background-color,box-shadow,transform] duration-200 active:scale-[0.98] ${estilos[variante]} ${className}`}
    >
      <span>{children}</span>
      <span
        className={`ease-entrada grid size-9 place-items-center rounded-full transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-px group-hover:scale-105 ${fondoIcono}`}
      >
        <IconoChat size={17} />
      </span>
    </a>
  );
}
