export interface Match {
  id: string;
  homeTeam: string;
  awayTeam: string;
  homeFlag: string;
  awayFlag: string;
  date: string;
  time: string;
  group: string;
  phase: string;
  status: "upcoming" | "live" | "finished";
  homeScore?: number;
  awayScore?: number;
  stadium: string;
}

export interface Prediction {
  matchId: string;
  homeScore: number | null;
  awayScore: number | null;
  saved: boolean;
}

export interface UserRanking {
  position: number;
  name: string;
  avatar: string;
  points: number;
  correctPredictions: number;
  totalPredictions: number;
  isCurrentUser?: boolean;
}

export interface UserStats {
  name: string;
  points: number;
  rank: number;
  totalPredictions: number;
  correctPredictions: number;
  exactScores: number;
  effectiveness: number;
  streak: number;
}

const flags: Record<string, string> = {
  "Argentina": "🇦🇷",
  "Brasil": "🇧🇷",
  "Alemania": "🇩🇪",
  "Francia": "🇫🇷",
  "España": "🇪🇸",
  "Inglaterra": "🇬🇧",
  "Portugal": "🇵🇹",
  "Países Bajos": "🇳🇱",
  "Italia": "🇮🇹",
  "Uruguay": "🇺🇾",
  "México": "🇲🇽",
  "Colombia": "🇨🇴",
  "Japón": "🇯🇵",
  "Corea del Sur": "🇰🇷",
  "Australia": "🇦🇺",
  "Arabia Saudita": "🇸🇦",
  "Canadá": "🇨🇦",
  "Estados Unidos": "🇺🇸",
  "Marruecos": "🇲🇦",
  "Senegal": "🇸🇳",
  "Qatar": "🇶🇦",
  "Croacia": "🇭🇷",
  "Dinamarca": "🇩🇰",
  "Suiza": "🇨🇭",
};

export const matches: Match[] = [
  { id: "m1", homeTeam: "Argentina", awayTeam: "Arabia Saudita", homeFlag: flags["Argentina"], awayFlag: flags["Arabia Saudita"], date: "2026-06-11", time: "13:00", group: "A", phase: "Fase de Grupos", status: "upcoming", stadium: "Estadio Lusail" },
  { id: "m2", homeTeam: "Francia", awayTeam: "Australia", homeFlag: flags["Francia"], awayFlag: flags["Australia"], date: "2026-06-11", time: "16:00", group: "D", phase: "Fase de Grupos", status: "upcoming", stadium: "Al Janoub Stadium" },
  { id: "m3", homeTeam: "España", awayTeam: "Japón", homeFlag: flags["España"], awayFlag: flags["Japón"], date: "2026-06-12", time: "10:00", group: "E", phase: "Fase de Grupos", status: "upcoming", stadium: "Khalifa International" },
  { id: "m4", homeTeam: "Brasil", awayTeam: "Croacia", homeFlag: flags["Brasil"], awayFlag: flags["Croacia"], date: "2026-06-12", time: "13:00", group: "G", phase: "Fase de Grupos", status: "upcoming", stadium: "Estadio Lusail" },
  { id: "m5", homeTeam: "Inglaterra", awayTeam: "Estados Unidos", homeFlag: flags["Inglaterra"], awayFlag: flags["Estados Unidos"], date: "2026-06-12", time: "19:00", group: "B", phase: "Fase de Grupos", status: "upcoming", stadium: "Al Bayt Stadium" },
  { id: "m6", homeTeam: "Alemania", awayTeam: "México", homeFlag: flags["Alemania"], awayFlag: flags["México"], date: "2026-06-13", time: "13:00", group: "F", phase: "Fase de Grupos", status: "upcoming", stadium: "Education City" },
  { id: "m7", homeTeam: "Portugal", awayTeam: "Uruguay", homeFlag: flags["Portugal"], awayFlag: flags["Uruguay"], date: "2026-06-13", time: "16:00", group: "H", phase: "Fase de Grupos", status: "upcoming", stadium: "Stadium 974" },
  { id: "m8", homeTeam: "Países Bajos", awayTeam: "Senegal", homeFlag: flags["Países Bajos"], awayFlag: flags["Senegal"], date: "2026-06-13", time: "19:00", group: "A", phase: "Fase de Grupos", status: "upcoming", stadium: "Al Thumama" },
  { id: "m9", homeTeam: "Colombia", awayTeam: "Corea del Sur", homeFlag: flags["Colombia"], awayFlag: flags["Corea del Sur"], date: "2026-06-14", time: "10:00", group: "C", phase: "Fase de Grupos", status: "finished", homeScore: 2, awayScore: 0, stadium: "Al Rayyan" },
  { id: "m10", homeTeam: "Dinamarca", awayTeam: "Suiza", homeFlag: flags["Dinamarca"], awayFlag: flags["Suiza"], date: "2026-06-14", time: "16:00", group: "D", phase: "Fase de Grupos", status: "finished", homeScore: 1, awayScore: 1, stadium: "Ahmed bin Ali" },
  { id: "m11", homeTeam: "Italia", awayTeam: "Canadá", homeFlag: flags["Italia"], awayFlag: flags["Canadá"], date: "2026-06-15", time: "13:00", group: "F", phase: "Fase de Grupos", status: "finished", homeScore: 3, awayScore: 1, stadium: "Al Janoub" },
  { id: "m12", homeTeam: "Marruecos", awayTeam: "Qatar", homeFlag: flags["Marruecos"], awayFlag: flags["Qatar"], date: "2026-06-15", time: "19:00", group: "C", phase: "Fase de Grupos", status: "live", homeScore: 1, awayScore: 0, stadium: "Education City" },
];

