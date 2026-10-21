"use client";

import { AnimatePresence, motion, type Transition } from "motion/react";
import { useEffect, useId, useMemo, useRef, type Dispatch } from "react";
import {
  IconoAbajo,
  IconoAtras,
  IconoBasura,
  IconoBuscar,
  IconoCarrito,
  IconoCerrar,
  IconoCheck,
  IconoChat,
  IconoMas,
  IconoMenos,
  IconoUbicacion,
} from "../iconos";
import { CLIENTE, DISTRIBUIDORA, FAMILIAS, PRODUCTOS, normalizar, pesos, precioFinal, type Producto } from "./datos";
import { lineasDe, resumen, type Accion, type Estado } from "./estado";

const resorte: Transition = { type: "spring", stiffness: 520, damping: 36, mass: 0.7 };
const cajon: Transition = { duration: 0.42, ease: [0.32, 0.72, 0, 1] };

export function Telefono({ estado, enviar, irAPC }: { estado: Estado; enviar: Dispatch<Accion>; irAPC: () => void }) {
  const dir = estado.direccion;

  return (
    <div className="mx-auto w-full max-w-[372px]">
      <div className="rounded-[3rem] bg-[#1d1c17] p-[9px] shadow-[0_0_0_1px_rgb(255_255_255/0.06)_inset,0_1px_0_rgb(255_255_255/0.14)_inset,0_40px_80px_-40px_rgb(23_22_15/0.55),0_18px_36px_-24px_rgb(23_22_15/0.35)]">
        <div
          className="bg-superficie relative isolate h-[min(700px,calc(100dvh-7rem))] min-h-[560px] overflow-hidden rounded-[calc(3rem-9px)]"
          role="region"
          aria-label="Simulación de la app de pedidos en el celular del cliente"
        >
          <BarraEstado />
          <AnimatePresence initial={false} custom={dir} mode="popLayout">
            <motion.div
              key={estado.pantalla}
              custom={dir}
              variants={{
                entra: (d: number) => ({ x: d > 0 ? "28%" : "-28%", opacity: 0 }),
                quieta: { x: 0, opacity: 1 },
                sale: (d: number) => ({ x: d > 0 ? "-18%" : "18%", opacity: 0 }),
              }}
              initial="entra"
              animate="quieta"
              exit="sale"
              transition={cajon}
              className="absolute inset-x-0 top-9 bottom-0 flex flex-col"
            >
              {estado.pantalla === "catalogo" && <Catalogo estado={estado} enviar={enviar} />}
              {estado.pantalla === "pedido" && <MiPedido estado={estado} enviar={enviar} />}
              {estado.pantalla === "exito" && <Exito estado={estado} enviar={enviar} irAPC={irAPC} />}
            </motion.div>
          </AnimatePresence>
          <AnimatePresence>
            {estado.vistaWhatsApp && estado.confirmado && (
              <VistaWhatsApp
                mensaje={estado.confirmado.mensaje}
                cerrar={() => enviar({ t: "whatsapp", abierto: false })}
              />
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

function BarraEstado() {
  return (
    <div
      className="text-tinta absolute inset-x-0 top-0 z-20 flex h-9 items-center justify-between px-7 text-[12px] font-semibold"
      aria-hidden="true"
    >
      <span className="cifra">9:41</span>
      <span className="absolute top-2 left-1/2 h-[22px] w-[86px] -translate-x-1/2 rounded-full bg-[#1d1c17]" />
      <span className="flex items-center gap-1">
        <svg width="16" height="10" viewBox="0 0 16 10" fill="currentColor">
          <rect x="0" y="6" width="3" height="4" rx="1" />
          <rect x="4.3" y="4" width="3" height="6" rx="1" />
          <rect x="8.6" y="2" width="3" height="8" rx="1" />
          <rect x="12.9" y="0" width="3" height="10" rx="1" />
        </svg>
        <svg width="22" height="11" viewBox="0 0 22 11" fill="none">
          <rect x="0.5" y="0.5" width="18" height="10" rx="3" stroke="currentColor" opacity=".45" />
          <rect x="2" y="2" width="13" height="7" rx="1.6" fill="currentColor" />
          <rect x="19.6" y="3.6" width="1.6" height="3.8" rx=".8" fill="currentColor" opacity=".45" />
        </svg>
      </span>
    </div>
  );
}

function Catalogo({ estado, enviar }: { estado: Estado; enviar: Dispatch<Accion> }) {
  const idBuscar = useId();
  const { items, total } = resumen(estado.carrito);
  const visibles = useMemo(() => {
    const q = normalizar(estado.busqueda.trim());
    return PRODUCTOS.filter(
      (p) => (!estado.familia || p.familia === estado.familia) && (!q || normalizar(p.descripcion).includes(q)),
    );
  }, [estado.busqueda, estado.familia]);
  const tocado = Object.keys(estado.carrito).length > 0;

  return (
    <>
      <header className="flex items-start justify-between gap-3 px-5 pt-3 pb-3">
        <div className="min-w-0">
          <p className="truncate text-[17px] font-semibold tracking-[-0.02em]">{DISTRIBUIDORA}</p>
          <p className="text-gris text-[13px]">Hola, {CLIENTE.nombre}. Armá tu pedido.</p>
        </div>
        <button
          type="button"
          onClick={() => items > 0 && enviar({ t: "ir", pantalla: "pedido" })}
          disabled={items === 0}
          aria-label={items ? `Ver pedido, ${items} ítems` : "El pedido está vacío"}
          className="bg-papel text-tinta ring-linea ease-entrada relative grid size-11 shrink-0 place-items-center rounded-full ring-1 transition-transform duration-150 active:scale-95 disabled:opacity-60"
        >
          <IconoCarrito size={19} />
          <AnimatePresence>
            {items > 0 && (
              <motion.span
                key={items}
                initial={{ scale: 0.6, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.6, opacity: 0 }}
                transition={resorte}
                className="cifra bg-sello absolute -top-1 -right-1 grid h-5 min-w-5 place-items-center rounded-full px-1 text-[11px] font-semibold text-white"
              >
                {items}
              </motion.span>
            )}
          </AnimatePresence>
        </button>
      </header>

      <div className="px-5">
        <label htmlFor={idBuscar} className="sr-only">
          Buscar producto
        </label>
        <div className="bg-papel ring-linea focus-within:ring-tinta/40 flex h-11 items-center gap-2 rounded-2xl px-3.5 ring-1">
          <IconoBuscar size={17} className="text-gris shrink-0" />
          <input
            id={idBuscar}
            type="search"
            inputMode="search"
            autoComplete="off"
            placeholder="Buscar producto"
            value={estado.busqueda}
            onChange={(e) => enviar({ t: "buscar", texto: e.target.value })}
            className="placeholder:text-gris-suave h-full w-full min-w-0 bg-transparent text-[16px] outline-none focus-visible:outline-none [&::-webkit-search-cancel-button]:hidden"
          />
          {estado.busqueda && (
            <button
              type="button"
              onClick={() => enviar({ t: "buscar", texto: "" })}
              aria-label="Borrar búsqueda"
              className="text-gris hover:text-tinta -mr-2 grid size-9 shrink-0 place-items-center rounded-full"
            >
              <IconoCerrar size={15} />
            </button>
          )}
        </div>
      </div>

      <div
        role="group"
        aria-label="Filtrar por familia"
        className="sin-barra mt-3 flex gap-2 overflow-x-auto px-5 pb-1"
      >
        {[null, ...FAMILIAS].map((f) => {
          const activa = estado.familia === f;
          return (
            <button
              key={f ?? "todos"}
              type="button"
              aria-pressed={activa}
              onClick={() => enviar({ t: "familia", familia: f })}
              className={`relative h-9 shrink-0 rounded-full px-3.5 text-[13.5px] font-medium transition-colors duration-200 ${
                activa ? "text-papel" : "text-tinta-2 ring-linea hover:ring-linea-fuerte ring-1"
              }`}
            >
              {activa && (
                <motion.span
                  layoutId="chip-activo"
                  transition={resorte}
                  className="bg-tinta absolute inset-0 -z-0 rounded-full"
                />
              )}
              <span className="relative">{f ?? "Todos"}</span>
            </button>
          );
        })}
      </div>

      <div className="pantalla-scroll relative mt-2 flex-1 overflow-y-auto px-5 pb-28">
        {visibles.length === 0 ? (
          <div className="flex flex-col items-center px-4 pt-14 text-center">
            <span className="bg-papel text-gris ring-linea grid size-12 place-items-center rounded-full ring-1">
              <IconoBuscar size={20} />
            </span>
            <p className="mt-4 text-[15px] font-medium">No encontramos «{estado.busqueda.trim()}»</p>
            <p className="text-gris mt-1 text-[13px]">Probá con otra palabra, por ejemplo «yerba».</p>
            <button
              type="button"
              onClick={() => {
                enviar({ t: "buscar", texto: "" });
                enviar({ t: "familia", familia: null });
              }}
              className="ring-linea-fuerte hover:bg-papel mt-4 h-10 rounded-full px-4 text-[14px] font-medium ring-1"
            >
              Ver todo el catálogo
            </button>
          </div>
        ) : (
          <ul className="divide-linea divide-y">
            {visibles.map((p, i) => (
              <FilaProducto
                key={p.ean13}
                p={p}
                cantidad={estado.carrito[p.ean13] ?? 0}
                enviar={enviar}
                invitar={!tocado && i === 0}
              />
            ))}
          </ul>
        )}
      </div>

      <AnimatePresence>
        {items > 0 && (
          <motion.div
            initial={{ y: "120%" }}
            animate={{ y: 0 }}
            exit={{ y: "120%" }}
            transition={{ type: "spring", stiffness: 380, damping: 34 }}
            className="from-superficie via-superficie/95 to-superficie/0 absolute inset-x-0 bottom-0 z-10 bg-gradient-to-t px-4 pt-6 pb-5"
          >
            <button
              type="button"
              onClick={() => enviar({ t: "ir", pantalla: "pedido" })}
              className="bg-tinta text-papel ease-entrada flex h-14 w-full items-center justify-between rounded-2xl pr-2 pl-5 shadow-[0_1px_0_rgb(255_255_255/0.12)_inset,0_14px_30px_-14px_rgb(23_22_15/0.6)] transition-transform duration-150 active:scale-[0.98]"
            >
              <span className="text-[15px] font-semibold">Ver pedido</span>
              <span className="flex items-center gap-3">
                <span className="cifra text-papel/75 text-[14px]" aria-live="polite">
                  {items} {items === 1 ? "ítem" : "ítems"} ·{" "}
                  <span className="text-papel font-semibold">{pesos(total)}</span>
                </span>
                <span className="bg-papel/12 grid size-10 place-items-center rounded-xl">
                  <IconoAtras size={17} className="rotate-180" />
                </span>
              </span>
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

function FilaProducto({
  p,
  cantidad,
  enviar,
  invitar,
}: {
  p: Producto;
  cantidad: number;
  enviar: Dispatch<Accion>;
  invitar: boolean;
}) {
  const final = precioFinal(p);
  return (
    <li className="py-3.5">
      <p className="text-[15px] leading-snug font-medium tracking-[-0.01em]">{p.descripcion}</p>
      <p className="text-gris-suave mt-0.5 font-mono text-[11px]">
        <span className="sr-only">Código </span>
        {p.ean13} · {p.familia}
      </p>
      <div className="mt-2 flex items-center justify-between gap-3">
        <div className="flex items-baseline gap-2">
          <span className="cifra text-[16px] font-semibold tracking-[-0.01em]">{pesos(final)}</span>
          {p.descuento > 0 && (
            <>
              <span className="cifra text-gris-suave text-[12px] line-through">
                <span className="sr-only">antes </span>
                {pesos(p.p_venta)}
              </span>
              <span className="bg-sello-suave text-sello rounded-md px-1.5 py-0.5 text-[11px] font-semibold">
                −{p.descuento}%
              </span>
            </>
          )}
        </div>
        <Cantidad
          nombre={p.descripcion}
          cantidad={cantidad}
          cambiar={(c) => enviar({ t: "cantidad", ean: p.ean13, cantidad: c })}
          invitar={invitar}
        />
      </div>
    </li>
  );
}

function Cantidad({
  nombre,
  cantidad,
  cambiar,
  invitar,
}: {
  nombre: string;
  cantidad: number;
  cambiar: (c: number) => void;
  invitar: boolean;
}) {
  return (
    <div className="relative flex h-10 items-center">
      <AnimatePresence initial={false} mode="popLayout">
        {cantidad === 0 ? (
          <motion.button
            key="sumar"
            type="button"
            onClick={() => cambiar(1)}
            aria-label={`Sumar ${nombre}`}
            initial={{ opacity: 0, scale: 0.85 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.85 }}
            transition={resorte}
            whileTap={{ scale: 0.9 }}
            className="bg-tinta text-papel relative grid size-10 place-items-center rounded-full"
          >
            {invitar && (
              <span
                aria-hidden="true"
                className="ring-sello/60 absolute inset-0 rounded-full ring-2 motion-safe:animate-ping motion-safe:[animation-iteration-count:4]"
              />
            )}
            <IconoMas size={18} />
          </motion.button>
        ) : (
          <motion.div
            key="paso"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={resorte}
            className="bg-papel ring-linea-fuerte flex h-10 items-center rounded-full ring-1"
          >
            <motion.button
              type="button"
              whileTap={{ scale: 0.86 }}
              onClick={() => cambiar(cantidad - 1)}
              aria-label={cantidad === 1 ? `Quitar ${nombre}` : `Restar uno de ${nombre}`}
              className="text-tinta grid size-10 place-items-center rounded-full"
            >
              {cantidad === 1 ? <IconoBasura size={16} /> : <IconoMenos size={17} />}
            </motion.button>
            <span className="relative w-7 overflow-hidden text-center">
              <AnimatePresence initial={false} mode="popLayout">
                <motion.span
                  key={cantidad}
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -10, opacity: 0 }}
                  transition={{ duration: 0.18, ease: [0.22, 1, 0.36, 1] }}
                  className="cifra block text-[15px] font-semibold"
                  aria-live="polite"
                >
                  {cantidad}
                </motion.span>
              </AnimatePresence>
            </span>
            <motion.button
              type="button"
              whileTap={{ scale: 0.86 }}
              onClick={() => cambiar(cantidad + 1)}
              aria-label={`Sumar uno de ${nombre}`}
              className="text-tinta grid size-10 place-items-center rounded-full"
            >
              <IconoMas size={17} />
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function Encabezado({ titulo, volver }: { titulo: string; volver?: () => void }) {
  return (
    <header className="flex h-14 items-center gap-1 px-3">
      {volver && (
        <button
          type="button"
          onClick={volver}
          aria-label="Seguir comprando"
          className="text-tinta hover:bg-papel grid size-11 place-items-center rounded-full"
        >
          <IconoAtras size={19} />
        </button>
      )}
      <h3 className="text-[17px] font-semibold tracking-[-0.02em]">{titulo}</h3>
    </header>
  );
}

function MiPedido({ estado, enviar }: { estado: Estado; enviar: Dispatch<Accion> }) {
  const lineas = lineasDe(estado.carrito);
  const { total } = resumen(estado.carrito);
  const idObs = useId();

  const confirmar = () => {
    if (estado.guardando) return;
    enviar({ t: "guardando" });
    const ahora = new Date();
    const hora = `${String(ahora.getHours()).padStart(2, "0")}:${String(ahora.getMinutes()).padStart(2, "0")}`;
    window.setTimeout(() => enviar({ t: "confirmar", hora }), 700);
  };

  if (lineas.length === 0) {
    return (
      <>
        <Encabezado titulo="Mi pedido" volver={() => enviar({ t: "ir", pantalla: "catalogo" })} />
        <div className="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
          <span className="bg-papel text-gris ring-linea grid size-14 place-items-center rounded-full ring-1">
            <IconoCarrito size={22} />
          </span>
          <p className="mt-4 text-[16px] font-medium">Tu pedido está vacío</p>
          <p className="text-gris mt-1 text-[13.5px]">Volvé al catálogo y sumá lo que necesites.</p>
          <button
            type="button"
            onClick={() => enviar({ t: "ir", pantalla: "catalogo" })}
            className="bg-tinta text-papel mt-5 h-11 rounded-full px-5 text-[14px] font-medium active:scale-[0.98]"
          >
            Ver catálogo
          </button>
        </div>
      </>
    );
  }

  return (
    <>
      <Encabezado titulo="Mi pedido" volver={() => enviar({ t: "ir", pantalla: "catalogo" })} />
      <div className="pantalla-scroll flex-1 overflow-y-auto px-5 pb-36">
        <div className="bg-papel ring-linea flex gap-3 rounded-2xl p-3.5 ring-1">
          <IconoUbicacion size={18} className="text-gris mt-0.5 shrink-0" />
          <div className="min-w-0 text-[13px] leading-snug">
            <p className="font-medium">
              {CLIENTE.apellido}, {CLIENTE.nombre}
            </p>
            <p className="text-gris">{CLIENTE.direccion}</p>
          </div>
        </div>

        <ul className="divide-linea mt-3 divide-y">
          <AnimatePresence initial={false}>
            {lineas.map((l) => (
              <motion.li
                key={l.ean13}
                layout
                exit={{ opacity: 0, x: -24, transition: { duration: 0.18 } }}
                transition={resorte}
                className="flex items-center gap-3 py-3"
              >
                <div className="min-w-0 flex-1">
                  <p className="text-[14px] leading-snug font-medium">{l.descripcion}</p>
                  <p className="cifra text-gris mt-0.5 text-[12px]">
                    {l.cantidad} × {pesos(l.precio_unitario)}
                  </p>
                </div>
                <span className="cifra text-[14.5px] font-semibold">{pesos(l.subtotal)}</span>
                <button
                  type="button"
                  onClick={() => enviar({ t: "cantidad", ean: l.ean13, cantidad: 0 })}
                  aria-label={`Quitar ${l.descripcion}`}
                  className="text-gris hover:bg-papel hover:text-sello -mr-2 grid size-10 shrink-0 place-items-center rounded-full"
                >
                  <IconoBasura size={16} />
                </button>
              </motion.li>
            ))}
          </AnimatePresence>
        </ul>

        <label htmlFor={idObs} className="mt-4 block text-[13px] font-medium">
          Observaciones <span className="text-gris font-normal">(opcional)</span>
        </label>
        <textarea
          id={idObs}
          rows={2}
          placeholder="Indicaciones para la entrega"
          className="bg-papel ring-linea placeholder:text-gris-suave focus:ring-tinta/40 mt-1.5 w-full resize-none rounded-2xl px-3.5 py-2.5 text-[16px] ring-1 outline-none focus-visible:outline-none"
        />

        <button
          type="button"
          onClick={() => enviar({ t: "vaciar" })}
          className="text-gris hover:text-sello mt-3 h-10 rounded-full px-1 text-[13px] font-medium underline-offset-4 hover:underline"
        >
          Vaciar pedido
        </button>
      </div>

      <div className="border-linea bg-superficie/95 absolute inset-x-0 bottom-0 border-t px-4 pt-3 pb-5 backdrop-blur-sm">
        <div className="mb-3 flex items-baseline justify-between px-1">
          <span className="text-gris text-[13px]">Total a pagar</span>
          <span className="cifra text-[22px] font-semibold tracking-[-0.02em]" aria-live="polite">
            {pesos(total)}
          </span>
        </div>
        <button
          type="button"
          onClick={confirmar}
          aria-busy={estado.guardando}
          className="bg-tinta text-papel ease-entrada flex h-14 w-full items-center justify-center gap-2 rounded-2xl text-[15px] font-semibold shadow-[0_1px_0_rgb(255_255_255/0.12)_inset,0_14px_30px_-14px_rgb(23_22_15/0.6)] transition-transform duration-150 active:scale-[0.98]"
        >
          {estado.guardando ? (
            <>
              <span
                className="border-papel/30 border-t-papel size-4 animate-spin rounded-full border-2"
                aria-hidden="true"
              />
              Guardando pedido…
            </>
          ) : (
            "Confirmar pedido"
          )}
        </button>
      </div>
    </>
  );
}

function Exito({ estado, enviar, irAPC }: { estado: Estado; enviar: Dispatch<Accion>; irAPC: () => void }) {
  const c = estado.confirmado;
  if (!c) return null;
  return (
    <div className="flex flex-1 flex-col px-6 pt-10 pb-6">
      <div className="flex flex-1 flex-col items-center text-center">
        <motion.span
          initial={{ scale: 0.7, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: "spring", stiffness: 300, damping: 18, delay: 0.12 }}
          className="bg-listo-suave text-listo grid size-16 place-items-center rounded-full"
        >
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <motion.path
              d="m5 12.5 4.2 4L19 7"
              stroke="currentColor"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.45, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            />
          </svg>
        </motion.span>
        <p className="mt-5 text-[22px] font-semibold tracking-[-0.02em]" role="status">
          ¡Pedido enviado!
        </p>
        <p className="text-gris mt-1 text-[14px]">
          Pedido <span className="cifra text-tinta font-mono font-medium">#{c.id}</span> registrado
        </p>
        <p className="cifra mt-5 text-[30px] font-semibold tracking-[-0.03em]">{pesos(c.total)}</p>
        <p className="text-gris mt-6 max-w-[15rem] text-[13.5px] leading-relaxed">
          Si querés, mandale el detalle al negocio por WhatsApp.
        </p>
      </div>

      <div className="space-y-2.5">
        <button
          type="button"
          onClick={() => enviar({ t: "whatsapp", abierto: true })}
          className="bg-wa ease-entrada flex h-14 w-full items-center justify-center gap-2.5 rounded-2xl text-[15px] font-semibold text-white transition-transform duration-150 active:scale-[0.98]"
        >
          <IconoChat size={18} />
          Mandar por WhatsApp
        </button>
        <button
          type="button"
          onClick={irAPC}
          className="ring-linea-fuerte hover:bg-papel flex h-12 w-full items-center justify-center gap-2 rounded-2xl text-[14px] font-medium ring-1 lg:hidden"
        >
          Ver cómo llegó a la PC
          <IconoAbajo size={16} />
        </button>
        <button
          type="button"
          onClick={() => enviar({ t: "otro" })}
          className="text-tinta-2 hover:bg-papel flex h-12 w-full items-center justify-center rounded-2xl text-[14px] font-medium"
        >
          Hacer otro pedido
        </button>
      </div>
    </div>
  );
}

function FormatoWhatsApp({ texto }: { texto: string }) {
  return (
    <>
      {texto.split("\n").map((linea, i) => (
        <span key={i} className="block min-h-[1em]">
          {linea.split(/(\*[^*]+\*|_[^_]+_)/g).map((parte, j) => {
            if (/^\*[^*]+\*$/.test(parte))
              return (
                <strong key={j} className="font-semibold">
                  {parte.slice(1, -1)}
                </strong>
              );
            if (/^_[^_]+_$/.test(parte)) return <em key={j}>{parte.slice(1, -1)}</em>;
            return parte;
          })}
        </span>
      ))}
    </>
  );
}

function VistaWhatsApp({ mensaje, cerrar }: { mensaje: string; cerrar: () => void }) {
  const refCerrar = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    refCerrar.current?.focus({ preventScroll: true });
  }, []);
  return (
    <>
      <motion.div
        className="bg-tinta/35 absolute inset-0 z-30"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.25 }}
        onClick={cerrar}
        aria-hidden="true"
      />
      <motion.div
        role="dialog"
        aria-modal="false"
        aria-label="Vista previa del mensaje de WhatsApp"
        className="absolute inset-x-0 bottom-0 z-40 flex max-h-[86%] flex-col overflow-hidden rounded-t-[1.75rem] bg-[#efeae2]"
        initial={{ y: "100%" }}
        animate={{ y: 0 }}
        exit={{ y: "100%" }}
        transition={cajon}
        onKeyDown={(e) => e.key === "Escape" && cerrar()}
      >
        <div className="flex items-center gap-3 bg-[#f6f5f1] px-4 py-3">
          <span className="bg-tinta text-papel grid size-9 place-items-center rounded-full text-[13px] font-semibold">
            DS
          </span>
          <div className="min-w-0 flex-1">
            <p className="truncate text-[14.5px] font-semibold">{DISTRIBUIDORA}</p>
            <p className="text-gris text-[12px]">Vista previa del mensaje</p>
          </div>
          <button
            type="button"
            ref={refCerrar}
            onClick={cerrar}
            aria-label="Cerrar vista previa"
            className="text-gris hover:text-tinta grid size-10 place-items-center rounded-full hover:bg-black/5"
          >
            <IconoCerrar size={17} />
          </button>
        </div>
        <div className="pantalla-scroll flex-1 overflow-y-auto px-3 py-4">
          <motion.div
            initial={{ opacity: 0, y: 12, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ ...resorte, delay: 0.18 }}
            className="ml-auto w-[92%] origin-bottom-right rounded-2xl rounded-tr-md bg-[#d9fdd3] px-3 py-2.5 text-[12.5px] leading-[1.45] text-[#111b21] shadow-[0_1px_0.5px_rgb(0_0_0/0.13)]"
          >
            <FormatoWhatsApp texto={mensaje} />
            <span className="mt-1 flex items-center justify-end gap-1 text-[10.5px] text-[#667781]">
              ahora <IconoCheck size={13} className="text-[#53bdeb]" />
            </span>
          </motion.div>
        </div>
        <p className="text-gris bg-[#f6f5f1] px-5 py-3.5 text-center text-[12px] leading-snug">
          En la app real, este botón abre WhatsApp con el mensaje listo para mandar.
        </p>
      </motion.div>
    </>
  );
}
