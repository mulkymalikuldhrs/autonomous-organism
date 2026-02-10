import { useCallback } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";

export type RealOrganismState = {
  problemsScanned: number;
  ideasGenerated: number;
  revenue: number;
  generation: number;
};

export function useOrganismReal() {
  const qc = useQueryClient();

  const sessionQuery = useQuery({
    queryKey: ["auth", "session"],
    queryFn: async () => {
      const { data, error } = await supabase.auth.getSession();
      if (error) throw error;
      return data.session;
    },
  });

  const profileQuery = useQuery({
    queryKey: ["profile"],
    enabled: !!sessionQuery.data,
    queryFn: async () => {
      const { data, error } = await supabase
        .from("profiles")
        .select("organization_id, role, display_name")
        .eq("user_id", sessionQuery.data!.user.id)
        .maybeSingle();
      if (error) throw error;
      return data;
    },
  });

  const logsQuery = useQuery({
    queryKey: ["engine_logs"],
    queryFn: async () => {
      const resp = await fetch("/api/logs");
      if (!resp.ok) throw new Error("Failed to fetch logs from local engine");
      return resp.json();
    },
    refetchInterval: 4000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    queryFn: async () => {
      const resp = await fetch("/api/metrics");
      if (!resp.ok) throw new Error("Failed to fetch metrics from local engine");
      return resp.json() as Promise<RealOrganismState>;
    },
    refetchInterval: 6000,
  });

  const runSense = useCallback(async () => {
    const resp = await fetch("/api/run/sense", { method: "POST" });
    if (!resp.ok) throw new Error("Sense trigger failed");
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runDecision = useCallback(
    async () => {
      // In the new architecture, decision is part of the lifecycle or can be triggered.
      // For now, we'll let it be autonomous, but we can add a POST /api/run/decision if needed.
      console.log("Decision run triggered (Autonomous Lifecycle will pick it up)");
    },
    []
  );

  return {
    session: sessionQuery.data,
    profile: profileQuery.data,
    logs: logsQuery.data ?? [],
    logsLoading: logsQuery.isLoading,
    state: metricsQuery.data,
    stateLoading: metricsQuery.isLoading,
    runSense,
    runDecision,
  };
}
