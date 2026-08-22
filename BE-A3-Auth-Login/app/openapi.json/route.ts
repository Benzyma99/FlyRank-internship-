import { NextResponse } from "next/server";
import { openapiSpec } from "@/lib/swagger";

/** Serve the OpenAPI spec used by Swagger UI */
export async function GET() {
  return NextResponse.json(openapiSpec);
}
