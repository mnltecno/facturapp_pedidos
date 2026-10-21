"use client";

import { useEffect } from "react";
import { registrarLlegada, tokenVisitante } from "@/lib/contacto-navegador";

export function Llegada() {
  useEffect(() => {
    registrarLlegada();
    tokenVisitante();
  }, []);
  return null;
}
