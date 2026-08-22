import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

/** POST /auth/signup — register a new user with email + password */
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

  const { data, error } = await supabase.auth.signUp({ email, password });

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }

  // Return the newly created Supabase user object
  return NextResponse.json(data.user, { status: 201 });
}
