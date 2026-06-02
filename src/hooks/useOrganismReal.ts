import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  generation: number;
  agentsActive: number;
  agentsTerminated: number;
  engineRuns: { engine: string; status: string; count: number }[];
};

export function useOrganismReal() {
  const qc = useQueryClient();

  // Unified metrics fetch from FastAPI
  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const resp = await fetch("/api/metrics");
      if (!resp.ok) throw new Error("Failed to fetch metrics");
      const data = await resp.json();
      return {
        ...data,
        engineRuns: [], // Placeholder or fetched separately if needed
        agentsActive: 0,
        agentsTerminated: 0,
      } as RealOrganismState;
    },
    refetchInterval: 5000,
  });

  const logsQuery = useQuery({
    queryKey: ["engine_logs"],
    queryFn: async () => {
      const resp = await fetch("/api/logs");
      if (!resp.ok) throw new Error("Failed to fetch logs");
      return await resp.json();
    },
    refetchInterval: 3000,
  });

  // Mocked for compatibility with existing UI components while keeping real integration
  const ideasQuery = useQuery({
    queryKey: ["idea_candidates"],
    queryFn: async () => [],
  });

  const runEngine = useCallback(async (name: string) => {
    const resp = await fetch(`/api/engine/run/${name}`, { method: "POST" });
    if (!resp.ok) throw new Error(`Failed to trigger ${name}`);
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["metrics"] }),
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
    ]);
  }, [qc]);

  return {
    state: metricsQuery.data,
    logs: logsQuery.data ?? [],
    ideas: ideasQuery.data ?? [],
    engineRuns: [],
    runSense: () => runEngine("sense"),
    runDecision: () => runEngine("decision"),
    runFactory: () => runEngine("factory"),
    runGrowth: () => runEngine("growth"),
  };
}
