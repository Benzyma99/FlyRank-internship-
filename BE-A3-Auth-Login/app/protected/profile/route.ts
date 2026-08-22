import { NextResponse } from "next/server";
import { withAuth } from "@/lib/auth-middleware";

/** GET /protected/profile — protected by auth middleware */
export const GET = withAuth(async (_request, { user }) => {
  // Route logic runs only after middleware verifies the token
  const { id, email, created_at } = user;

  return NextResponse.json({ id, email, created_at }, { status: 200 });
});
