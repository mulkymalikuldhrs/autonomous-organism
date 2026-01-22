import { useState, useEffect, useCallback } from "react";
import type { LogEntry } from "@/components/ui/activity-log";

interface OrganismState {
  status: "alive" | "dormant" | "spawning" | "dying";
  generation: number;
  uptime: number;
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  agentsActive: number;
  agentsTerminated: number;
}

interface Agent {
  id: string;
  name: string;
  type: "research" | "builder" | "growth" | "support";
  status: "active" | "idle" | "terminated" | "spawning";
  tasksCompleted: number;
  uptime: string;
  efficiency: number;
}

const agentNames = {
  research: ["SCOUT-", "PROBE-", "SENSOR-", "SCAN-"],
  builder: ["FORGE-", "BUILD-", "CREATE-", "CRAFT-"],
  growth: ["GROW-", "SCALE-", "BOOST-", "VIRAL-"],
  support: ["FIX-", "HEAL-", "PATCH-", "MEND-"],
};

const logMessages = {
  sense: [
    "Scanning Reddit for pain points...",
    "Analyzing YouTube comments...",
    "Processing Quora questions...",
    "Found 47 potential problems in tech space",
    "Detected trending issue: API rate limiting",
  ],
  decision: [
    "Clustering problems by category...",
    "Running sentiment analysis...",
    "Calculating automation potential...",
    "Top candidate: developer tools (score: 87)",
    "Selected MVP: API monitoring dashboard",
  ],
  factory: [
    "Generating project structure...",
    "Creating database schema...",
    "Building API endpoints...",
    "Deploying to Vercel...",
    "Product live: monitor.saas.ai",
  ],
  growth: [
    "Generating blog content...",
    "Posting to Medium...",
    "A/B testing CTAs...",
    "New signup from organic search",
    "Revenue +$12.99 from subscription",
  ],
  memory: [
    "Recording success pattern...",
    "Logging failed experiment...",
    "Updating strategy weights...",
    "Weekly analysis complete",
  ],
  system: [
    "Agent FORGE-7 efficiency dropping...",
    "Spawning new research agent...",
    "Terminating idle agent...",
    "Memory optimization complete",
    "Immune system check: OK",
  ],
};

export function useOrganismSimulation() {
  const [state, setState] = useState<OrganismState>({
    status: "alive",
    generation: 1,
    uptime: 0,
    problemsScanned: 2847,
    ideasGenerated: 156,
    productsBuilt: 3,
    revenue: 247.5,
    agentsActive: 4,
    agentsTerminated: 2,
  });

  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [agents, setAgents] = useState<Agent[]>([
    { id: "R001", name: "SCOUT-1", type: "research", status: "active", tasksCompleted: 127, uptime: "3d 4h", efficiency: 94 },
    { id: "B001", name: "FORGE-1", type: "builder", status: "active", tasksCompleted: 45, uptime: "2d 12h", efficiency: 88 },
    { id: "G001", name: "GROW-1", type: "growth", status: "idle", tasksCompleted: 89, uptime: "1d 8h", efficiency: 72 },
    { id: "S001", name: "FIX-1", type: "support", status: "active", tasksCompleted: 234, uptime: "5d 2h", efficiency: 91 },
    { id: "R002", name: "PROBE-2", type: "research", status: "terminated", tasksCompleted: 12, uptime: "0d 0h", efficiency: 0 },
    { id: "B002", name: "BUILD-2", type: "builder", status: "spawning", tasksCompleted: 0, uptime: "0d 0h", efficiency: 0 },
  ]);

  const addLog = useCallback((type: LogEntry["type"], source: string, message: string) => {
    const newLog: LogEntry = {
      id: Date.now().toString(),
      timestamp: new Date(),
      type,
      source,
      message,
    };
    setLogs((prev) => [newLog, ...prev].slice(0, 100));
  }, []);

  // Simulate organism activity
  useEffect(() => {
    const interval = setInterval(() => {
      // Random activity
      const sources = ["SENSE", "DECISION", "FACTORY", "GROWTH", "MEMORY", "SYSTEM"];
      const sourceKey = sources[Math.floor(Math.random() * sources.length)].toLowerCase() as keyof typeof logMessages;
      const messages = logMessages[sourceKey] || logMessages.system;
      const message = messages[Math.floor(Math.random() * messages.length)];
      
      const types: LogEntry["type"][] = ["info", "success", "warning", "system"];
      const type = types[Math.floor(Math.random() * types.length)];

      addLog(type, sourceKey.toUpperCase(), message);

      // Update metrics occasionally
      if (Math.random() > 0.7) {
        setState((prev) => ({
          ...prev,
          uptime: prev.uptime + 1,
          problemsScanned: prev.problemsScanned + Math.floor(Math.random() * 10),
          ideasGenerated: Math.random() > 0.9 ? prev.ideasGenerated + 1 : prev.ideasGenerated,
          revenue: Math.random() > 0.8 ? +(prev.revenue + Math.random() * 5).toFixed(2) : prev.revenue,
        }));
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [addLog]);

  // Initial logs
  useEffect(() => {
    addLog("system", "CORE", "Organism initialized successfully");
    addLog("info", "SENSE", "Beginning environmental scan...");
    addLog("success", "SYSTEM", "All engines operational");
  }, [addLog]);

  return { state, logs, agents, addLog };
}
