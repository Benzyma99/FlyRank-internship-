"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchProfile } from "@/lib/auth-client";
import { AuthForm } from "./auth-form";

/** Home page auth gate — shows the login form or redirects if already signed in. */
export function AuthPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Skip the form when a valid session already exists
    fetchProfile()
      .then(() => router.replace("/dashboard"))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-sm text-zinc-500 dark:text-zinc-400">Loading…</p>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col items-center justify-center px-4">
      <AuthForm onSuccess={() => router.replace("/dashboard")} />
    </div>
  );
}
