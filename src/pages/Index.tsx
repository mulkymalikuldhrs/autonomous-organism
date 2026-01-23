import { Eye, Brain, Factory, TrendingUp, Database, Shield, Bot, Zap } from "lucide-react";
import { NeuralBackground } from "@/components/NeuralBackground";
import { Header } from "@/components/Header";
import { OrganismCore } from "@/components/OrganismCore";
import { OrganEngine } from "@/components/OrganEngine";
import { OrganismCard, OrganismCardHeader, OrganismCardTitle, OrganismCardContent } from "@/components/ui/organism-card";
import { MetricDisplay } from "@/components/ui/metric-display";
import { ActivityLog } from "@/components/ui/activity-log";
import { Progress } from "@/components/ui/progress";
import { AuthGate } from "@/components/AuthGate";
import { useOrganismReal } from "@/hooks/useOrganismReal";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { usePuterAi } from "@/hooks/usePuterAi";
import { supabase } from "@/integrations/supabase/client";

export default function Index() {
  const { toast } = useToast();
  const puter = usePuterAi();
  const { state, logs, runSense, runDecision } = useOrganismReal();

  const logEntries = logs.map((l: any) => ({
    id: l.id,
    timestamp: new Date(l.created_at),
    type: l.level,
    source: l.source,
    message: l.message,
  }));

  const onRunSense = async () => {
    try {
      await runSense();
      toast({ title: "Sense Engine", description: "Ingest selesai dijalankan." });
    } catch (e: any) {
      toast({ title: "Sense gagal", description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  const onRunDecision = async () => {
    try {
      if (!puter.ready) throw new Error(puter.error ?? "Puter belum siap");

      const { data: cleanRows, error } = await supabase
        .from("problem_clean")
        .select("text_clean")
        .order("created_at", { ascending: false })
        .limit(25);
      if (error) throw error;

      const corpus = (cleanRows ?? []).map((r) => r.text_clean).join("\n\n---\n\n").slice(0, 12000);
      if (!corpus.trim()) throw new Error("Belum ada data problem_clean. Jalankan Sense dulu.");

      const prompt =
        "Kamu adalah Decision Core untuk organisme SaaS. Dari kumpulan keluhan berikut, pilih 1 tema masalah terbaik untuk dibangun sebagai MVP.\n" +
        "Berikan output 3 baris saja, format persis:\n" +
        "THEME: <tema>\n" +
        "SCORE: <0-100>\n" +
        "SUMMARY: <ringkas 1-2 kalimat>\n\n" +
        "DATA:\n" +
        corpus;

      const text = await puter.chat(prompt, { model: "gpt-5-nano" });
      const theme = (text.match(/THEME:\s*(.+)/i)?.[1] ?? "").trim();
      const scoreRaw = (text.match(/SCORE:\s*(\d{1,3})/i)?.[1] ?? "50").trim();
      const summary = (text.match(/SUMMARY:\s*(.+)/i)?.[1] ?? "").trim();
      const score = Math.max(0, Math.min(100, Number(scoreRaw) || 50));
      if (!theme) throw new Error("Output model tidak valid. Coba ulangi.");

      await runDecision({ theme, score, summary, evidence: { model: "gpt-5-nano", raw: text } });
      toast({ title: "Decision Core", description: `Top idea: ${theme} (${score})` });
    } catch (e: any) {
      toast({ title: "Decision gagal", description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  return (
    <AuthGate>
      <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
        <NeuralBackground />
        
        <div className="relative z-10">
          <Header 
            organismName="ORGANISM-ALPHA" 
            generation={state?.generation ?? 1} 
            status="online" 
          />

          <main className="container mx-auto px-4 py-8">
          {/* Hero Section - Core Status */}
          <section className="mb-12">
            <div className="grid lg:grid-cols-3 gap-8 items-center">
              {/* Left Metrics */}
              <OrganismCard variant="default" size="lg" className="lg:col-span-1">
                <OrganismCardHeader>
                  <Zap className="w-5 h-5 text-primary" />
                  <OrganismCardTitle>Vital Signs</OrganismCardTitle>
                </OrganismCardHeader>
                <OrganismCardContent className="space-y-6">
                  <MetricDisplay 
                    label="Problems Scanned" 
                    value={(state?.problemsScanned ?? 0).toLocaleString()} 
                    variant="primary"
                    trend="up"
                    trendValue="real-time"
                  />
                  <MetricDisplay 
                    label="Ideas Generated" 
                    value={state?.ideasGenerated ?? 0} 
                    variant="default"
                    trend="up"
                    trendValue="from DB"
                  />
                  <MetricDisplay 
                    label="Products Built" 
                    value={0} 
                    variant="accent"
                    size="sm"
                  />
                  <div className="pt-2">
                    <span className="text-xs text-muted-foreground uppercase tracking-wider">System Health</span>
                    <Progress value={87} className="mt-2 h-2" />
                    <span className="text-xs text-success mt-1 block">87% Optimal</span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <Button onClick={onRunSense}>
                      Run Sense
                    </Button>
                    <Button onClick={onRunDecision} variant="secondary" disabled={!puter.ready}>
                      Run Decision
                    </Button>
                  </div>
                  {!puter.ready && (
                    <p className="text-xs text-muted-foreground">
                      Memuat Puter.js… {puter.error ? `(${puter.error})` : ""}
                    </p>
                  )}
                </OrganismCardContent>
              </OrganismCard>

              {/* Center - Core Visualization */}
              <div className="flex flex-col items-center justify-center py-8 lg:col-span-1">
                <OrganismCore status="alive" className="mb-16" />
                <div className="text-center mt-8">
                  <h2 className="text-2xl font-bold gradient-text-primary mb-2">
                    Autonomous Life System
                  </h2>
                  <p className="text-sm text-muted-foreground max-w-md">
                    Self-evolving organism discovering problems, building solutions, 
                    and generating revenue without human intervention.
                  </p>
                </div>
              </div>

              {/* Right Metrics */}
              <OrganismCard variant="factory" size="lg" className="lg:col-span-1">
                <OrganismCardHeader>
                  <TrendingUp className="w-5 h-5 text-accent" />
                  <OrganismCardTitle className="text-accent">Revenue Engine</OrganismCardTitle>
                </OrganismCardHeader>
                <OrganismCardContent className="space-y-6">
                  <MetricDisplay 
                    label="Total Revenue" 
                    value={`$${(state?.revenue ?? 0).toFixed(2)}`} 
                    variant="accent"
                    trend="up"
                    trendValue="tracked later"
                  />
                  <MetricDisplay 
                    label="Active Agents" 
                     value={0} 
                    variant="success"
                    size="sm"
                  />
                  <MetricDisplay 
                    label="Terminated" 
                     value={0} 
                    variant="destructive"
                    size="sm"
                  />
                  <div className="pt-2">
                    <span className="text-xs text-muted-foreground uppercase tracking-wider">Efficiency</span>
                    <Progress value={92} className="mt-2 h-2" />
                    <span className="text-xs text-primary mt-1 block">92% Optimal</span>
                  </div>
                </OrganismCardContent>
              </OrganismCard>
            </div>
          </section>

          {/* Organ Engines Grid */}
          <section className="mb-12">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              Organ Engines
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              <OrganEngine
                name="Sense Engine"
                icon={Eye}
                variant="sense"
                status="processing"
                description="Scanning the digital world for human problems and pain points."
                metrics={[
                  { label: "Sources", value: 12, trend: "up", trendValue: "+2" },
                  { label: "Queue", value: 847 },
                ]}
              />
              <OrganEngine
                name="Decision Core"
                icon={Brain}
                variant="decision"
                status="online"
                description="Analyzing and scoring problems by automation potential and revenue."
                metrics={[
                  { label: "Candidates", value: 23 },
                  { label: "Accuracy", value: "94%" },
                ]}
              />
              <OrganEngine
                name="SaaS Factory"
                icon={Factory}
                variant="factory"
                status="online"
                description="Building and deploying MVP solutions automatically."
                metrics={[
                  { label: "In Build", value: 1 },
                  { label: "Deployed", value: 3 },
                ]}
              />
              <OrganEngine
                name="Growth Engine"
                icon={TrendingUp}
                variant="growth"
                status="idle"
                description="Marketing, content generation, and user acquisition."
                metrics={[
                  { label: "Reach", value: "12.4K" },
                  { label: "Conv Rate", value: "2.3%" },
                ]}
              />
              <OrganEngine
                name="Memory Engine"
                icon={Database}
                variant="memory"
                status="online"
                description="Recording patterns, failures, and evolution data."
                metrics={[
                  { label: "Records", value: "4.2K" },
                  { label: "Patterns", value: 87 },
                ]}
              />
              <OrganEngine
                name="Immune System"
                icon={Shield}
                variant="danger"
                status="online"
                description="Preventing runaway processes and protecting resources."
                metrics={[
                  { label: "Blocked", value: 14 },
                  { label: "Health", value: "98%" },
                ]}
              />
            </div>
          </section>

          {/* Agents & Logs Section */}
          <section className="grid lg:grid-cols-2 gap-8">
            {/* Agent Spawner (real backend not yet wired) */}
            <div>
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Bot className="w-5 h-5 text-intelligence" />
                Agents
              </h3>
              <OrganismCard variant="default" size="lg" className="p-6">
                <p className="text-sm text-muted-foreground">
                  Modul agent runtime (spawn/kill + telemetry) akan dibuat setelah pipeline Sense→Decision stabil.
                </p>
              </OrganismCard>
            </div>

            {/* Activity Log */}
            <div>
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
                Activity Log
              </h3>
              <OrganismCard variant="default" size="lg" className="h-[400px]">
                <ActivityLog entries={logEntries} maxHeight="360px" />
              </OrganismCard>
            </div>
          </section>

          {/* Footer */}
          <footer className="mt-16 pt-8 border-t border-border/30 text-center">
            <p className="text-xs text-muted-foreground font-mono">
              ORGANISM-ALPHA • GEN-0001 • Open Source • Autonomous Life System
            </p>
            <p className="text-[10px] text-muted-foreground/50 mt-2">
              "Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
            </p>
          </footer>
          </main>
        </div>
      </div>
    </AuthGate>
  );
}
