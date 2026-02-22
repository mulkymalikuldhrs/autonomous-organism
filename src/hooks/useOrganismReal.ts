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
    enabled: !!profileQuery.data?.organization_id,
    queryFn: async () => {
      const orgId = profileQuery.data!.organization_id;
      const { data, error } = await supabase
        .from("engine_logs")
        .select("id, level, source, message, created_at")
        .eq("organization_id", orgId)
        .order("created_at", { ascending: false })
        .limit(100);
      if (error) throw error;
      return data;
    },
    refetchInterval: 4000,
  });

  const metricsQuery = useQuery({
    queryKey: ["metrics"],
    enabled: !!profileQuery.data?.organization_id,
    queryFn: async () => {
      const orgId = profileQuery.data!.organization_id;
      const [{ count: rawCount }, { count: ideaCount }] = await Promise.all([
        supabase.from("problem_raw").select("id", { count: "exact", head: true }).eq("organization_id", orgId),
        supabase.from("idea_candidates").select("id", { count: "exact", head: true }).eq("organization_id", orgId),
      ]);
      return {
        problemsScanned: rawCount ?? 0,
        ideasGenerated: ideaCount ?? 0,
        revenue: 0,
        generation: 1,
      } satisfies RealOrganismState;
    },
    refetchInterval: 6000,
  });

  const runSense = useCallback(async () => {
    const { error } = await supabase.functions.invoke("ingest-sense", { body: {} });
    if (error) throw error;
    await Promise.all([
      qc.invalidateQueries({ queryKey: ["engine_logs"] }),
      qc.invalidateQueries({ queryKey: ["metrics"] }),
    ]);
  }, [qc]);

  const runDecision = useCallback(
    async ({ theme, score, summary, evidence }: { theme: string; score: number; summary: string; evidence: any }) => {
      const orgId = profileQuery.data?.organization_id;
      if (!orgId) throw new Error("Org belum siap");
      const { error } = await supabase.from("idea_candidates").insert({
        organization_id: orgId,
        theme,
        score,
        summary,
        evidence,
      });
      if (error) throw error;
      await qc.invalidateQueries({ queryKey: ["metrics"] });
    },
    [profileQuery.data?.organization_id, qc]
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
