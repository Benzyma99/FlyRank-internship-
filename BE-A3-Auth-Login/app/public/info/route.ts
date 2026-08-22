import { NextResponse } from "next/server";

/** GET /public/info — open to anyone; no auth required */
export async function GET() {
  return NextResponse.json(
    { message: "Welcome stranger! This info is public." },
    { status: 200 },
  );
}
