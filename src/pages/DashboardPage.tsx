import AppLayout from "@/components/AppLayout";
import StatsCard from "@/components/StatsCard";
import MatchCard from "@/components/MatchCard";
import CountdownTimer from "@/components/CountdownTimer";
import { matches, currentUser, rankings } from "@/data/mockData";
import { Trophy, Target, Zap, TrendingUp, ArrowRight, Megaphone } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  const upcomingMatches = matches.filter((m) => m.status === "upcoming").slice(0, 3);
  const liveMatch = matches.find((m) => m.status === "live");
  const nextMatch = upcomingMatches[0];

  return (
    <AppLayout>
      <div className="space-y-6 py-4">
        {/* Welcome banner */}
        <div className="gradient-shell rounded-2xl p-6 md:p-8 text-primary-foreground relative overflow-hidden animate-fade-in">
          <div className="absolute right-0 top-0 w-40 h-40 bg-primary-foreground/5 rounded-full -translate-y-1/2 translate-x-1/4" />
          <div className="absolute right-16 bottom-0 w-24 h-24 bg-primary-foreground/5 rounded-full translate-y-1/2" />
          <div className="relative z-10">
            <p className="text-sm text-primary-foreground/70 font-medium">¡Hola, {currentUser.name}! 👋</p>
            <h1 className="font-heading text-2xl md:text-3xl font-extrabold mt-1 mb-3">
              Prode Mundial Shell 2026
            </h1>
            <p className="text-primary-foreground/80 text-sm max-w-lg mb-5">
              Estás en la posición <strong>#{currentUser.rank}</strong> del ranking general. ¡Seguí pronosticando para escalar posiciones!
            </p>
            <Link to="/pronosticos">
              <Button className="bg-primary-foreground/20 hover:bg-primary-foreground/30 text-primary-foreground border-0 rounded-xl font-heading font-bold backdrop-blur-sm">
                Pronosticar ahora <ArrowRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 animate-fade-in delay-100">
          <StatsCard icon={<Trophy className="w-5 h-5" />} label="Puntos" value={currentUser.points} sub={`Puesto #${currentUser.rank}`} accent />
          <StatsCard icon={<Target className="w-5 h-5" />} label="Aciertos" value={currentUser.correctPredictions} sub={`de ${currentUser.totalPredictions}`} />
          <StatsCard icon={<Zap className="w-5 h-5" />} label="Efectividad" value={`${currentUser.effectiveness}%`} />
          <StatsCard icon={<TrendingUp className="w-5 h-5" />} label="Racha" value={`${currentUser.streak} ✓`} sub="Aciertos seguidos" />
        </div>

        {/* Live match */}
        {liveMatch && (
          <div className="animate-fade-in delay-200">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
              <h2 className="font-heading font-bold text-sm uppercase tracking-wider text-primary">En vivo ahora</h2>
            </div>
            <MatchCard match={liveMatch} />
          </div>
        )}

        {/* Countdown + Quick actions */}
        <div className="grid md:grid-cols-2 gap-4 animate-fade-in delay-300">
          {nextMatch && (
            <div className="glass-card p-5">
              <CountdownTimer targetDate={nextMatch.date + "T" + nextMatch.time} label="Próximo cierre de pronósticos" />
              <div className="text-center mt-3">
                <p className="text-xs text-muted-foreground">
                  {nextMatch.homeTeam} {nextMatch.homeFlag} vs {nextMatch.awayFlag} {nextMatch.awayTeam}
                </p>
              </div>
            </div>
          )}

          <div className="glass-card p-5 flex flex-col items-center justify-center gap-3 text-center">
            <Megaphone className="w-8 h-8 text-accent" />
            <div>
              <h3 className="font-heading font-bold text-sm">Noticias & Destacados</h3>
              <p className="text-xs text-muted-foreground mt-1">
                🏆 ¡Nuevo premio para el Top 3! Consultá las bases y condiciones en el portal interno.
              </p>
            </div>
          </div>
        </div>

        {/* Upcoming matches */}
        <div className="animate-fade-in delay-400">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-heading font-bold text-base">Próximos partidos</h2>
            <Link to="/fixture" className="text-xs text-primary font-semibold hover:underline flex items-center gap-1">
              Ver todos <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="grid md:grid-cols-3 gap-3">
            {upcomingMatches.map((m) => (
              <MatchCard key={m.id} match={m} compact />
            ))}
          </div>
        </div>

        {/* Quick ranking preview */}
        <div className="animate-fade-in delay-500">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-heading font-bold text-base">Top 5 Ranking</h2>
            <Link to="/ranking" className="text-xs text-primary font-semibold hover:underline flex items-center gap-1">
              Ver completo <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="glass-card overflow-hidden">
            {rankings.slice(0, 5).map((r) => (
              <div key={r.position} className={`flex items-center gap-3 px-4 py-3 border-b border-border/50 last:border-0 ${r.isCurrentUser ? "bg-primary/5" : ""}`}>
                <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                  r.position === 1 ? "badge-gold" : r.position === 2 ? "badge-silver" : r.position === 3 ? "badge-bronze" : "bg-muted text-muted-foreground"
                }`}>
                  {r.position}
                </span>
                <div className="w-8 h-8 rounded-full gradient-shell flex items-center justify-center text-xs font-bold text-primary-foreground">
                  {r.avatar}
                </div>
                <span className={`flex-1 text-sm font-medium ${r.isCurrentUser ? "text-primary font-bold" : ""}`}>
                  {r.name} {r.isCurrentUser && <span className="text-[10px] text-primary">(Tú)</span>}
                </span>
                <span className="font-heading font-bold text-sm">{r.points} pts</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
