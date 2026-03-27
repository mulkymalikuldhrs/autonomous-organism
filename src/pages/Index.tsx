import { Eye, Brain, Factory, TrendingUp, Database, Shield, Bot, Zap, DollarSign, Users } from "lucide-react";
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
  const {
    state,
    logs,
    agents,
    runSense,
    runDecision,
    runFactory,
    runGrowth,
    runSpawner,
    runMonetization
  } = useOrganismReal();

  const logEntries = logs.map((l: any) => ({
    id: l.id,
    timestamp: new Date(l.created_at),
    type: l.level,
    source: l.source,
    message: l.message,
  }));

  const handleAction = async (action: () => Promise<void>, name: string) => {
    try {
      await action();
      toast({ title: name, description: `${name} started in background.` });
    } catch (e: any) {
      toast({ title: `${name} gagal`, description: e?.message ?? "Error", variant: "destructive" });
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

                  <div className="grid grid-cols-2 gap-2 pt-2">
                    <Button onClick={() => handleAction(runSense, "Sense")} size="xs" className="text-[10px] h-7">Sense</Button>
                    <Button onClick={() => handleAction(runDecision, "Decision")} variant="secondary" size="xs" className="text-[10px] h-7">Decision</Button>
                    <Button onClick={() => handleAction(runFactory, "Factory")} variant="outline" size="xs" className="text-[10px] h-7">Factory</Button>
                    <Button onClick={() => handleAction(runGrowth, "Growth")} variant="ghost" size="xs" className="text-[10px] h-7">Growth</Button>
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
                     value={state?.activeAgents ?? 0}
                    variant="success"
                    size="sm"
                  />
                  <MetricDisplay 
                    label="Terminated" 
                     value={0} 
                    variant="destructive"
                    size="sm"
                  />
                  <div className="pt-2 space-y-3">
                    <div className="flex gap-2">
                      <Button onClick={() => handleAction(runSpawner, "Spawner")} variant="secondary" size="sm" className="w-full text-xs h-8">
                        <Users className="w-3 h-3 mr-1" /> Spawn
                      </Button>
                      <Button onClick={() => handleAction(runMonetization, "Monetization")} variant="accent" size="sm" className="w-full text-xs h-8">
                        <DollarSign className="w-3 h-3 mr-1" /> Monetize
                      </Button>
                    </div>
                    <div>
                      <span className="text-xs text-muted-foreground uppercase tracking-wider">Efficiency</span>
                      <Progress value={92} className="mt-2 h-2" />
                      <span className="text-xs text-primary mt-1 block">92% Optimal</span>
                    </div>
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
                Autonomous Agents
              </h3>
              <OrganismCard variant="default" size="lg" className="p-6">
                <div className="space-y-4 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                  {agents.length > 0 ? (
                    agents.map((agent: any) => (
                      <div key={agent.id} className="flex justify-between items-center border-b pb-2">
                        <div className="flex flex-col">
                          <span className="font-medium text-sm">{agent.type} Agent</span>
                          <span className="text-[10px] text-muted-foreground uppercase">Personality: {agent.personality}</span>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded ${
                          agent.status === 'active' ? 'bg-success/20 text-success' : 'bg-muted text-muted-foreground'
                        }`}>
                          {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                        </span>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground text-sm italic">
                      No active agents spawned. Click 'Spawn' to initialize.
                    </div>
                  )}
                </div>
              </OrganismCard>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
                System Activity
              </h3>
              <OrganismCard variant="default" size="lg" className="h-[348px]">
                <ActivityLog entries={logEntries} maxHeight="310px" />
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
