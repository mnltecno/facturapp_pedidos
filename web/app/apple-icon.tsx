import { ImageResponse } from "next/og";

export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#17160f",
      }}
    >
      <svg width="120" height="120" viewBox="0 0 32 32">
        <path d="M10 8.5h12v15.2l-2-1.4-2 1.4-2-1.4-2 1.4-2-1.4-2 1.4z" fill="#f3f0e8" />
        <path d="M13 13h6M13 16.5h4" stroke="#17160f" strokeWidth="1.6" strokeLinecap="round" />
        <circle cx="21.5" cy="21.5" r="3.2" fill="#b23a1c" />
      </svg>
    </div>,
    size,
  );
}
