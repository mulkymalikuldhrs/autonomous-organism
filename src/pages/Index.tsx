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
          organismName="ORGANISM-ALPHA"
          generation={state?.generation ?? 1}
          status="online"
        />

        <main className="container mx-auto px-4 py-8">
          <section className="mb-12">
            <div className="grid lg:grid-cols-3 gap-8 items-center">
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
                    <Progress value={94} className="mt-2 h-2" />
                    <span className="text-xs text-success mt-1 block">94% Optimal</span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <Button onClick={onRunSense} size="sm">Sense</Button>
                    <Button onClick={onRunDecision} variant="secondary" size="sm">Decision</Button>
                    <Button onClick={onRunFactory} variant="outline" size="sm">Factory</Button>
                    <Button onClick={onRunGrowth} variant="ghost" size="sm">Growth</Button>
                  </div>
                </OrganismCardContent>
              </OrganismCard>

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
                    trendValue="live"
                  />
                  <MetricDisplay 
                    label="Active Agents" 
                     value={4}
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
                  { label: "Sources", value: 7, trend: "up", trendValue: "Gen-4" },
                  { label: "Method", value: "Playwright" },
                ]}
              />
              <OrganEngine
                name="Decision Core"
                icon={Brain}
                variant="decision"
                status="online"
                description="Analyzing and scoring problems by automation potential and revenue."
                metrics={[
                  { label: "Weighting", value: "Weighted" },
                  { label: "Analysis", value: "LLM-Deep" },
                ]}
              />
              <OrganEngine
                name="SaaS Factory"
                icon={Factory}
                variant="factory"
                status="online"
                description="Building and deploying MVP solutions automatically."
                metrics={[
                  { label: "Outputs", value: "Docker" },
                  { label: "Stack", value: "Full-Stack" },
                ]}
              />
              <OrganEngine
                name="Growth Engine"
                icon={TrendingUp}
                variant="growth"
                status="idle"
                description="Marketing, content generation, and user acquisition."
                metrics={[
                  { label: "Stages", value: 3 },
                  { label: "Channels", value: 3 },
                ]}
              />
              <OrganEngine
                name="Memory Engine"
                icon={Database}
                variant="memory"
                status="online"
                description="Recording patterns, failures, and evolution data."
                metrics={[
                  { label: "Status", value: "Active" },
                  { label: "Learning", value: "Revenue-based" },
                ]}
              />
              <OrganEngine
                name="Immune System"
                icon={Shield}
                variant="danger"
                status="online"
                description="Preventing runaway processes and protecting resources."
                metrics={[
                  { label: "Disk Check", value: "Active" },
                  { label: "Integrity", value: "Verified" },
                ]}
              />
            </div>
          </section>

          <section className="grid lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Bot className="w-5 h-5 text-intelligence" />
                Agents Status
              </h3>
              <OrganismCard variant="default" size="lg" className="p-6">
                <div className="space-y-4">
                   <div className="flex justify-between items-center border-b pb-2">
                      <span className="font-medium text-sm">Builder Agent</span>
                      <span className="text-xs bg-success/20 text-success px-2 py-1 rounded">Efficient</span>
                   </div>
                   <div className="flex justify-between items-center border-b pb-2">
                      <span className="font-medium text-sm">Growth Agent</span>
                      <span className="text-xs bg-primary/20 text-primary px-2 py-1 rounded">Creative</span>
                   </div>
                   <div className="flex justify-between items-center border-b pb-2">
                      <span className="font-medium text-sm">Sense Agent</span>
                      <span className="text-xs bg-intelligence/20 text-intelligence px-2 py-1 rounded">Persistent</span>
                   </div>
                </div>
              </OrganismCard>
            </div>

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

          <footer className="mt-16 pt-8 border-t border-border/30 text-center">
            <p className="text-xs text-muted-foreground font-mono uppercase tracking-[0.2em]">
              ORGANISM-ALPHA GEN-4.1 • PRODUCTION READY • AUTONOMOUS LIFE SYSTEM
            </p>
            <p className="text-[10px] text-muted-foreground/50 mt-2 italic">
              "Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
            </p>
          </footer>
        </main>
      </div>
    </div>
  );
}
