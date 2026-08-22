import { NextResponse } from "next/server";
import {
  getSwaggerAsset,
  getSwaggerAssetContentType,
  getSwaggerHtml,
  getSwaggerInitJs,
} from "@/lib/swagger";

type RouteContext = {
  params: Promise<{ path?: string[] }>;
};

/**
 * Swagger UI at /docs (powered by swagger-ui-express HTML generation).
 * Static assets are served from swagger-ui-dist under /docs/*.
 */
export async function GET(_request: Request, context: RouteContext) {
  const { path = [] } = await context.params;
  const assetPath = path.join("/");

  // Main docs page
  if (!assetPath) {
    return new NextResponse(getSwaggerHtml(), {
      headers: { "Content-Type": "text/html; charset=utf-8" },
    });
  }

  // Boot script referenced by the generated HTML
  if (assetPath === "swagger-ui-init.js") {
    return new NextResponse(getSwaggerInitJs(), {
      headers: { "Content-Type": "application/javascript; charset=utf-8" },
    });
  }

  try {
    const content = await getSwaggerAsset(assetPath);

    return new NextResponse(content, {
      headers: { "Content-Type": getSwaggerAssetContentType(assetPath) },
    });
  } catch {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
}
