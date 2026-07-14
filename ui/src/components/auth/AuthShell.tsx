// Shared dark two-column auth shell, used by BOTH the Stack Auth handler
// (/handler/[...stack], cloud) and the local/OSS auth pages (/auth/login,
// /auth/signup). LEFT: a centered card that wraps the auth form (`children`).
// RIGHT (lg+ only): a brand/value panel with the DCXworks logo, proof points, and
// a Bland-style enterprise CTA block at the bottom (passed in as `enterpriseSlot`).
// Mobile collapses to the single card column. The form column scrolls and stays
// centered so tall (sign-up) forms never clip on short viewports. Palette is the
// app's blacks/greys with one warm CTA accent.

import { Mic } from "lucide-react";
import type { ReactNode } from "react";

import { BrandLogo } from "@/components/BrandLogo";

const HIGHLIGHTS = [
  "Speech-to-speech",
  "MCP-native",
  "BYOK - any model",
];

export function AuthShell({
  children,
  enterpriseSlot,
}: {
  children: ReactNode;
  enterpriseSlot?: ReactNode;
}) {
  return (
    <div className="grid min-h-screen w-full bg-background lg:grid-cols-[55%_45%]">
      {/* Form column (LEFT) — scrolls and stays centered so tall forms never
          clip. Carries the giant faded "DCXworks" imprint along its bottom. */}
      <main className="auth-imprint flex min-h-screen flex-col overflow-y-auto">
        <div className="flex min-h-full items-center justify-center p-6 sm:p-10">
          <div className="w-full max-w-md space-y-6 rounded-2xl border border-border/60 bg-card p-6 shadow-lg sm:p-8">
            {/* Mobile-only wordmark (brand panel is hidden) */}
            <div className="lg:hidden">
              <BrandLogo className="h-7" />
            </div>
            {children}
          </div>
        </div>
      </main>

      {/* Brand / value panel (RIGHT) — hidden on mobile. Voice-agent themed:
          layered film-grain noise + dot-grid patterns over the matte black,
          with a mic "agent" illustration ringed by pulsing sonar circles and
          a live waveform — a voice agent, listening. */}
      <aside className="relative hidden flex-col justify-between overflow-hidden border-l border-border/60 bg-zinc-950 p-10 lg:flex xl:p-14">
        {/* Backdrop layer 1: film-grain noise across the whole panel */}
        <div aria-hidden className="auth-noise pointer-events-none absolute inset-0" />
        {/* Backdrop layer 2: faint dot grid, faded out towards the edges */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0"
          style={{
            backgroundImage:
              "radial-gradient(circle, rgba(255,255,255,0.13) 1px, transparent 1px)",
            backgroundSize: "26px 26px",
            maskImage:
              "radial-gradient(ellipse 70% 55% at 50% 35%, black, transparent)",
            WebkitMaskImage:
              "radial-gradient(ellipse 70% 55% at 50% 35%, black, transparent)",
          }}
        />
        {/* Backdrop layer 3: soft radial glow behind the illustration */}
        <div
          aria-hidden
          className="pointer-events-none absolute -right-24 top-1/3 size-[28rem] rounded-full opacity-20 blur-3xl"
          style={{ background: "radial-gradient(circle, var(--cta), transparent 70%)" }}
        />

        <div className="relative">
          <BrandLogo inverse className="h-8" />
        </div>

        <div className="relative max-w-md space-y-6">
          {/* Voice-agent illustration: mic avatar + sonar rings + waveform.
              Hidden on short viewports so the enterprise CTA never clips. */}
          <div
            aria-hidden
            className="relative mx-auto hidden h-56 w-full items-center justify-center [@media(min-height:760px)]:flex"
          >
            {/* Static concentric "sound wave" circles */}
            <div className="absolute size-36 rounded-full border border-white/10" />
            <div className="absolute size-48 rounded-full border border-white/[0.07]" />
            <div className="absolute size-60 rounded-full border border-white/[0.04]" />
            {/* Pulsing sonar rings (staggered) */}
            <div className="auth-sonar absolute size-56" />
            <div className="auth-sonar absolute size-56" style={{ animationDelay: "1.2s" }} />
            <div className="auth-sonar absolute size-56" style={{ animationDelay: "2.4s" }} />
            {/* The agent: mic in a glassy circle, with a live waveform below */}
            <div className="relative flex flex-col items-center gap-5">
              <div
                className="flex size-24 items-center justify-center rounded-full border border-white/15 bg-white/[0.06] backdrop-blur"
                style={{ boxShadow: "0 0 70px -18px var(--cta)" }}
              >
                <Mic className="size-9 text-zinc-100" />
              </div>
              <div className="auth-waveform">
                {Array.from({ length: 8 }, (_, i) => (
                  <span key={i} />
                ))}
              </div>
            </div>
          </div>

          <h1 className="text-3xl font-semibold leading-tight tracking-tight text-zinc-50 xl:text-4xl">
            Voice agents that sound human, built your way.
          </h1>
          <ul className="flex flex-wrap gap-2">
            {HIGHLIGHTS.map((point) => (
              <li
                key={point}
                className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs font-medium text-zinc-300"
              >
                {point}
              </li>
            ))}
          </ul>
        </div>

        {/* Enterprise CTA block (Bland-style) — bottom margin lifts it off the
            viewport edge while justify-between keeps the column layout */}
        <div className="relative mb-12 max-w-md space-y-3 rounded-xl border border-white/10 bg-white/[0.03] p-5 xl:mb-16">
          <h2 className="text-sm font-semibold text-zinc-100">
            Need on-prem, data residency &amp; a data perimeter?
          </h2>
          <p className="text-sm text-zinc-400">
            We deploy DCXworks inside your environment for regulated and
            high-scale teams.
          </p>
          {enterpriseSlot}
        </div>
      </aside>
    </div>
  );
}
