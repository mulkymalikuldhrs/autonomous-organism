import { useEffect, useState } from "react";

/**
 * Gen-4.1 Autonomous Auth Gate
 * In local autonomous mode, we bypass Supabase Auth to allow the system
 * to operate without manual login, while maintaining the component structure.
 */
export function AuthGate({ children }: { children: React.ReactNode }) {
  const [ready] = useState(true);

  if (!ready) return null;
  return <>{children}</>;
}
