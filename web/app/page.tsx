import { FlotanteWhatsApp } from "@/components/flotante-whatsapp";
import { AntesAhora, Cierre, ComoLlega, Encabezado, Hero, Pie, Precio, SeccionDemo } from "@/components/secciones";

export default function Inicio() {
  return (
    <>
      <a
        href="#demo"
        className="focus:bg-tinta focus:text-papel sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:rounded-full focus:px-4 focus:py-2"
      >
        Ir a la demo
      </a>
      <Encabezado />
      <main>
        <Hero />
        <AntesAhora />
        <SeccionDemo />
        <ComoLlega />
        <Precio />
        <Cierre />
      </main>
      <Pie />
      <FlotanteWhatsApp />
    </>
  );
}
