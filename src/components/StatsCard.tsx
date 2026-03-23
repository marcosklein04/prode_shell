import { ReactNode } from "react";

interface StatsCardProps {
  icon: ReactNode;
  label: string;
  value: string | number;
  sub?: string;
  accent?: boolean;
}

export default function StatsCard({ icon, label, value, sub, accent }: StatsCardProps) {
  return (
    <div className={`glass-card hover-lift p-4 ${accent ? "border-primary/30" : ""}`}>
      <div className="flex items-center gap-3">
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${accent ? "gradient-shell text-primary-foreground" : "bg-muted text-muted-foreground"}`}>
          {icon}
        </div>
        <div className="min-w-0">
          <p className="text-[11px] text-muted-foreground uppercase tracking-wider font-medium">{label}</p>
          <p className="text-xl font-heading font-extrabold leading-tight">{value}</p>
          {sub && <p className="text-[10px] text-muted-foreground">{sub}</p>}
        </div>
      </div>
    </div>
  );
}
