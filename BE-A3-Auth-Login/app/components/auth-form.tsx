"use client";

import { useState } from "react";
import { login, setTokens, signup } from "@/lib/auth-client";

type Mode = "login" | "signup";

type AuthFormProps = {
  /** Called after tokens are stored — parent handles redirect. */
  onSuccess: () => void;
};

/** Email/password form that toggles between login and signup modes. */
export function AuthForm({ onSuccess }: AuthFormProps) {
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === "login") {
        const { access_token, refresh_token } = await login(email, password);
        setTokens(access_token, refresh_token);
        onSuccess();
      } else {
        // Signup only creates the user — a separate login call is needed for tokens
        await signup(email, password);
        const { access_token, refresh_token } = await login(email, password);
        setTokens(access_token, refresh_token);
        onSuccess();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full max-w-sm">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
          {mode === "login" ? "Welcome back" : "Create an account"}
        </h1>
        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
          {mode === "login"
            ? "Sign in with your email and password"
            : "Sign up to get started"}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <label
            htmlFor="email"
            className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
          >
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-50 dark:focus:border-zinc-500"
            placeholder="you@example.com"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label
            htmlFor="password"
            className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
          >
            Password
          </label>
          <input
            id="password"
            type="password"
            required
            autoComplete={mode === "login" ? "current-password" : "new-password"}
            minLength={6}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-50 dark:focus:border-zinc-500"
            placeholder="••••••••"
          />
        </div>

        {error && (
          <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600 dark:bg-red-950 dark:text-red-400">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="mt-2 flex h-10 items-center justify-center rounded-lg bg-zinc-900 text-sm font-medium text-white transition-colors hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
        >
          {loading
            ? "Please wait…"
            : mode === "login"
              ? "Sign in"
              : "Create account"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-zinc-500 dark:text-zinc-400">
        {mode === "login" ? (
          <>
            Don&apos;t have an account?{" "}
            <button
              type="button"
              onClick={() => {
                setMode("signup");
                setError(null);
              }}
              className="font-medium text-zinc-900 underline-offset-4 hover:underline dark:text-zinc-50"
            >
              Sign up
            </button>
          </>
        ) : (
          <>
            Already have an account?{" "}
            <button
              type="button"
              onClick={() => {
                setMode("login");
                setError(null);
              }}
              className="font-medium text-zinc-900 underline-offset-4 hover:underline dark:text-zinc-50"
            >
              Sign in
            </button>
          </>
        )}
      </p>
    </div>
  );
}
