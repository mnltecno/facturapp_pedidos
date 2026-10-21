"use client";

import { useEffect, useRef, useState, type ElementType, type ReactNode } from "react";

export function Reveal({
  children,
  as: Tag = "div",
  retraso = 0,
  className,
  id,
}: {
  children: ReactNode;
  as?: ElementType;
  retraso?: number;
  className?: string;
  id?: string;
}) {
  const ref = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setVisible(true);
          io.disconnect();
        }
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.08 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <Tag
      ref={ref}
      id={id}
      data-reveal=""
      data-visible={visible ? "true" : "false"}
      style={{ "--retraso": `${retraso}ms` } as React.CSSProperties}
      className={className}
    >
      {children}
    </Tag>
  );
}

export function useEnPantalla<T extends HTMLElement>(margen = "0px") {
  const ref = useRef<T>(null);
  const [en, setEn] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(([e]) => setEn(e.isIntersecting), { rootMargin: margen });
    io.observe(el);
    return () => io.disconnect();
  }, [margen]);
  return [ref, en] as const;
}
