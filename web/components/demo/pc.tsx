"use client";

import { AnimatePresence, motion } from "motion/react";
import { useState, type Dispatch } from "react";
import { IconoUbicacion } from "../iconos";
import { pesos } from "./datos";
import type { Accion, Estado, EstadoPedido, PedidoPC } from "./estado";

const resorte = { type: "spring", stiffness: 420, damping: 34 } as const;

export function PC({ estado, enviar }: { estado: Estado; enviar: Dispatch<Accion> }) {
  const pendientes = estado.pedidos.filter((p) => p.estado === "Pendiente").length;
  const hayNuevo = estado.pedidos.some((p) => p.id >= 1043);
  const [abiertos, setAbiertos] = useState<Record<number, boolean>>({});

  const estaAbierto = (p: PedidoPC) => abiertos[p.id] ?? (p.id === estado.pedidos[0]?.id && p.id >= 1043);

  return (
    <div className="bg-tinta/[0.04] ring-linea rounded-[1.6rem] p-1.5 ring-1">
      <div
        className="bg-superficie overflow-hidden rounded-[calc(1.6rem-6px)] shadow-[0_1px_0_rgb(255_255_255/0.9)_inset,0_30px_60px_-40px_rgb(23_22_15/0.35)]"
        role="region"
        aria-label="Simulación de FacturApp en la PC del negocio"
      >
        <div
          className="border-linea bg-papel/60 flex h-10 items-center justify-between border-b pr-1 pl-4"
          aria-hidden="true"
        >
          <span className="text-tinta-2 flex items-center gap-2 text-[12px] font-medium">
            <span className="bg-tinta text-papel grid size-4 place-items-center rounded-[5px] text-[9px] font-bold">
              F
            </span>
            FacturApp — Pedidos online
          </span>
          <span className="text-gris flex">
            {["M5 12h14", "M6 6h12v12H6z", "M7 7l10 10M17 7 7 17"].map((d) => (
              <span key={d} className="grid h-9 w-10 place-items-center">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
                  <path d={d} />
                </svg>
              </span>
            ))}
          </span>
        </div>

        <div className="flex flex-wrap items-end justify-between gap-3 px-4 pt-5 pb-4 sm:px-6">
          <div>
            <p className="text-[19px] font-semibold tracking-[-0.02em]">Pedidos online</p>
            <p className="text-gris mt-0.5 text-[13px]">Lo que tus clientes confirmaron desde el celular.</p>
          </div>
          <span
            className={`cifra inline-flex h-8 items-center gap-2 rounded-full px-3 text-[12.5px] font-medium transition-colors duration-300 ${
              pendientes ? "bg-pendiente-suave text-pendiente" : "bg-papel text-gris ring-linea ring-1"
            }`}
            aria-live="polite"
          >
            <span className={`size-1.5 rounded-full ${pendientes ? "bg-pendiente" : "bg-gris-suave"}`} />
            {pendientes === 0 ? "Sin pendientes" : pendientes === 1 ? "1 pendiente" : `${pendientes} pendientes`}
          </span>
        </div>

        <div className="border-linea bg-papel/50 text-gris hidden grid-cols-[4.5rem_1fr_4rem_7.5rem_7.5rem] gap-3 border-y px-6 py-2 text-[11px] font-medium tracking-[0.08em] uppercase md:grid">
          <span>N.º</span>
          <span>Cliente</span>
          <span>Hora</span>
          <span className="text-right">Total</span>
          <span className="text-right">Estado</span>
        </div>

        <ul className="divide-linea border-linea divide-y border-t md:border-t-0">
          {!hayNuevo && (
            <li className="flex items-center gap-3 px-4 py-4 sm:px-6">
              <span className="relative grid size-2.5 place-items-center">
                <span className="bg-pendiente/40 absolute size-2.5 rounded-full motion-safe:animate-ping" />
                <span className="bg-pendiente size-1.5 rounded-full" />
              </span>
              <p className="text-gris text-[13.5px]">Esperando pedidos. Confirmá uno en el teléfono y aparece acá.</p>
            </li>
          )}
          <AnimatePresence initial={false}>
            {estado.pedidos.map((p) => (
              <Fila
                key={p.id}
                p={p}
                abierto={estaAbierto(p)}
                alternar={() => setAbiertos((a) => ({ ...a, [p.id]: !estaAbierto(p) }))}
                importar={() => enviar({ t: "importar", id: p.id })}
              />
            ))}
          </AnimatePresence>
        </ul>
      </div>
    </div>
  );
}

function Chip({ estado }: { estado: EstadoPedido }) {
  const clase =
    estado === "Pendiente"
      ? "bg-pendiente-suave text-pendiente"
      : estado === "Importado"
        ? "bg-listo-suave text-listo"
        : "bg-papel text-gris";
  return (
    <AnimatePresence initial={false} mode="popLayout">
      <motion.span
        key={estado}
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
        className={`inline-flex h-7 items-center rounded-full px-2.5 text-[12px] font-medium ${clase}`}
      >
        {estado}
      </motion.span>
    </AnimatePresence>
  );
}

