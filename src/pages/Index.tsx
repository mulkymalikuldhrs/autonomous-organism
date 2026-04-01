import { Eye, Brain, Factory, TrendingUp, Database, Shield, Bot, Zap, Coins, Users } from "lucide-react";
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

  const handleRun = async (fn: () => Promise<void>, name: string) => {
    try {
      await fn();
      toast({ title: name, description: `${name} engine started.` });
    } catch (e: any) {
      toast({ title: `${name} failed`, description: e?.message ?? "Error", variant: "destructive" });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 relative overflow-hidden font-sans">
      <NeuralBackground />

      <div className="relative z-10">
        <Header
          organismName="ORGANISM-ALPHA"
          generation={state?.generation ?? 4}
          status={state?.status ?? "online"}
        />

        <main className="container mx-auto px-4 py-8">
          {/* Main Dashboard Grid */}
          <section className="mb-12">
            <div className="grid lg:grid-cols-3 gap-8 items-stretch">

              {/* Vital Signs */}
              <OrganismCard variant="default" size="lg" className="border-cyan-500/30 bg-slate-900/50 backdrop-blur-md">
                <OrganismCardHeader>
                  <Zap className="w-5 h-5 text-cyan-400 animate-pulse" />
                  <OrganismCardTitle className="text-cyan-400">Vital Signs</OrganismCardTitle>
                </OrganismCardHeader>
                <OrganismCardContent className="space-y-6">
                  <MetricDisplay 
                    label="Problems Scanned" 
                    value={(state?.problemsScanned ?? 0).toLocaleString()} 
                    variant="primary"
                    trend="up"
                  />
                  <MetricDisplay 
                    label="Ideas Generated" 
                    value={state?.ideasGenerated ?? 0} 
                    variant="default"
                    trend="up"
                  />
                  <MetricDisplay 
                    label="Products Built" 
                    value={state?.productsBuilt ?? 0}
                    variant="accent"
                  />
                  <div className="pt-2">
                    <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">System Health</span>
                    <Progress value={94} className="mt-2 h-1.5 bg-slate-800" indicatorClassName="bg-cyan-500" />
                    <span className="text-[10px] text-cyan-400 mt-1 block font-mono">94% OPTIMAL / GEN-4</span>
                  </div>

                  <div className="grid grid-cols-2 gap-2 pt-2">
                    <Button onClick={() => handleRun(runSense, "Sense")} size="sm" className="bg-cyan-600 hover:bg-cyan-500 text-xs h-8">Sense</Button>
                    <Button onClick={() => handleRun(runDecision, "Decision")} variant="secondary" size="sm" className="bg-violet-600 hover:bg-violet-500 text-xs h-8">Decision</Button>
                    <Button onClick={() => handleRun(runFactory, "Factory")} variant="outline" size="sm" className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10 text-xs h-8">Factory</Button>
                    <Button onClick={() => handleRun(runSpawner, "Spawner")} variant="ghost" size="sm" className="text-violet-400 hover:bg-violet-500/10 text-xs h-8">Spawner</Button>
                  </div>
                </OrganismCardContent>
              </OrganismCard>

              {/* Core Visual */}
              <div className="flex flex-col items-center justify-center py-8 lg:col-span-1">
                <OrganismCore status="alive" className="mb-12" />
                <div className="text-center mt-4">
                  <h2 className="text-3xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-500 mb-2">
                    AUTONOMOUS SPECIES
                  </h2>
                  <p className="text-xs text-slate-400 max-w-xs mx-auto leading-relaxed font-mono uppercase">
                    Gen-4 Digital Organism: Identifying problems, breeding businesses, evolving strategies.
                  </p>
                </div>
              </div>

              {/* Revenue Engine */}
              <OrganismCard variant="factory" size="lg" className="border-violet-500/30 bg-slate-900/50 backdrop-blur-md">
                <OrganismCardHeader>
                  <Coins className="w-5 h-5 text-violet-400" />
                  <OrganismCardTitle className="text-violet-400">Revenue Engine</OrganismCardTitle>
                </OrganismCardHeader>
                <OrganismCardContent className="space-y-6">
                  <MetricDisplay 
                    label="Total Revenue" 
                    value={`$${(state?.revenue ?? 0).toFixed(2)}`} 
                    variant="accent"
                    trend="up"
                    className="text-violet-400"
                  />
                  <div className="grid grid-cols-2 gap-4">
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
                  </div>
                  <div className="pt-2">
                    <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">Monetization Efficiency</span>
                    <Progress value={78} className="mt-2 h-1.5 bg-slate-800" indicatorClassName="bg-violet-500" />
                    <span className="text-[10px] text-violet-400 mt-1 block font-mono">SCALING / $50K TARGET</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 pt-2">
                    <Button onClick={() => handleRun(runGrowth, "Growth")} size="sm" variant="outline" className="border-violet-500/50 text-violet-400 hover:bg-violet-500/10 text-xs h-8">Growth</Button>
                    <Button onClick={() => handleRun(runMonetization, "Monetize")} size="sm" className="bg-violet-600 hover:bg-violet-500 text-xs h-8">Monetize</Button>
                  </div>
                </OrganismCardContent>
              </OrganismCard>

            </div>
          </section>

          {/* Engine Status Grid */}
          <section className="mb-12">
            <h3 className="text-sm font-bold mb-6 flex items-center gap-2 uppercase tracking-[0.3em] text-slate-500">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-ping" />
              Engine Sub-Systems
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <OrganEngine
                name="Sense Engine"
                icon={Eye}
                variant="sense"
                status="processing"
                description="Gen-4 Playwright scan of Reddit, HN, and IndieHackers."
                metrics={[
                  { label: "Sources", value: 7 },
                  { label: "Mode", value: "Real-time" },
                ]}
              />
              <OrganEngine
                name="Decision Core"
                icon={Brain}
                variant="decision"
                status="online"
                description="LLM-based weighted formula (Negative Emotion, Volume, Ease)."
                metrics={[
                  { label: "Logic", value: "Weighted" },
                  { label: "AI", value: "Mistral-7B" },
                ]}
              />
              <OrganEngine
                name="SaaS Factory"
                icon={Factory}
                variant="factory"
                status="online"
                description="Generating full-stack specs, codebases, and Dockerfiles."
                metrics={[
                  { label: "Output", value: "Full-Stack" },
                  { label: "Registry", value: "Local" },
                ]}
              />
              <OrganEngine
                name="Growth Engine"
                icon={TrendingUp}
                variant="growth"
                status="idle"
                description="Multi-stage marketing campaigns (Twitter, Reddit, IH)."
                metrics={[
                  { label: "Outbox", value: "Active" },
                  { label: "Channels", value: 3 },
                ]}
              />
              <OrganEngine
                name="Memory Engine"
                icon={Database}
                variant="memory"
                status="online"
                description="SQLite persistence of lifecycle logs and evolution data."
                metrics={[
                  { label: "Storage", value: "Local" },
                  { label: "Learning", value: "Revenue" },
                ]}
              />
              <OrganEngine
                name="Immune System"
                icon={Shield}
                variant="danger"
                status="online"
                description="System integrity check, error monitoring, and resource protection."
                metrics={[
                  { label: "Disk", value: "Normal" },
                  { label: "Health", value: "98%" },
                ]}
              />
            </div>
          </section>

          {/* Agents & Logs */}
          <section className="grid lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-sm font-bold mb-6 flex items-center gap-2 uppercase tracking-[0.3em] text-slate-500">
                <Bot className="w-5 h-5 text-violet-400" />
                Active Agents
              </h3>
              <OrganismCard variant="default" size="lg" className="bg-slate-900/50 backdrop-blur-md border-slate-800">
                <div className="p-2 space-y-3">
                  {agents.length === 0 ? (
                    <p className="text-xs text-slate-500 italic p-4">No agents spawned. Run Spawner to initialize.</p>
                  ) : (
                    agents.map((agent) => (
                      <div key={agent.id} className="flex justify-between items-center p-3 rounded-lg bg-slate-800/40 border border-slate-700/50 hover:border-cyan-500/30 transition-colors">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${agent.status === 'active' ? 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]' : 'bg-rose-500'}`} />
                          <div>
                            <p className="text-sm font-bold text-slate-200 uppercase tracking-tighter">{agent.type} Agent</p>
                            <p className="text-[10px] text-slate-400 font-mono">Personality: {agent.personality}</p>
                          </div>
                        </div>
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${agent.status === 'active' ? 'border-emerald-500/30 text-emerald-400' : 'border-rose-500/30 text-rose-400'}`}>
                          {agent.status.toUpperCase()}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              </OrganismCard>
            </div>

            <div>
              <h3 className="text-sm font-bold mb-6 flex items-center gap-2 uppercase tracking-[0.3em] text-slate-500">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                SENSORY LOG
              </h3>
              <OrganismCard variant="default" size="lg" className="h-[400px] bg-slate-900/50 backdrop-blur-md border-slate-800 overflow-hidden">
                <ActivityLog entries={logEntries} maxHeight="360px" />
              </OrganismCard>
            </div>
          </section>

          {/* Final Footer */}
          <footer className="mt-20 pt-8 border-t border-slate-800/50 text-center">
            <p className="text-[10px] text-slate-500 font-mono tracking-[0.5em] uppercase">
              ORGANISM-ALPHA • GEN-0004 • AUTONOMOUS LIFE SYSTEM • ZERO COST INFRA
            </p>
            <p className="text-[10px] text-slate-600 mt-4 italic">
              "Pemilik bukan bikin produk. Pemilik menciptakan spesies digital."
            </p>
          </footer>
        </main>
      </div>
    </div>
  );
}
