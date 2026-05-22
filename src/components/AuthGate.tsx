import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";

export function AuthGate({ children }: { children: React.ReactNode }) {
  const nav = useNavigate();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Mode Otonom Lokal: Bypass auth untuk kemudahan akses dashboard sistem
    setReady(true);
  }, []);

  if (!ready) return null;
  return <>{children}</>;
}
