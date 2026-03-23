import { Match } from "@/data/mockData";
import { Clock, MapPin } from "lucide-react";

interface MatchCardProps {
  match: Match;
  compact?: boolean;
  children?: React.ReactNode;
}

export default function MatchCard({ match, compact, children }: MatchCardProps) {
  const statusColors = {
    upcoming: "bg-accent/20 text-accent-foreground",
    live: "bg-primary/10 text-primary",
    finished: "bg-muted text-muted-foreground",
  };
  const statusLabels = { upcoming: "Próximo", live: "🔴 En vivo", finished: "Finalizado" };

  return (
    <div className="glass-card hover-lift p-4 md:p-5">
      <div className="flex items-center justify-between mb-3">
        <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full ${statusColors[match.status]}`}>
          {statusLabels[match.status]}
        </span>
        <span className="text-[10px] text-muted-foreground font-medium">{match.phase} · {match.group}</span>
      </div>

      <div className="flex items-center justify-between gap-3">
        {/* Home */}
        <div className="flex-1 text-center">
          <div className="text-3xl mb-1">{match.homeFlag}</div>
          <p className="text-xs font-semibold truncate">{match.homeTeam}</p>
        </div>

        {/* Score / VS */}
        <div className="flex-shrink-0 text-center min-w-[70px]">
          {match.status === "upcoming" ? (
            <div className="text-lg font-heading font-bold text-muted-foreground">VS</div>
          ) : (
            <div className="flex items-center justify-center gap-2">
              <span className="text-2xl font-heading font-extrabold">{match.homeScore}</span>
              <span className="text-muted-foreground">-</span>
              <span className="text-2xl font-heading font-extrabold">{match.awayScore}</span>
            </div>
          )}
        </div>

        {/* Away */}
        <div className="flex-1 text-center">
          <div className="text-3xl mb-1">{match.awayFlag}</div>
          <p className="text-xs font-semibold truncate">{match.awayTeam}</p>
        </div>
      </div>

      {!compact && (
        <div className="flex items-center justify-center gap-4 mt-3 text-[10px] text-muted-foreground">
          <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{match.date} · {match.time}</span>
          <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{match.stadium}</span>
        </div>
      )}

      {children}
    </div>
  );
}
