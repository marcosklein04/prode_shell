import { ReactNode } from "react";
import AppNavbar from "./AppNavbar";

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <AppNavbar />
      <main className="pt-16 pb-20 md:pb-8 px-4 md:px-6 max-w-7xl mx-auto">
        {children}
      </main>
    </div>
  );
}
