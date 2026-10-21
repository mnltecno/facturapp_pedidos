import type { SVGProps } from "react";

type P = SVGProps<SVGSVGElement> & { size?: number };

function Base({ size = 18, children, ...rest }: P) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      {...rest}
    >
      {children}
    </svg>
  );
}

export const IconoFlecha = (p: P) => (
  <Base {...p}>
    <path d="M7 17 17 7M9 7h8v8" />
  </Base>
);

export const IconoAbajo = (p: P) => (
  <Base {...p}>
    <path d="M12 5v14M6 13l6 6 6-6" />
  </Base>
);

export const IconoChat = (p: P) => (
  <Base {...p}>
    <path d="M20 11.5a8 8 0 0 1-11.6 7.2L4 20l1.3-4.2A8 8 0 1 1 20 11.5Z" />
    <path d="M9 10.2c.3 1.8 2 3.7 4 4.2l1.2-1.1 1.7.8" />
  </Base>
);

export const IconoBuscar = (p: P) => (
  <Base {...p}>
    <circle cx="11" cy="11" r="6.5" />
    <path d="m20 20-4.2-4.2" />
  </Base>
);

export const IconoMas = (p: P) => (
  <Base {...p}>
    <path d="M12 5v14M5 12h14" />
  </Base>
);

export const IconoMenos = (p: P) => (
  <Base {...p}>
    <path d="M5 12h14" />
  </Base>
);

export const IconoBasura = (p: P) => (
  <Base {...p}>
    <path d="M5 7h14M10 7V5h4v2M7 7l.8 12h8.4L17 7" />
  </Base>
);

export const IconoCheck = (p: P) => (
  <Base {...p}>
    <path d="m5 12.5 4.2 4L19 7" />
  </Base>
);

export const IconoAtras = (p: P) => (
  <Base {...p}>
    <path d="M15 5 8 12l7 7" />
  </Base>
);

export const IconoReiniciar = (p: P) => (
  <Base {...p}>
    <path d="M4 12a8 8 0 1 0 2.4-5.7" />
    <path d="M4 4v4h4" />
  </Base>
);

export const IconoCerrar = (p: P) => (
  <Base {...p}>
    <path d="M6 6l12 12M18 6 6 18" />
  </Base>
);

export const IconoCarrito = (p: P) => (
  <Base {...p}>
    <path d="M3 4h2l2.2 10.2a1 1 0 0 0 1 .8h8.9a1 1 0 0 0 1-.8L20 8H6" />
    <circle cx="9" cy="19" r="1.2" />
    <circle cx="17" cy="19" r="1.2" />
  </Base>
);

export const IconoUbicacion = (p: P) => (
  <Base {...p}>
    <path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z" />
    <circle cx="12" cy="10" r="2.2" />
  </Base>
);

export const IconoTelefono = (p: P) => (
  <Base {...p}>
    <rect x="7" y="2.8" width="10" height="18.4" rx="2.4" />
    <path d="M11 18h2" />
  </Base>
);

export const IconoPC = (p: P) => (
  <Base {...p}>
    <rect x="3" y="4" width="18" height="12" rx="1.8" />
    <path d="M9 20h6M12 16v4" />
  </Base>
);
