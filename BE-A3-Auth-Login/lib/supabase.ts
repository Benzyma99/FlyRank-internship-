import { createClient } from "@supabase/supabase-js";

// Loaded from .env.local by Next.js (server-side only — not prefixed with NEXT_PUBLIC_)
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error(
    "Missing SUPABASE_URL or SUPABASE_KEY. Set them in .env.local.",
  );
}

const url = supabaseUrl;
const key = supabaseKey;

// Shared Supabase client for auth routes and other server code
export const supabase = createClient(url, key);

/**
 * Sign out the session tied to the given access token.
 * Uses a request-scoped client so signOut applies to that JWT.
 */
export async function signOutWithToken(token: string) {
  const authedClient = createClient(url, key, {
    global: {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  });

  return authedClient.auth.signOut();
}
