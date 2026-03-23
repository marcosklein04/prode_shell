import { Link, useLocation } from "react-router-dom";
import { Trophy, Home, ClipboardList, BarChart3, User, Calendar, Menu, X, LogOut } from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const navItems = [
  { to: "/dashboard", label: "Inicio", icon: Home },
  { to: "/pronosticos", label: "Pronósticos", icon: ClipboardList },
  { to: "/ranking", label: "Ranking", icon: Trophy },
  { to: "/fixture", label: "Fixture", icon: Calendar },
  { to: "/perfil", label: "Mi Perfil", icon: User },
];

export default function AppNavbar() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Desktop navbar */}
      <nav className="hidden md:flex fixed top-0 left-0 right-0 z-50 h-16 items-center justify-between px-6 bg-card/90 backdrop-blur-lg border-b border-border">
        <Link to="/dashboard" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg gradient-shell flex items-center justify-center">
            <Trophy className="w-4 h-4 text-primary-foreground" />
          </div>
          <span className="font-heading font-extrabold text-lg tracking-tight">
            <span className="text-primary">Prode</span>{" "}
            <span className="text-foreground">Mundial</span>
          </span>
        </Link>

        <div className="flex items-center gap-1">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`nav-link flex items-center gap-2 rounded-lg ${
                location.pathname === item.to ? "active bg-muted" : ""
              }`}
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </Link>
          ))}
        </div>

        <Link to="/" className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors">
          <LogOut className="w-4 h-4" />
          Salir
        </Link>
      </nav>

      {/* Mobile bottom nav */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-card/95 backdrop-blur-lg border-t border-border safe-area-bottom">
        <div className="flex items-center justify-around py-2 px-2">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`flex flex-col items-center gap-0.5 px-3 py-1.5 rounded-xl transition-colors ${
                location.pathname === item.to
                  ? "text-primary"
                  : "text-muted-foreground"
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="text-[10px] font-medium">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* Mobile top bar */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-50 h-14 flex items-center justify-between px-4 bg-card/90 backdrop-blur-lg border-b border-border">
        <Link to="/dashboard" className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg gradient-shell flex items-center justify-center">
            <Trophy className="w-3.5 h-3.5 text-primary-foreground" />
          </div>
          <span className="font-heading font-extrabold text-base">
            <span className="text-primary">Prode</span> <span className="text-foreground">Mundial</span>
          </span>
        </Link>
        <Link to="/" className="text-muted-foreground">
          <LogOut className="w-5 h-5" />
        </Link>
      </div>
    </>
  );
}
