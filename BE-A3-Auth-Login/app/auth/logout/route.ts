import { NextResponse } from "next/server";
import { withAuth } from "@/lib/auth-middleware";
import { signOutWithToken } from "@/lib/supabase";

/** POST /auth/logout — protected by auth middleware */
export const POST = withAuth(async (_request, { token }) => {
  const { error } = await signOutWithToken(token);

  if (error) {
    return NextResponse.json(
      { error: "Invalid or expired token" },
      { status: 401 },
    );
  }

  // Successful logout — no response body
  return new NextResponse(null, { status: 204 });
});
