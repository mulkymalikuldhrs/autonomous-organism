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
import { Badge } from "@/components/ui/badge";

export default function Index() {
  const { toast } = useToast();
  const { state, logs, agents, runSense, runDecision, runFactory, runGrowth, runMonetization, runSpawner } = useOrganismReal();

  const logEntries = logs.map((l: any) => ({
    id: l.id,
    timestamp: new Date(l.created_at),
    type: l.level,
    source: l.source,
    message: l.message,
  }));

  const handleAction = async (name: string, action: () => Promise<void>) => {
    try {
      await action();
      toast({ title: name, description: "Action triggered successfully." });
    } catch (e: any) {
      toast({ title: `${name} failed`, description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      <NeuralBackground />

      <div className="relative z-10">
        <Header
          organismName="ORGANISM-ALPHA"
          generation={state?.generation ?? 4}
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
                  <Progress value={95} className="mt-2 h-2" />
                  <span className="text-xs text-success mt-1 block">95% Optimal</span>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2">
                  <Button onClick={() => handleAction("Sense Engine", runSense)}>
                    Run Sense
                  </Button>
                  <Button onClick={() => handleAction("Decision Core", runDecision)} variant="secondary">
                    Run Decision
                  </Button>
                </div>
              </OrganismCardContent>
            </OrganismCard>

            {/* Center - Core Visualization */}
            <div className="flex flex-col items-center justify-center py-8 lg:col-span-1">
              <OrganismCore status="alive" className="mb-16" />
              <div className="text-center mt-8">
                <h2 className="text-2xl font-bold gradient-text-primary mb-2">
                  Gen-4 Autonomous Organism
                </h2>
                <p className="text-sm text-muted-foreground max-w-md">
                  Self-evolving species digital discovering problems, building solutions,
                  and generating revenue without human intervention.
                </p>
                <div className="mt-4 flex gap-2 justify-center">
                  <Button variant="outline" size="sm" onClick={() => handleAction("SaaS Factory", runFactory)}>Factory</Button>
                  <Button variant="outline" size="sm" onClick={() => handleAction("Growth Engine", runGrowth)}>Growth</Button>
                </div>
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
                   value={state?.activeAgents ?? 0}
                  variant="success"
                  size="sm"
                />
                <MetricDisplay
                  label="Terminated"
                   value={state?.terminatedAgents ?? 0}
                  variant="destructive"
                  size="sm"
                />
                <div className="pt-2">
                  <span className="text-xs text-muted-foreground uppercase tracking-wider">Efficiency</span>
                  <Progress value={92} className="mt-2 h-2" />
                  <span className="text-xs text-primary mt-1 block">92% Optimal</span>
                </div>
                <div className="grid grid-cols-2 gap-3 pt-2">
                  <Button onClick={() => handleAction("Monetization", runMonetization)} variant="outline" className="text-accent border-accent/20 hover:bg-accent/10">
                    Monetize
                  </Button>
                  <Button onClick={() => handleAction("Spawner", runSpawner)} variant="outline" className="text-intelligence border-intelligence/20 hover:bg-intelligence/10">
                    Spawn Agent
                  </Button>
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
              description="Scanning the digital world for human problems and pain points."
              metrics={[
                { label: "Sources", value: 7, trend: "up", trendValue: "Playwright" },
                { label: "Found", value: state?.problemsScanned ?? 0 },
              ]}
            />
            <OrganEngine
              name="Decision Core"
              icon={Brain}
              variant="decision"
              status="online"
              description="Analyzing and scoring problems by automation potential and revenue."
              metrics={[
                { label: "Ideas", value: state?.ideasGenerated ?? 0 },
                { label: "Logic", value: "Gen-4" },
              ]}
            />
            <OrganEngine
              name="SaaS Factory"
              icon={Factory}
              variant="factory"
              status="online"
              description="Building and deploying MVP solutions automatically."
              metrics={[
                { label: "Built", value: state?.productsBuilt ?? 0 },
                { label: "Stack", value: "FastAPI" },
              ]}
            />
            <OrganEngine
              name="Growth Engine"
              icon={TrendingUp}
              variant="growth"
              status="online"
              description="Marketing, content generation, and user acquisition."
              metrics={[
                { label: "Channels", value: 3 },
                { label: "Outbox", value: "Active" },
              ]}
            />
            <OrganEngine
              name="Memory Engine"
              icon={Database}
              variant="memory"
              status="online"
              description="Recording patterns, failures, and evolution data."
              metrics={[
                { label: "Logs", value: logs.length },
                { label: "DB", value: "SQLite" },
              ]}
            />
            <OrganEngine
              name="Immune System"
              icon={Shield}
              variant="danger"
              status="online"
              description="Preventing runaway processes and protecting resources."
              metrics={[
                { label: "Status", value: "Active" },
                { label: "Health", value: "98%" },
              ]}
            />
          </div>
        </section>

        {/* Agents & Logs Section */}
        <section className="grid lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
              <Bot className="w-5 h-5 text-intelligence" />
              Autonomous Agents
            </h3>
            <OrganismCard variant="default" size="lg" className="p-6 h-[400px] overflow-y-auto">
              <div className="space-y-4">
                {agents.length === 0 && (
                   <p className="text-sm text-muted-foreground">No agents active. Trigger Spawner to begin.</p>
                )}
                {agents.map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between p-3 border border-border/50 rounded-lg bg-card/50">
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${agent.status === 'active' ? 'bg-success animate-pulse' : 'bg-destructive'}`} />
                      <div>
                        <p className="font-medium text-sm">{agent.type}</p>
                        <p className="text-xs text-muted-foreground">{agent.personality}</p>
                      </div>
                    </div>
                    <Badge variant={agent.status === 'active' ? 'default' : 'destructive'}>
                      {agent.status.toUpperCase()}
                    </Badge>
                  </div>
                ))}
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
