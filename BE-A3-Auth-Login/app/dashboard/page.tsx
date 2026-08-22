import { DashboardPage } from "../components/dashboard-page";

/** /dashboard route — auth logic lives in the client component. */
export default function Dashboard() {
  return (
    <div className="flex min-h-full flex-1 flex-col bg-zinc-50 font-sans dark:bg-black">
      <DashboardPage />
    </div>
  );
}
