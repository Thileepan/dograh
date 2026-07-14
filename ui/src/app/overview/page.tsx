"use client";

import {
    AudioLines,
    Brain,
    FileText,
    Megaphone,
    Mic,
    Phone,
    Workflow,
    Wrench,
} from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const CAPABILITIES = [
    {
        icon: Workflow,
        title: "Visual workflow builder",
        description:
            "Design conversation flows on a drag-and-drop canvas — prompts, branching, and tools on every node.",
    },
    {
        icon: Brain,
        title: "Any model, your keys",
        description:
            "Mix and match LLM, speech-to-text, and text-to-speech providers, or run realtime speech-to-speech models.",
    },
    {
        icon: Phone,
        title: "Telephony & WebRTC",
        description:
            "Take and place real phone calls through your telephony provider, or talk to agents right in the browser.",
    },
    {
        icon: Megaphone,
        title: "Outbound campaigns",
        description:
            "Upload contact lists and run scheduled outbound calling campaigns at scale.",
    },
    {
        icon: Wrench,
        title: "Tools & MCP",
        description:
            "Let agents call HTTP APIs and MCP servers to fetch data and take actions mid-call.",
    },
    {
        icon: FileText,
        title: "QA & analytics",
        description:
            "Review transcripts and recordings, score calls, and trace every step of an agent run.",
    },
    {
        icon: AudioLines,
        title: "Natural voice",
        description:
            "Pick from a wide catalog of voices and languages, with barge-in and low-latency responses.",
    },
    {
        icon: Mic,
        title: "Test as you build",
        description:
            "Talk to your agent from the editor at any point — iterate on prompts and hear the result instantly.",
    },
];

export default function OverviewPage() {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="max-w-5xl mx-auto space-y-10">
                {/* Hero: headline + CTAs, with a voice-agent motif on the right */}
                <div className="relative overflow-hidden rounded-2xl border border-border/60 bg-card px-8 py-10 sm:px-12">
                    <div className="relative z-10 max-w-xl space-y-5">
                        <h1 className="text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">
                            Build voice agents, your way.
                        </h1>
                        <p className="text-muted-foreground leading-7">
                            Describe your agent with prompts, shape the conversation on a
                            visual canvas, and launch it over the phone or the web — with
                            full control over every model in the pipeline.
                        </p>
                        <div className="flex flex-wrap gap-3">
                            <Button asChild size="lg">
                                <Link href="/workflow">Create an agent</Link>
                            </Button>
                            <Button asChild variant="outline" size="lg">
                                <Link href="/model-configurations">Configure models</Link>
                            </Button>
                        </div>
                    </div>

                    {/* Voice-agent illustration: mic avatar, sonar rings, waveform */}
                    <div
                        aria-hidden
                        className="pointer-events-none absolute inset-y-0 right-0 hidden w-1/2 items-center justify-center lg:flex"
                    >
                        <div className="absolute size-40 rounded-full border border-foreground/10" />
                        <div className="absolute size-56 rounded-full border border-foreground/[0.07]" />
                        <div className="absolute size-72 rounded-full border border-foreground/[0.04]" />
                        <div className="auth-sonar absolute size-52" />
                        <div className="auth-sonar absolute size-52" style={{ animationDelay: "1.8s" }} />
                        <div className="relative flex flex-col items-center gap-4">
                            <div
                                className="flex size-20 items-center justify-center rounded-full border border-border bg-background"
                                style={{ boxShadow: "0 0 60px -18px var(--cta)" }}
                            >
                                <Mic className="size-8 text-foreground" />
                            </div>
                            <div className="auth-waveform">
                                {Array.from({ length: 8 }, (_, i) => (
                                    <span key={i} />
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Platform capabilities */}
                <div>
                    <h2 className="mb-4 text-lg font-semibold">
                        Everything you need to ship a voice agent
                    </h2>
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                        {CAPABILITIES.map(({ icon: Icon, title, description }) => (
                            <Card key={title} className="border-border/60">
                                <CardContent className="space-y-2 pt-6">
                                    <div className="flex size-9 items-center justify-center rounded-lg bg-cta/15">
                                        <Icon className="size-4.5 text-cta" />
                                    </div>
                                    <p className="font-medium">{title}</p>
                                    <p className="text-sm leading-6 text-muted-foreground">
                                        {description}
                                    </p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
