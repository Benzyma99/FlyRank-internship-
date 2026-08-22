# BE-A3 Auth Login

A REST API built with [Next.js](https://nextjs.org) and [Supabase Auth](https://supabase.com/docs/guides/auth) that demonstrates user registration, login, token-based access control, and protected routes.

The API exposes public endpoints for onboarding and information, and protected endpoints that require a valid JWT access token. Authentication logic is centralized in reusable middleware so protected routes stay consistent and easy to extend.

Interactive API documentation is available at [`/docs`](http://localhost:3000/docs) via Swagger UI.

## Tech Stack

- **Next.js 16** (App Router, Route Handlers)
- **Supabase** (`@supabase/supabase-js`) for authentication
- **TypeScript**
- **Swagger UI** (`swagger-ui-express`) for API documentation

## Prerequisites

- [Node.js](https://nodejs.org/) 20.9 or later
- [npm](https://www.npmjs.com/)
- A Supabase project (local via [Supabase CLI](https://supabase.com/docs/guides/cli) or hosted on [supabase.com](https://supabase.com))

## Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env.local
```

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Your Supabase project URL (e.g. `http://127.0.0.1:54321` for local dev) |
| `SUPABASE_KEY` | Yes | Your Supabase anon/public API key |
| `PORT` | No | Port the app runs on (default: `3000`) |
| `NODE_ENV` | No | Environment mode (default: `development`) |

Example `.env.local` for local Supabase:

```env
NODE_ENV=development

SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_KEY=your_anon_key

PORT=3000
```

> **Note:** `.env.local` is gitignored. Never commit secrets to version control.

## Getting Started

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The API will be available at [http://localhost:3000](http://localhost:3000).

Other scripts:

```bash
npm run build   # Production build
npm run start   # Start production server
npm run lint    # Run ESLint
```

## Authentication

Protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Obtain an access token by calling `POST /auth/login` with valid credentials. The response includes `access_token` and `refresh_token`.

## API Reference

| Method | Endpoint | Auth Required | Description |
|--------|----------|:-------------:|-------------|
| `POST` | `/auth/signup` | No | Register a new user with email and password. Returns `201` with the user object. |
| `POST` | `/auth/login` | No | Authenticate and receive JWT tokens. Returns `200` with `access_token` and `refresh_token`. |
| `POST` | `/auth/logout` | Yes | Sign out the current session. Returns `204` with no body. |
| `GET` | `/public/info` | No | Public endpoint. Returns a welcome message. |
| `GET` | `/protected/profile` | Yes | Returns the authenticated user's profile (`id`, `email`, `created_at`). |
| `GET` | `/protected/dashboard` | Yes | Returns a personalized dashboard greeting. |
| `GET` | `/docs` | No | Swagger UI for interactive API exploration. |
| `GET` | `/openapi.json` | No | OpenAPI 3.0 specification. |

### Quick Examples

**Sign up:**

```bash
curl -X POST http://localhost:3000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

**Log in:**

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

**Access a protected route:**

```bash
curl http://localhost:3000/protected/profile \
  -H "Authorization: Bearer <access_token>"
```

## Swagger UI

Open [http://localhost:3000/docs](http://localhost:3000/docs) to explore and test all endpoints interactively.

Protected routes display a lock icon in Swagger UI. To test them:

1. Call `POST /auth/login` and copy the `access_token`.
2. Click **Authorize** and paste the token (without the `Bearer ` prefix).
3. Use **Try it out** on any protected endpoint.

## Project Structure

```
app/
  auth/
    signup/route.ts      # POST /auth/signup
    login/route.ts       # POST /auth/login
    logout/route.ts      # POST /auth/logout
  public/
    info/route.ts        # GET /public/info
  protected/
    profile/route.ts     # GET /protected/profile
    dashboard/route.ts   # GET /protected/dashboard
  docs/[[...path]]/      # Swagger UI at /docs
lib/
  supabase.ts            # Supabase client
  auth-middleware.ts     # Reusable Bearer token verification
openapi.json             # OpenAPI specification
```

## License

Private project.