export const rankings: UserRanking[] = [
  { position: 1, name: "Carlos Méndez", avatar: "CM", points: 48, correctPredictions: 16, totalPredictions: 20 },
  { position: 2, name: "María García", avatar: "MG", points: 45, correctPredictions: 15, totalPredictions: 20 },
  { position: 3, name: "Lucas Fernández", avatar: "LF", points: 42, correctPredictions: 14, totalPredictions: 20 },
  { position: 4, name: "Ana Rodríguez", avatar: "AR", points: 39, correctPredictions: 13, totalPredictions: 20 },
  { position: 5, name: "Juan Martínez", avatar: "JM", points: 36, correctPredictions: 12, totalPredictions: 20, isCurrentUser: true },
  { position: 6, name: "Laura Pérez", avatar: "LP", points: 33, correctPredictions: 11, totalPredictions: 20 },
  { position: 7, name: "Diego López", avatar: "DL", points: 30, correctPredictions: 10, totalPredictions: 20 },
  { position: 8, name: "Valentina Sosa", avatar: "VS", points: 27, correctPredictions: 9, totalPredictions: 20 },
  { position: 9, name: "Martín Díaz", avatar: "MD", points: 24, correctPredictions: 8, totalPredictions: 20 },
  { position: 10, name: "Sofía Torres", avatar: "ST", points: 21, correctPredictions: 7, totalPredictions: 20 },
  { position: 11, name: "Pablo Ruiz", avatar: "PR", points: 18, correctPredictions: 6, totalPredictions: 20 },
  { position: 12, name: "Camila Herrera", avatar: "CH", points: 15, correctPredictions: 5, totalPredictions: 20 },
];

export const currentUser: UserStats = {
  name: "Juan Martínez",
  points: 36,
  rank: 5,
  totalPredictions: 20,
  correctPredictions: 12,
  exactScores: 4,
  effectiveness: 60,
  streak: 3,
};

export const userPredictions: (Prediction & { match: Match })[] = matches.filter(m => m.status === "finished").map(m => ({
  matchId: m.id,
  homeScore: m.homeScore !== undefined ? m.homeScore + (Math.random() > 0.5 ? 0 : 1) : null,
  awayScore: m.awayScore !== undefined ? m.awayScore + (Math.random() > 0.6 ? 0 : -1) : null,
  saved: true,
  match: m,
}));
