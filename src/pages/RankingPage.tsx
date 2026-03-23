import AppLayout from "@/components/AppLayout";
import { rankings } from "@/data/mockData";
import { Trophy, Medal, Crown, ChevronUp, ChevronDown, Minus } from "lucide-react";
import { useState } from "react";

export default function RankingPage() {
  const [showAll, setShowAll] = useState(false);
  const displayed = showAll ? rankings : rankings.slice(0, 10);

  const getPodiumIcon = (pos: number) => {
    if (pos === 1) return <Crown className="w-5 h-5 text-accent" />;
    if (pos === 2) return <Medal className="w-5 h-5 text-muted-foreground" />;
    if (pos === 3) return <Medal className="w-5 h-5 text-orange-500" />;
    return null;
  };

  return (
    <AppLayout>
      <div className="py-4 space-y-6">
        <div className="animate-fade-in">
          <h1 className="font-heading text-2xl font-extrabold">Ranking General</h1>
          <p className="text-sm text-muted-foreground mt-1">Clasificación actualizada de todos los participantes</p>
        </div>

        {/* Podium */}
        <div className="grid grid-cols-3 gap-3 animate-fade-in delay-100">
          {rankings.slice(0, 3).map((r, i) => {
            const order = [1, 0, 2];
            const user = rankings[order[i]];
            const heights = ["h-32", "h-40", "h-28"];
            const badges = ["badge-silver", "badge-gold", "badge-bronze"];
            return (
              <div key={user.position} className="flex flex-col items-center">
                <div className={`w-14 h-14 md:w-16 md:h-16 rounded-full gradient-shell flex items-center justify-center text-lg font-bold text-primary-foreground mb-2 ${order[i] === 0 ? "ring-4 ring-accent/50 glow-yellow" : ""}`}>
                  {user.avatar}
                </div>
                <p className="text-xs font-semibold text-center truncate max-w-full">{user.name}</p>
                <p className="text-[10px] text-muted-foreground">{user.points} pts</p>
                <div className={`mt-2 w-full ${heights[i]} rounded-t-xl flex items-start justify-center pt-3 ${order[i] === 0 ? "gradient-shell" : "bg-muted"}`}>
                  <span className={`text-2xl font-heading font-extrabold ${order[i] === 0 ? "text-primary-foreground" : "text-muted-foreground"}`}>
                    #{user.position}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Table */}
        <div className="glass-card overflow-hidden animate-fade-in delay-200">
          <div className="px-4 py-3 border-b border-border/50 bg-muted/50">
            <div className="grid grid-cols-12 text-[10px] uppercase tracking-wider font-semibold text-muted-foreground">
              <span className="col-span-1">#</span>
              <span className="col-span-5">Jugador</span>
              <span className="col-span-2 text-center">Aciertos</span>
              <span className="col-span-2 text-center">Total</span>
              <span className="col-span-2 text-right">Puntos</span>
            </div>
          </div>
          {displayed.map((r) => (
            <div
              key={r.position}
              className={`grid grid-cols-12 items-center px-4 py-3 border-b border-border/30 last:border-0 transition-colors hover:bg-muted/30 ${
                r.isCurrentUser ? "bg-primary/5 border-l-2 border-l-primary" : ""
              }`}
            >
              <span className="col-span-1">
                {r.position <= 3 ? (
                  <span className={`${r.position === 1 ? "badge-gold" : r.position === 2 ? "badge-silver" : "badge-bronze"} !px-2 !py-0.5`}>
                    {r.position}
                  </span>
                ) : (
                  <span className="text-sm font-bold text-muted-foreground">{r.position}</span>
                )}
              </span>
              <div className="col-span-5 flex items-center gap-2">
                <div className="w-8 h-8 rounded-full gradient-shell flex items-center justify-center text-[10px] font-bold text-primary-foreground flex-shrink-0">
                  {r.avatar}
                </div>
                <span className={`text-sm font-medium truncate ${r.isCurrentUser ? "text-primary font-bold" : ""}`}>
                  {r.name} {r.isCurrentUser && <span className="text-[10px]">(Tú)</span>}
                </span>
              </div>
              <span className="col-span-2 text-center text-sm">{r.correctPredictions}</span>
              <span className="col-span-2 text-center text-sm text-muted-foreground">{r.totalPredictions}</span>
              <span className="col-span-2 text-right font-heading font-bold text-sm">{r.points}</span>
            </div>
          ))}
        </div>

        {rankings.length > 10 && (
          <div className="text-center">
            <button onClick={() => setShowAll(!showAll)} className="text-sm text-primary font-semibold hover:underline">
              {showAll ? "Ver menos" : `Ver todos (${rankings.length})`}
            </button>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
