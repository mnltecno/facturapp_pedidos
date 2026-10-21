"use client";

import { AnimatePresence, MotionConfig, motion } from "motion/react";
import { useCallback, useReducer, useRef } from "react";
import { marcarDemoUsada } from "@/lib/contacto-navegador";
import { IconoPC, IconoReiniciar, IconoTelefono } from "../iconos";
import { inicial, reductor, type Accion } from "./estado";
import { PC } from "./pc";
import { Telefono } from "./telefono";

export function Demo() {
  const [estado, despachar] = useReducer(reductor, inicial);
  const refPC = useRef<HTMLDivElement>(null);

  const enviar = useCallback((a: Accion) => {
    if (a.t !== "reiniciar") marcarDemoUsada();
    despachar(a);
  }, []);

  const irAPC = useCallback(() => {
    const reducir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    refPC.current?.scrollIntoView({ behavior: reducir ? "auto" : "smooth", block: "start" });
  }, []);

  const tocada = estado !== inicial;

  return (
    <MotionConfig reducedMotion="user">
      <div className="mb-6 flex min-h-11 items-center justify-end">
        <AnimatePresence>
          {tocada && (
            <motion.button
              type="button"
              onClick={() => despachar({ t: "reiniciar" })}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 6 }}
              transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
              className="text-tinta-2 ring-linea-fuerte hover:bg-superficie inline-flex h-11 items-center gap-2 rounded-full px-4 text-[14px] font-medium ring-1"
            >
              <IconoReiniciar size={16} />
              Empezar de nuevo
            </motion.button>
          )}
        </AnimatePresence>
      </div>

      <div className="grid items-start gap-14 lg:grid-cols-[372px_minmax(0,1fr)] lg:gap-16 xl:gap-20">
        <div>
          <Etiqueta
            icono={<IconoTelefono size={16} />}
            titulo="El celular de tu cliente"
            detalle="Una página web con tu catálogo"
          />
          <Telefono estado={estado} enviar={enviar} irAPC={irAPC} />
        </div>
        <div ref={refPC} className="scroll-mt-6 lg:sticky lg:top-10">
          <Etiqueta icono={<IconoPC size={16} />} titulo="Tu PC con FacturApp" detalle="Donde caen los pedidos" />
          <PC estado={estado} enviar={enviar} />
          <p className="text-gris mt-5 max-w-md text-[13.5px] leading-relaxed">
            Los datos de esta demo son de prueba. En tu FacturApp, el catálogo y los precios son los que cargás vos.
          </p>
        </div>
      </div>
    </MotionConfig>
  );
}

function Etiqueta({ icono, titulo, detalle }: { icono: React.ReactNode; titulo: string; detalle: string }) {
  return (
    <div className="mb-4 flex items-center gap-3 lg:mb-5">
      <span className="bg-superficie text-tinta ring-linea grid size-8 place-items-center rounded-full ring-1">
        {icono}
      </span>
      <p className="text-[14px] leading-tight">
        <span className="block font-medium">{titulo}</span>
        <span className="text-gris">{detalle}</span>
      </p>
    </div>
  );
}
