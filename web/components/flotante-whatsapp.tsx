"use client";

import { AnimatePresence, MotionConfig, motion } from "motion/react";
import { useEffect, useState } from "react";
import { alClicContacto } from "@/lib/contacto-navegador";
import { NUMERO_WHATSAPP } from "@/lib/contacto";
import { IconoChat } from "./iconos";

// Aparece cuando el hero ya quedó atrás y se corre cuando hay en pantalla algo
// que no debe tapar: la demo (el botón de confirmar del teléfono vive abajo),
// el cierre y el pie, que ya tienen su propio CTA.
const QUE_NO_TAPA = ["#inicio", "#demo", "#contacto", "footer"];

export function FlotanteWhatsApp() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const enPantalla = new Map<Element, boolean>();
    const io = new IntersectionObserver(
      (entradas) => {
        for (const e of entradas) enPantalla.set(e.target, e.isIntersecting);
        setVisible(![...enPantalla.values()].some(Boolean));
      },
      { rootMargin: "0px 0px -18% 0px" },
    );
    for (const sel of QUE_NO_TAPA) {
      const el = document.querySelector(sel);
      if (el) {
        enPantalla.set(el, true);
        io.observe(el);
      }
    }
    return () => io.disconnect();
  }, []);

  return (
    <MotionConfig reducedMotion="user">
      <AnimatePresence>
        {visible && (
          <motion.a
            key="flotante"
            href={`https://wa.me/${NUMERO_WHATSAPP}`}
            target="_blank"
            rel="noopener noreferrer"
            onClick={alClicContacto}
            aria-label="Hablar por WhatsApp. Te contestamos al toque."
            initial={{ opacity: 0, y: 24, scale: 0.92 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 16, scale: 0.96, transition: { duration: 0.16 } }}
            transition={{ type: "spring", stiffness: 420, damping: 30, delay: 0.1 }}
            whileHover={{ y: -2 }}
            whileTap={{ scale: 0.96 }}
            className="group bg-tinta text-papel fixed right-4 bottom-[max(1rem,env(safe-area-inset-bottom))] z-40 inline-flex min-h-12 items-center gap-2.5 rounded-full py-1.5 pr-1.5 pl-4 text-[14.5px] font-medium shadow-[0_1px_0_rgb(255_255_255/0.14)_inset,0_18px_40px_-16px_rgb(23_22_15/0.55),0_4px_12px_-6px_rgb(23_22_15/0.3)] sm:right-6 sm:bottom-6"
          >
            <span className="flex flex-col leading-tight">
              <span>WhatsApp</span>
              <span className="text-papel/65 hidden text-[11.5px] font-normal sm:block">Te contestamos al toque</span>
            </span>
            <span className="bg-papel/12 ease-entrada grid size-9 place-items-center rounded-full transition-transform duration-300 group-hover:rotate-[-8deg] group-active:scale-90">
              <IconoChat size={17} />
            </span>
          </motion.a>
        )}
      </AnimatePresence>
    </MotionConfig>
  );
}
