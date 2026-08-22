import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

/** POST /auth/login — authenticate with email + password, return JWT tokens */
export async function POST(request: Request) {
  let body: { email?: string; password?: string };

  try {
    body = await request.json();
  } catch {
    // Body was missing or not valid JSON
    return NextResponse.json({ error: "Bad Request" }, { status: 400 });
  }

  const { email, password } = body;

  // Both fields are required
  if (!email || !password) {
    return NextResponse.json({ error: "Bad Request" }, { status: 400 });
  }

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  // Wrong password, unknown user, etc.
  if (error) {
    return NextResponse.json(
      { error: "Invalid login credentials" },
      { status: 401 },
    );
  }

  // Session holds the access (JWT) and refresh tokens
  return NextResponse.json(
    {
      access_token: data.session.access_token,
      refresh_token: data.session.refresh_token,
    },
    { status: 200 },
  );
}
