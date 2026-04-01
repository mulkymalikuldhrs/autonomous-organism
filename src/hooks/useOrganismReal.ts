import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  activeAgents: number;
  terminatedAgents: number;
  revenue: number;
  generation: number;
  status: string;
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
      const response = await fetch("/api/logs");
      if (!response.ok) throw new Error("Gagal mengambil log");
      return await response.json();
    },
    refetchInterval: 4000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const response = await fetch("/api/metrics");
      if (!response.ok) throw new Error("Gagal mengambil metrics");
      const data = await response.json();
      return {
        problemsScanned: data.problemsScanned ?? 0,
        ideasGenerated: data.ideasGenerated ?? 0,
        productsBuilt: data.productsBuilt ?? 0,
        activeAgents: data.activeAgents ?? 0,
        terminatedAgents: data.terminatedAgents ?? 0,
        revenue: data.revenue ?? 0,
        generation: data.generation ?? 1,
        status: data.status ?? "offline",
      } satisfies RealOrganismState;
    },
    refetchInterval: 5000,
  });

  const agentsQuery = useQuery({
    queryKey: ["agents"],
    queryFn: async () => {
      const response = await fetch("/api/agents");
      if (!response.ok) throw new Error("Gagal mengambil agents");
      return await response.json() as Agent[];
    },
    refetchInterval: 5000,
  });

  const runSense = useCallback(async () => {
    const response = await fetch("/api/run-sense", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Sense");
    qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runDecision = useCallback(async () => {
    const response = await fetch("/api/run-decision", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Decision");
    qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runFactory = useCallback(async () => {
    const response = await fetch("/api/run-factory", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Factory");
    qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runGrowth = useCallback(async () => {
    const response = await fetch("/api/run-growth", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Growth");
    qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runSpawner = useCallback(async () => {
    const response = await fetch("/api/run-spawner", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Spawner");
    qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runMonetization = useCallback(async () => {
    const response = await fetch("/api/run-monetization", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Monetization");
    qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  return {
    logs: logsQuery.data ?? [],
    logsLoading: logsQuery.isLoading,
    state: metricsQuery.data,
    stateLoading: metricsQuery.isLoading,
    agents: agentsQuery.data ?? [],
    agentsLoading: agentsQuery.isLoading,
    runSense,
    runDecision,
    runFactory,
    runGrowth,
    runSpawner,
    runMonetization,
  };
}
