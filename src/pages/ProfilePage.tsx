import AppLayout from "@/components/AppLayout";
import StatsCard from "@/components/StatsCard";
import { currentUser, userPredictions } from "@/data/mockData";
import { Trophy, Target, Zap, Hash, TrendingUp, Award, Check, X } from "lucide-react";

export default function ProfilePage() {
  return (
    <AppLayout>
      <div className="py-4 space-y-6">
        {/* Header */}
        <div className="glass-card p-6 flex flex-col md:flex-row items-center gap-5 animate-fade-in">
          <div className="w-20 h-20 rounded-2xl gradient-shell flex items-center justify-center text-2xl font-heading font-extrabold text-primary-foreground glow-red">
            {currentUser.name.split(" ").map(n => n[0]).join("")}
          </div>
          <div className="text-center md:text-left">
            <h1 className="font-heading text-2xl font-extrabold">{currentUser.name}</h1>
            <p className="text-muted-foreground text-sm">Shell Argentina · Participante activo</p>
            <div className="flex items-center justify-center md:justify-start gap-3 mt-2">
              <span className="badge-gold flex items-center gap-1"><Trophy className="w-3 h-3" /> #{currentUser.rank}</span>
              <span className="text-sm font-heading font-bold">{currentUser.points} puntos</span>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 animate-fade-in delay-100">
          <StatsCard icon={<Target className="w-5 h-5" />} label="Aciertos" value={currentUser.correctPredictions} sub={`de ${currentUser.totalPredictions}`} accent />
          <StatsCard icon={<Hash className="w-5 h-5" />} label="Exactos" value={currentUser.exactScores} sub="Resultados exactos" />
          <StatsCard icon={<Zap className="w-5 h-5" />} label="Efectividad" value={`${currentUser.effectiveness}%`} />
          <StatsCard icon={<TrendingUp className="w-5 h-5" />} label="Racha" value={`${currentUser.streak}`} sub="Aciertos seguidos" />
          <StatsCard icon={<Trophy className="w-5 h-5" />} label="Posición" value={`#${currentUser.rank}`} sub={`de ${12} jugadores`} />
          <StatsCard icon={<Award className="w-5 h-5" />} label="Puntos" value={currentUser.points} accent />
        </div>

        {/* Effectiveness bar */}
        <div className="glass-card p-5 animate-fade-in delay-200">
          <h3 className="font-heading font-bold text-sm mb-3">Progreso general</h3>
          <div className="w-full h-4 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full gradient-shell rounded-full transition-all duration-1000"
              style={{ width: `${currentUser.effectiveness}%` }}
            />
          </div>
          <div className="flex justify-between mt-2 text-[10px] text-muted-foreground">
            <span>0%</span>
            <span className="font-bold text-primary">{currentUser.effectiveness}% efectividad</span>
            <span>100%</span>
          </div>
        </div>

        {/* History */}
        <div className="animate-fade-in delay-300">
          <h2 className="font-heading font-bold text-base mb-3">Historial de pronósticos</h2>
          <div className="glass-card overflow-hidden">
            {userPredictions.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground">
                <Target className="w-10 h-10 mx-auto mb-3 opacity-40" />
                <p className="text-sm">Aún no hay pronósticos finalizados</p>
              </div>
            ) : (
              userPredictions.map((p) => {
                const correct = p.homeScore === p.match.homeScore && p.awayScore === p.match.awayScore;
                return (
                  <div key={p.matchId} className="flex items-center gap-3 px-4 py-3 border-b border-border/30 last:border-0">
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${correct ? "bg-emerald-100 text-emerald-600" : "bg-destructive/10 text-destructive"}`}>
                      {correct ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {p.match.homeFlag} {p.match.homeTeam} vs {p.match.awayTeam} {p.match.awayFlag}
                      </p>
                      <p className="text-[10px] text-muted-foreground">
                        Real: {p.match.homeScore}-{p.match.awayScore} · Tu pronóstico: {p.homeScore}-{p.awayScore}
                      </p>
                    </div>
                    <span className={`text-xs font-bold ${correct ? "text-emerald-600" : "text-destructive"}`}>
                      {correct ? "+3 pts" : "+0"}
                    </span>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
