import { Eye, Brain, Factory, TrendingUp, Database, Shield, Bot, Zap } from "lucide-react";
import { NeuralBackground } from "@/components/NeuralBackground";
import { Header } from "@/components/Header";
import { OrganismCore } from "@/components/OrganismCore";
import { OrganEngine } from "@/components/OrganEngine";
import { OrganismCard, OrganismCardHeader, OrganismCardTitle, OrganismCardContent } from "@/components/ui/organism-card";
import { MetricDisplay } from "@/components/ui/metric-display";
import { ActivityLog } from "@/components/ui/activity-log";
import { Progress } from "@/components/ui/progress";
import { useOrganismReal } from "@/hooks/useOrganismReal";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";

export default function Index() {
  const { toast } = useToast();
  const { state, logs, runSense, runDecision, runFactory, runGrowth } = useOrganismReal();

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
      toast({ title: "Sense Engine", description: "Sense engine started in background." });
    } catch (e: any) {
      toast({ title: "Sense gagal", description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  const onRunDecision = async () => {
    try {
      await runDecision();
      toast({ title: "Decision Core", description: "Decision core started in background." });
    } catch (e: any) {
      toast({ title: "Decision gagal", description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  const onRunFactory = async () => {
    try {
      await runFactory();
      toast({ title: "SaaS Factory", description: "SaaS Factory started in background." });
    } catch (e: any) {
      toast({ title: "Factory gagal", description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  const onRunGrowth = async () => {
    try {
      await runGrowth();
      toast({ title: "Growth Engine", description: "Growth engine started in background." });
    } catch (e: any) {
      toast({ title: "Growth gagal", description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      <NeuralBackground />

      <div className="relative z-10">
        <Header
          organismName="ORGANISME-SAAS-OTONOM"
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
                  value={state?.productsBuilt ?? 0}
                  variant="accent"
                  size="sm"
                />
                <div className="pt-2">
                  <span className="text-xs text-muted-foreground uppercase tracking-wider">System Health</span>
                  <Progress value={87} className="mt-2 h-2" />
                  <span className="text-xs text-success mt-1 block">87% Optimal (Gen-3)</span>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2">
                  <Button onClick={onRunSense} size="sm">Sense</Button>
                  <Button onClick={onRunDecision} variant="secondary" size="sm">Decision</Button>
                  <Button onClick={onRunFactory} variant="outline" size="sm">Factory</Button>
                  <Button onClick={onRunGrowth} variant="ghost" size="sm">Growth</Button>
                </div>
              </OrganismCardContent>
            </OrganismCard>

            {/* Center - Core Visualization */}
            <div className="flex flex-col items-center justify-center py-8 lg:col-span-1">
              <OrganismCore status="alive" className="mb-16" />
              <div className="text-center mt-8">
                <h2 className="text-2xl font-bold gradient-text-primary mb-2 uppercase">
                  Autonomous SaaS Organism
                </h2>
                <p className="text-sm text-muted-foreground max-w-md">
                  A self-evolving digital species discovering problems, building MVPs,
                  and scaling independently using local AI and automation.
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
                  trendValue="USD"
                />
                <MetricDisplay
                  label="Active Agents"
                   value={0}
                  variant="success"
                  size="sm"
                />
                <MetricDisplay
                  label="Evolution Score"
                   value={92}
                  variant="intelligence"
                  size="sm"
                />
                <div className="pt-2">
                  <span className="text-xs text-muted-foreground uppercase tracking-wider">Market Efficiency</span>
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
              status="online"
              description="Scanning HN, Reddit RSS and forums for human pain points."
              metrics={[
                { label: "Sources", value: 5, trend: "up", trendValue: "Real" },
                { label: "Mode", value: "Scrape" },
              ]}
            />
            <OrganEngine
              name="Decision Core"
              icon={Brain}
              variant="decision"
              status="online"
              description="Clustering problems and scoring by automation potential."
              metrics={[
                { label: "Clustering", value: "K-Means" },
                { label: "Accuracy", value: "High" },
              ]}
            />
            <OrganEngine
              name="SaaS Factory"
              icon={Factory}
              variant="factory"
              status="online"
              description="Generating FastAPI + HTML boilerplates automatically."
              metrics={[
                { label: "Output", value: "/products" },
                { label: "Type", value: "FullStack" },
              ]}
            />
            <OrganEngine
              name="Growth Engine"
              icon={TrendingUp}
              variant="growth"
              status="online"
              description="Marketing copy generation and distribution planning."
              metrics={[
                { label: "Outbox", value: "Ready" },
                { label: "Channels", value: 4 },
              ]}
            />
            <OrganEngine
              name="Memory Engine"
              icon={Database}
              variant="memory"
              status="online"
              description="SQL-based pattern recording and evolution data."
              metrics={[
                { label: "DB", value: "SQLite" },
                { label: "Persistence", value: "Local" },
              ]}
            />
            <OrganEngine
              name="Immune System"
              icon={Shield}
              variant="danger"
              status="online"
              description="Monitoring error rates and protecting resources."
              metrics={[
                { label: "Status", value: "Healthy" },
                { label: "Isolation", value: "Off" },
              ]}
            />
          </div>
        </section>

        {/* Agents & Logs Section */}
        <section className="grid lg:grid-cols-2 gap-8">
          {/* Agent Spawner */}
          <div>
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
              <Bot className="w-5 h-5 text-intelligence" />
              Agent Spawner (Gen-3)
            </h3>
            <OrganismCard variant="default" size="lg" className="p-6">
              <p className="text-sm text-muted-foreground mb-4">
                Creating specialized sub-agents for each product.
              </p>
              <div className="flex gap-2">
                <Button variant="outline" className="w-full">View Active Agents</Button>
                <Button variant="outline" className="w-full">Spawn New Agent</Button>
              </div>
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
            ORGANISME-SAAS-OTONOM • GEN-0003 • Open Source • Autonomous Life System
          </p>
          <p className="text-[10px] text-muted-foreground/50 mt-2">
            "Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
          </p>
        </footer>
        </main>
      </div>
    </div>
  );
}
