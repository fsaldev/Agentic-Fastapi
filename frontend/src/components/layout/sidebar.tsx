"use client";

import { LayoutDashboard, Car, Users, Calendar } from "lucide-react";
import { NavItem } from "@/components/layout/nav-item";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Cars", href: "/cars", icon: Car },
  { name: "Customers", href: "/customers", icon: Users },
  { name: "Bookings", href: "/bookings", icon: Calendar },
];

interface SidebarProps {
  onNavigate?: () => void;
}

export function Sidebar({ onNavigate }: SidebarProps) {
  return (
    <nav className="flex flex-col gap-1 px-3 py-4" aria-label="Main navigation">
      {navigation.map((item) => (
        <NavItem
          key={item.href}
          href={item.href}
          label={item.name}
          icon={item.icon}
          onClick={onNavigate}
        />
      ))}
    </nav>
  );
}
