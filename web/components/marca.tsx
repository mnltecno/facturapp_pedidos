export function Marca({ className = "" }: { className?: string }) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true">
        <rect width="32" height="32" rx="9" fill="var(--tinta)" />
        <path d="M10 8.5h12v15.2l-2-1.4-2 1.4-2-1.4-2 1.4-2-1.4-2 1.4z" fill="var(--papel)" />
        <path d="M13 13h6M13 16.5h4" stroke="var(--tinta)" strokeWidth="1.6" strokeLinecap="round" />
        <circle cx="21.5" cy="21.5" r="3.2" fill="var(--sello)" />
      </svg>
      <span className="text-[17px] font-semibold tracking-[-0.03em]">FacturApp</span>
    </span>
  );
}