function Fila({
  p,
  abierto,
  alternar,
  importar,
}: {
  p: PedidoPC;
  abierto: boolean;
  alternar: () => void;
  importar: () => void;
}) {
  const idDetalle = `detalle-${p.id}`;
  return (
    <motion.li
      layout="position"
      initial={{ opacity: 0, y: -14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={resorte}
      className="relative"
    >
      {p.nuevo && (
        <motion.span
          aria-hidden="true"
          className="bg-pendiente-suave pointer-events-none absolute inset-0"
          initial={{ opacity: 0.9 }}
          animate={{ opacity: 0 }}
          transition={{ duration: 2.4, ease: [0.22, 1, 0.36, 1], delay: 0.4 }}
        />
      )}
      <div className="relative grid grid-cols-[1fr_auto] items-center gap-x-3 gap-y-1 px-4 py-3.5 sm:px-6 md:grid-cols-[4.5rem_1fr_4rem_7.5rem_7.5rem]">
        <button
          type="button"
          onClick={alternar}
          aria-expanded={abierto}
          aria-controls={idDetalle}
          className="col-span-1 flex min-w-0 items-center gap-3 rounded-lg text-left md:col-span-3 md:grid md:grid-cols-[4.5rem_1fr_4rem] md:gap-3"
        >
          <span className="cifra font-mono text-[13px] font-medium">#{p.id}</span>
          <span className="min-w-0">
            <span className="block truncate text-[14px] font-medium">{p.cliente}</span>
            <span className="cifra text-gris block text-[12px] md:hidden">
              {p.hora} · {p.lineas.length} {p.lineas.length === 1 ? "producto" : "productos"}
            </span>
          </span>
          <span className="cifra text-gris hidden text-[13px] md:block">{p.hora}</span>
        </button>
        <span className="cifra row-span-2 text-right text-[14px] font-semibold md:row-span-1">{pesos(p.total)}</span>
        <span className="col-span-1 flex items-center gap-2 md:col-span-1 md:justify-end">
          <Chip estado={p.estado} />
        </span>
      </div>

      <AnimatePresence initial={false}>
        {abierto && (
          <motion.div
            id={idDetalle}
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.32, ease: [0.25, 1, 0.5, 1] }}
            className="relative overflow-hidden"
          >
            <div className="bg-papel/70 ring-linea relative mx-4 mb-4 rounded-2xl p-4 ring-1 sm:mx-6">
              <table className="w-full text-[12.5px]">
                <caption className="sr-only">Detalle del pedido {p.id}</caption>
                <thead className="text-gris text-[10.5px] tracking-[0.08em] uppercase">
                  <tr>
                    <th className="hidden pb-2 text-left font-medium sm:table-cell">EAN13</th>
                    <th className="pb-2 text-left font-medium">Descripción</th>
                    <th className="pb-2 text-right font-medium">Cant.</th>
                    <th className="hidden pb-2 text-right font-medium sm:table-cell">Precio</th>
                    <th className="pb-2 text-right font-medium">Subtotal</th>
                  </tr>
                </thead>
                <tbody className="cifra">
                  {p.lineas.map((l) => (
                    <tr key={l.ean13} className="border-linea border-t">
                      <td className="text-gris hidden py-1.5 pr-3 font-mono text-[11.5px] sm:table-cell">{l.ean13}</td>
                      <td className="py-1.5 pr-2">{l.descripcion}</td>
                      <td className="py-1.5 text-right">{l.cantidad}</td>
                      <td className="text-gris hidden py-1.5 pl-3 text-right sm:table-cell">
                        {pesos(l.precio_unitario)}
                      </td>
                      <td className="py-1.5 pl-3 text-right font-medium">{pesos(l.subtotal)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="border-linea mt-3 flex flex-wrap items-center justify-between gap-3 border-t pt-3">
                <p className="text-gris flex items-center gap-1.5 text-[12px]">
                  <IconoUbicacion size={14} />
                  <span>
                    {p.direccion} <span className="text-gris-suave">· va a la hoja de ruta</span>
                  </span>
                </p>
                <AnimatePresence mode="popLayout" initial={false}>
                  {p.estado === "Pendiente" ? (
                    <motion.button
                      key="importar"
                      type="button"
                      onClick={importar}
                      exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.12 } }}
                      whileTap={{ scale: 0.96 }}
                      className="bg-tinta text-papel hover:bg-tinta-2 h-10 rounded-full px-5 text-[13.5px] font-medium shadow-[0_1px_0_rgb(255_255_255/0.12)_inset]"
                    >
                      Importar pedido
                    </motion.button>
                  ) : p.id >= 1043 && p.estado === "Importado" ? (
                    <motion.span
                      key="sello"
                      aria-hidden="true"
                      initial={{ opacity: 0, scale: 1.6, rotate: -14 }}
                      animate={{ opacity: 0.88, scale: 1, rotate: -8 }}
                      transition={{ type: "spring", stiffness: 520, damping: 22 }}
                      className="border-sello text-sello pointer-events-none ml-auto inline-flex h-10 items-center rounded-md border-2 px-3 font-mono text-[13px] font-bold tracking-[0.18em] mix-blend-multiply"
                    >
                      IMPORTADO
                    </motion.span>
                  ) : null}
                </AnimatePresence>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.li>
  );
}
