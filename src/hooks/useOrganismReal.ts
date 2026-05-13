import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  revenue: number;
  generation: number;
};

export function useOrganismReal() {
  const qc = useQueryClient();

  const logsQuery = useQuery({
    queryKey: ["engine_logs"],
    queryFn: async () => {
      const resp = await fetch("/api/logs");
      if (!resp.ok) throw new Error("Failed to fetch logs");
      return resp.json();
    },
    refetchInterval: 4000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const resp = await fetch("/api/metrics");
      if (!resp.ok) throw new Error("Failed to fetch metrics");
      return resp.json() as Promise<RealOrganismState>;
    },
    refetchInterval: 6000,
  });

  const runSense = useCallback(async () => {
    const resp = await fetch("/api/run/sense", { method: "POST" });
    if (!resp.ok) throw new Error("Sense engine failed");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runDecision = useCallback(
    async ({ theme, score, summary, evidence }: { theme: string; score: number; summary: string; evidence: any }) => {
      // In Gen-4.1, decision is handled autonomously by the backend
      // This remains for manual overrides if needed
      console.log("Manual decision trigger:", { theme, score, summary });
    },
    []
  );

  return {
    logs: logsQuery.data ?? [],
    logsLoading: logsQuery.isLoading,
    state: metricsQuery.data,
    stateLoading: metricsQuery.isLoading,
    runSense,
    runDecision,
  };
}
