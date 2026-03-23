import { useState } from "react";
import AppLayout from "@/components/AppLayout";
import MatchCard from "@/components/MatchCard";
import { matches } from "@/data/mockData";

const phases = ["Todos", "Fase de Grupos"];
const statuses = ["Todos", "Próximo", "En vivo", "Finalizado"];
const statusMap: Record<string, string> = { "Próximo": "upcoming", "En vivo": "live", "Finalizado": "finished" };

export default function FixturePage() {
  const [phaseFilter, setPhaseFilter] = useState("Todos");
  const [statusFilter, setStatusFilter] = useState("Todos");

  const filtered = matches.filter((m) => {
    if (phaseFilter !== "Todos" && m.phase !== phaseFilter) return false;
    if (statusFilter !== "Todos" && m.status !== statusMap[statusFilter]) return false;
    return true;
  });

  // Group by date
  const grouped = filtered.reduce<Record<string, typeof matches>>((acc, m) => {
    (acc[m.date] = acc[m.date] || []).push(m);
    return acc;
  }, {});

  return (
    <AppLayout>
      <div className="py-4 space-y-6">
        <div className="animate-fade-in">
          <h1 className="font-heading text-2xl font-extrabold">Fixture</h1>
          <p className="text-sm text-muted-foreground mt-1">Calendario completo del Mundial 2026</p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-2 animate-fade-in delay-100">
          {statuses.map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                statusFilter === s
                  ? "gradient-shell text-primary-foreground"
                  : "bg-muted text-muted-foreground hover:bg-muted/80"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {/* Matches grouped by date */}
        <div className="space-y-6 animate-fade-in delay-200">
          {Object.entries(grouped).length === 0 ? (
            <div className="glass-card p-8 text-center text-muted-foreground">
              <p className="text-sm">No hay partidos con los filtros seleccionados</p>
            </div>
          ) : (
            Object.entries(grouped).sort(([a], [b]) => a.localeCompare(b)).map(([date, dateMatches]) => (
              <div key={date}>
                <h3 className="font-heading font-bold text-sm text-muted-foreground mb-3 uppercase tracking-wider">
                  📅 {new Date(date + "T12:00:00").toLocaleDateString("es-AR", { weekday: "long", day: "numeric", month: "long", year: "numeric" })}
                </h3>
                <div className="grid md:grid-cols-2 gap-3">
                  {dateMatches.map((m) => (
                    <MatchCard key={m.id} match={m} />
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </AppLayout>
  );
}
