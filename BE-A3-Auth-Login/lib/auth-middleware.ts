import { NextResponse } from "next/server";
import type { User } from "@supabase/supabase-js";
import { supabase } from "@/lib/supabase";

export type AuthenticatedContext = {
  user: User;
  token: string;
};

type AuthMiddlewareResult =
  | { ok: true; context: AuthenticatedContext }
  | { ok: false; response: NextResponse };

/**
 * Reusable auth middleware — extracts and verifies the Bearer token once,
 * so protected routes don't repeat the same checks.
 */
export async function requireAuth(
  request: Request,
): Promise<AuthMiddlewareResult> {
  const authHeader = request.headers.get("Authorization");

  // Expect "Bearer <token>"; reject missing / malformed headers
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return {
      ok: false,
      response: NextResponse.json(
        { error: "Access token required" },
        { status: 401 },
      ),
    };
  }

  const token = authHeader.slice("Bearer ".length).trim();

  if (!token) {
    return {
      ok: false,
      response: NextResponse.json(
        { error: "Access token required" },
        { status: 401 },
      ),
    };
  }

  // Verify the JWT with Supabase (rejects expired, tampered, or invalid tokens)
  const { data, error } = await supabase.auth.getUser(token);

  if (error || !data.user) {
    return {
      ok: false,
      response: NextResponse.json(
        { error: "Invalid or expired token" },
        { status: 401 },
      ),
    };
  }

  return {
    ok: true,
    context: { user: data.user, token },
  };
}

/**
 * Wraps a route handler so auth runs first; handler only executes when verified.
 */
export function withAuth(
  handler: (
    request: Request,
    context: AuthenticatedContext,
  ) => Promise<Response> | Response,
) {
  return async (request: Request) => {
    const auth = await requireAuth(request);

    if (!auth.ok) {
      return auth.response;
    }

    return handler(request, auth.context);
  };
}
