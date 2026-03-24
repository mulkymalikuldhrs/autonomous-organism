import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  activeAgents: number;
  terminatedAgents: number;
  generation: number;
};

export type Agent = {
  id: number;
  type: string;
  status: string;
  personality: string;
  last_run: string;
};

export function useOrganismReal() {
  const qc = useQueryClient();

  const logsQuery = useQuery({
    queryKey: ["engine_logs"],
    queryFn: async () => {
      const res = await fetch("/api/logs");
      if (!res.ok) throw new Error("Failed to fetch logs");
      return res.json();
    },
    refetchInterval: 3000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const res = await fetch("/api/metrics");
      if (!res.ok) throw new Error("Failed to fetch metrics");
      return res.json() as Promise<RealOrganismState>;
    },
    refetchInterval: 5000,
  });

  const agentsQuery = useQuery({
    queryKey: ["agents"],
    queryFn: async () => {
      const res = await fetch("/api/agents");
      if (!res.ok) throw new Error("Failed to fetch agents");
      return res.json() as Promise<Agent[]>;
    },
    refetchInterval: 10000,
  });

  const runSense = useCallback(async () => {
    const res = await fetch("/api/run-sense", { method: "POST" });
    if (!res.ok) throw new Error("Sense failed");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runDecision = useCallback(async () => {
    const res = await fetch("/api/run-decision", { method: "POST" });
    if (!res.ok) throw new Error("Decision failed");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runFactory = useCallback(async () => {
    const res = await fetch("/api/run-factory", { method: "POST" });
    if (!res.ok) throw new Error("Factory failed");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runGrowth = useCallback(async () => {
    const res = await fetch("/api/run-growth", { method: "POST" });
    if (!res.ok) throw new Error("Growth failed");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runMonetization = useCallback(async () => {
    const res = await fetch("/api/run-monetization", { method: "POST" });
    if (!res.ok) throw new Error("Monetization failed");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runSpawner = useCallback(async () => {
    const res = await fetch("/api/run-spawner", { method: "POST" });
    if (!res.ok) throw new Error("Spawner failed");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  return {
    logs: logsQuery.data ?? [],
    state: metricsQuery.data,
    agents: agentsQuery.data ?? [],
    runSense,
    runDecision,
    runFactory,
    runGrowth,
    runMonetization,
    runSpawner
  };
}
