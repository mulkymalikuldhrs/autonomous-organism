import { Eye, Brain, Factory, TrendingUp, Database, Shield, Bot, Zap, DollarSign, GitBranch, RefreshCw } from "lucide-react";
import { NeuralBackground } from "@/components/NeuralBackground";
import { Header } from "@/components/Header";
import { OrganismCore } from "@/components/OrganismCore";
import { OrganEngine } from "@/components/OrganEngine";
import { OrganismCard, OrganismCardHeader, OrganismCardTitle, OrganismCardContent } from "@/components/ui/organism-card";
import { MetricDisplay } from "@/components/ui/metric-display";
import { ActivityLog } from "@/components/ui/activity-log";
import { Progress } from "@/components/ui/progress";
import { useOrganismReal, AgentStatus } from "@/hooks/useOrganismReal";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function Index() {
  const { toast } = useToast();
  const {
    state,
    logs,
    agents,
    runSense,
    runDecision,
    runFactory,
    runGrowth,
    runMonetization,
    runSpawner,
    runEvolution
  } = useOrganismReal();

  const logEntries = logs.map((l: any) => ({
    id: l.id,
    timestamp: new Date(l.created_at),
    type: l.level,
    source: l.source,
    message: l.message,
  }));

  const onRunEngine = async (name: string, fn: () => Promise<void>) => {
    try {
      await fn();
      toast({ title: `${name} Started`, description: `${name} process triggered in background.` });
    } catch (e: any) {
      toast({ title: `${name} Failed`, description: e?.message ?? "Error", variant: "destructive" });
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
                    <Progress value={87} className="mt-2 h-2" />
                    <span className="text-xs text-success mt-1 block">87% Optimal</span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <Button onClick={() => onRunEngine("Sense", runSense)} size="sm" variant="outline">Sense</Button>
                    <Button onClick={() => onRunEngine("Decision", runDecision)} size="sm" variant="outline">Decision</Button>
                    <Button onClick={() => onRunEngine("Factory", runFactory)} size="sm" variant="outline">Factory</Button>
                    <Button onClick={() => onRunEngine("Spawner", runSpawner)} size="sm" variant="outline">Spawner</Button>
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
                    trendValue="tracked"
                  />
                  <MetricDisplay 
                    label="Active Agents" 
                     value={agents.filter(a => a.status === 'active').length}
                    variant="success"
                    size="sm"
                  />
                  <MetricDisplay 
                    label="Terminated" 
                     value={agents.filter(a => a.status === 'terminated').length}
                    variant="destructive"
                    size="sm"
                  />
                  <div className="pt-2">
                    <span className="text-xs text-muted-foreground uppercase tracking-wider">Efficiency</span>
                    <Progress value={92} className="mt-2 h-2" />
                    <span className="text-xs text-primary mt-1 block">92% Optimal</span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <Button onClick={() => onRunEngine("Growth", runGrowth)} size="sm" variant="accent">Growth</Button>
                    <Button onClick={() => onRunEngine("Monetization", runMonetization)} size="sm" variant="accent">Monetize</Button>
                    <Button onClick={() => onRunEngine("Evolution", runEvolution)} size="sm" variant="accent">Evolve</Button>
                    <Button size="sm" variant="ghost" disabled>Immune</Button>
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
                status="online"
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
                status="online"
                description="Marketing, content generation, and user acquisition."
                metrics={[
                  { label: "Stages", value: 3 },
                  { label: "Channels", value: 3 },
                ]}
              />
              <OrganEngine
                name="Monetization"
                icon={DollarSign}
                variant="accent"
                status="online"
                description="Handling revenue streams, subscriptions and sales simulation."
                metrics={[
                  { label: "Revenue", value: "Active" },
                  { label: "Strategy", value: "Multi-Model" },
                ]}
              />
              <OrganEngine
                name="Agent Spawner"
                icon={GitBranch}
                variant="intelligence"
                status="online"
                description="Generating specialized sub-agents to handle complex tasks."
                metrics={[
                  { label: "Active", value: agents.filter(a => a.status === 'active').length },
                  { label: "Framework", value: "Autonomous" },
                ]}
              />
              <OrganEngine
                name="Evolution Engine"
                icon={RefreshCw}
                variant="primary"
                status="online"
                description="Self-optimizing scoring weights based on performance data."
                metrics={[
                  { label: "Learning", value: "On" },
                  { label: "Feedback", value: "Loop" },
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
                  {agents.length > 0 ? (
                    agents.map((agent) => (
                      <div key={agent.id} className="flex justify-between items-center border-b pb-2">
                        <div className="flex flex-col">
                          <span className="font-medium text-sm">{agent.name}</span>
                          <span className="text-[10px] text-muted-foreground uppercase">{agent.type} Agent</span>
                        </div>
                        <span className={cn(
                          "text-xs px-2 py-1 rounded",
                          agent.status === 'active' ? "bg-success/20 text-success" : "bg-destructive/20 text-destructive"
                        )}>
                          {agent.personality}
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-muted-foreground italic">No agents active. Trigger Spawner.</p>
                  )}
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
            <p className="text-xs text-muted-foreground font-mono">
              ORGANISM-ALPHA • GEN-0004 • Open Source • Autonomous Life System
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
