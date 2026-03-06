import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  generation: number;
};

export function useOrganismReal() {
  const qc = useQueryClient();

  const logsQuery = useQuery({
    queryKey: ["engine_logs"],
    queryFn: async () => {
      const response = await fetch("/api/logs");
      if (!response.ok) throw new Error("Failed to fetch logs");
      return response.json();
    },
    refetchInterval: 4000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const response = await fetch("/api/metrics");
      if (!response.ok) throw new Error("Failed to fetch metrics");
      return response.json() as Promise<RealOrganismState>;
    },
    refetchInterval: 6000,
  });

  const runSense = useCallback(async () => {
    const response = await fetch("/api/run-sense", { method: "POST" });
    if (!response.ok) throw new Error("Failed to run Sense engine");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runDecision = useCallback(async () => {
    const response = await fetch("/api/run-decision", { method: "POST" });
    if (!response.ok) throw new Error("Failed to run Decision engine");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runFactory = useCallback(async () => {
    const response = await fetch("/api/run-factory", { method: "POST" });
    if (!response.ok) throw new Error("Failed to run SaaS Factory");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runGrowth = useCallback(async () => {
    const response = await fetch("/api/run-growth", { method: "POST" });
    if (!response.ok) throw new Error("Failed to run Growth engine");
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
    runSense,
    runDecision,
    runFactory,
    runGrowth,
  };
}
