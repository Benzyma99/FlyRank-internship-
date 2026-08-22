import { readFile } from "fs/promises";
import { join } from "path";
import swaggerUi from "swagger-ui-express";
import openapiSpec from "@/openapi.json";

// Resolve swagger-ui-dist from node_modules (reliable in Next.js dev/build)
const swaggerAssetPath = join(
  process.cwd(),
  "node_modules",
  "swagger-ui-dist",
);

/** Swagger UI HTML generated via swagger-ui-express */
export function getSwaggerHtml() {
  const html = swaggerUi.generateHTML(openapiSpec, {
    customSiteTitle: "BE-A3 Auth Login API",
    swaggerOptions: {
      persistAuthorization: true,
    },
  });

  // Use absolute /docs/ paths so assets load when visiting /docs (no trailing slash)
  return html
    .replaceAll('href="./', 'href="/docs/')
    .replaceAll("href='./", "href='/docs/")
    .replaceAll('src="./', 'src="/docs/')
    .replaceAll("src='./", "src='/docs/");
}

/** Init script that boots Swagger UI with the embedded OpenAPI spec */
export function getSwaggerInitJs() {
  const options = {
    swaggerDoc: openapiSpec,
    customOptions: {
      persistAuthorization: true,
    },
  };

  return `
window.onload = function() {
  const options = ${JSON.stringify(options)};
  const swaggerOptions = {
    spec: options.swaggerDoc,
    dom_id: "#swagger-ui",
    deepLinking: true,
    presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
    plugins: [SwaggerUIBundle.plugins.DownloadUrl],
    layout: "StandaloneLayout",
    ...options.customOptions,
  };
  window.ui = SwaggerUIBundle(swaggerOptions);
};
`;
}

/** Serve swagger-ui-dist static assets (css, js, icons) */
export async function getSwaggerAsset(fileName: string) {
  const filePath = join(swaggerAssetPath, fileName);
  return readFile(filePath);
}

export function getSwaggerAssetContentType(fileName: string) {
  if (fileName.endsWith(".css")) {
    return "text/css";
  }

  if (fileName.endsWith(".js")) {
    return "application/javascript";
  }

  if (fileName.endsWith(".png")) {
    return "image/png";
  }

  if (fileName.endsWith(".html")) {
    return "text/html";
  }

  return "application/octet-stream";
}

export { openapiSpec };
