import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  generation: number;
  status: string;
};

export function useOrganismReal() {
  const qc = useQueryClient();

  const logsQuery = useQuery({
    queryKey: ["engine_logs"],
    queryFn: async () => {
      const response = await fetch("/api/logs");
      if (!response.ok) throw new Error("Gagal mengambil log");
      return response.json();
    },
    refetchInterval: 3000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const response = await fetch("/api/metrics");
      if (!response.ok) throw new Error("Gagal mengambil metrik");
      return response.json() as Promise<RealOrganismState>;
    },
    refetchInterval: 5000,
  });

  const runSense = useCallback(async () => {
    const response = await fetch("/api/run-sense", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Sense engine");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runDecision = useCallback(async () => {
    const response = await fetch("/api/run-decision", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Decision core");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runFactory = useCallback(async () => {
    const response = await fetch("/api/run-factory", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan SaaS Factory");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
  }, [qc]);

  const runGrowth = useCallback(async () => {
    const response = await fetch("/api/run-growth", { method: "POST" });
    if (!response.ok) throw new Error("Gagal menjalankan Growth engine");
    await qc.invalidateQueries({ queryKey: ["engine_logs"] });
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
