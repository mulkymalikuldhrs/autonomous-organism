import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  generation: number;
};

export type AgentStatus = {
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
        revenue: data.revenue ?? 0,
        generation: data.generation ?? 1,
      } satisfies RealOrganismState;
    },
    refetchInterval: 6000,
  });

  const agentsQuery = useQuery({
    queryKey: ["agents"],
    queryFn: async () => {
      const response = await fetch("/api/agents");
      if (!response.ok) throw new Error("Gagal mengambil status agen");
      return await response.json() as AgentStatus[];
    },
    refetchInterval: 8000,
  });

  const runSense = useCallback(async () => {
    const response = await fetch("/api/run-sense", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Sense");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runDecision = useCallback(async () => {
    const response = await fetch("/api/run-decision", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Decision");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runFactory = useCallback(async () => {
    const response = await fetch("/api/run-factory", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Factory");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runGrowth = useCallback(async () => {
    const response = await fetch("/api/run-growth", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Growth");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runSpawner = useCallback(async () => {
    const response = await fetch("/api/run-spawner", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Spawner");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["agents"] }),
    ]);
  }, [qc]);

  const runMonetization = useCallback(async () => {
    const response = await fetch("/api/run-monetization", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Monetization");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
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
