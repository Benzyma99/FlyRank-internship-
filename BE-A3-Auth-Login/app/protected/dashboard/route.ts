import { NextResponse } from "next/server";
import { withAuth } from "@/lib/auth-middleware";

/** GET /protected/dashboard — second protected route using shared middleware */
export const GET = withAuth(async (_request, { user }) => {
  return NextResponse.json(
    {
      message: `Welcome back, ${user.email}!`,
      user_id: user.id,
    },
    { status: 200 },
  );
});
