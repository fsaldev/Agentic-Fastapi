"use client";

import * as React from "react";
import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";
import { Breadcrumb } from "@/components/layout/breadcrumb";

interface AppLayoutProps {
  children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  return (
    <div className="min-h-screen bg-background">
      <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />

      <div className="flex">
        {/* Desktop sidebar */}
        <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:bg-background">
          <Sidebar />
        </aside>

        {/* Mobile drawer overlay */}
        {sidebarOpen && (
          <div className="fixed inset-0 z-50 lg:hidden">
            <div
              className="fixed inset-0 bg-black/50"
              onClick={() => setSidebarOpen(false)}
              aria-hidden="true"
            />
            <aside className="fixed inset-y-0 left-0 z-50 w-64 border-r bg-background shadow-lg animate-in slide-in-from-left duration-200">
              <div className="flex h-14 items-center border-b px-4">
                <span className="text-lg font-semibold">Navigation</span>
              </div>
              <Sidebar onNavigate={() => setSidebarOpen(false)} />
            </aside>
          </div>
        )}

        {/* Main content */}
        <main className="flex-1 overflow-auto">
          <div className="px-4 py-4 lg:px-6">
            <Breadcrumb />
            <div className="mt-4">{children}</div>
          </div>
        </main>
      </div>
    </div>
  );
}
