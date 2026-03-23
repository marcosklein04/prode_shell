import { useState } from "react";
import AppLayout from "@/components/AppLayout";
import MatchCard from "@/components/MatchCard";
import { matches } from "@/data/mockData";
import { Button } from "@/components/ui/button";
import { Check, Clock, Lock } from "lucide-react";
import { toast } from "sonner";

interface PredictionState {
  [matchId: string]: { home: string; away: string; saved: boolean };
}

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<PredictionState>({});
  const upcomingMatches = matches.filter((m) => m.status === "upcoming");
  const closedMatches = matches.filter((m) => m.status !== "upcoming");

  const updatePrediction = (matchId: string, side: "home" | "away", value: string) => {
    if (!/^\d{0,2}$/.test(value)) return;
    setPredictions((prev) => ({
      ...prev,
      [matchId]: { ...prev[matchId], [side]: value, saved: false },
    }));
  };

  const savePrediction = (matchId: string) => {
    const p = predictions[matchId];
    if (!p || p.home === "" || p.away === "" || p.home === undefined || p.away === undefined) {
      toast.error("Completá ambos resultados");
      return;
    }
    setPredictions((prev) => ({ ...prev, [matchId]: { ...prev[matchId], saved: true } }));
    toast.success("¡Pronóstico guardado!");
  };

  return (
    <AppLayout>
      <div className="py-4 space-y-6">
        <div className="animate-fade-in">
          <h1 className="font-heading text-2xl font-extrabold">Mis Pronósticos</h1>
          <p className="text-sm text-muted-foreground mt-1">Ingresá tus resultados antes del cierre de cada partido</p>
        </div>

        {/* Upcoming - pronosticables */}
        <div className="space-y-4 animate-fade-in delay-100">
          <h2 className="font-heading font-bold text-sm uppercase tracking-wider text-primary flex items-center gap-2">
            <Clock className="w-4 h-4" /> Partidos abiertos ({upcomingMatches.length})
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {upcomingMatches.map((match) => {
              const p = predictions[match.id];
              return (
                <MatchCard key={match.id} match={match}>
                  <div className="mt-4 pt-4 border-t border-border/50">
                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-medium text-center mb-3">Tu pronóstico</p>
                    <div className="flex items-center justify-center gap-3">
                      <div className="text-center">
                        <p className="text-[10px] text-muted-foreground mb-1">{match.homeTeam}</p>
                        <input
                          type="text"
                          inputMode="numeric"
                          maxLength={2}
                          value={p?.home ?? ""}
                          onChange={(e) => updatePrediction(match.id, "home", e.target.value)}
                          className="w-14 h-14 text-center text-2xl font-heading font-extrabold rounded-xl bg-muted border-2 border-border focus:border-primary outline-none transition-colors"
                        />
                      </div>
                      <span className="text-muted-foreground font-bold text-lg mt-4">-</span>
                      <div className="text-center">
                        <p className="text-[10px] text-muted-foreground mb-1">{match.awayTeam}</p>
                        <input
                          type="text"
                          inputMode="numeric"
                          maxLength={2}
                          value={p?.away ?? ""}
                          onChange={(e) => updatePrediction(match.id, "away", e.target.value)}
                          className="w-14 h-14 text-center text-2xl font-heading font-extrabold rounded-xl bg-muted border-2 border-border focus:border-primary outline-none transition-colors"
                        />
                      </div>
                    </div>
                    <div className="mt-3 flex justify-center">
                      {p?.saved ? (
                        <div className="flex items-center gap-1.5 text-sm font-medium text-emerald-600">
                          <Check className="w-4 h-4" /> Guardado
                        </div>
                      ) : (
                        <Button onClick={() => savePrediction(match.id)} className="gradient-shell text-primary-foreground border-0 rounded-xl font-heading font-bold text-xs h-9 px-6">
                          Guardar pronóstico
                        </Button>
                      )}
                    </div>
                  </div>
                </MatchCard>
              );
            })}
          </div>
        </div>

        {/* Closed matches */}
        {closedMatches.length > 0 && (
          <div className="space-y-4 animate-fade-in delay-200">
            <h2 className="font-heading font-bold text-sm uppercase tracking-wider text-muted-foreground flex items-center gap-2">
              <Lock className="w-4 h-4" /> Partidos cerrados ({closedMatches.length})
            </h2>
            <div className="grid md:grid-cols-2 gap-4 opacity-70">
              {closedMatches.map((match) => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
