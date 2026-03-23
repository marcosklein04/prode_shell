import { useEffect, useState } from "react";

interface CountdownTimerProps {
  targetDate: string;
  label?: string;
}

export default function CountdownTimer({ targetDate, label = "Cierre de pronósticos" }: CountdownTimerProps) {
  const [timeLeft, setTimeLeft] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });

  useEffect(() => {
    const calculate = () => {
      const diff = new Date(targetDate).getTime() - Date.now();
      if (diff <= 0) return { days: 0, hours: 0, minutes: 0, seconds: 0 };
      return {
        days: Math.floor(diff / (1000 * 60 * 60 * 24)),
        hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((diff / (1000 * 60)) % 60),
        seconds: Math.floor((diff / 1000) % 60),
      };
    };
    setTimeLeft(calculate());
    const interval = setInterval(() => setTimeLeft(calculate()), 1000);
    return () => clearInterval(interval);
  }, [targetDate]);

  const units = [
    { value: timeLeft.days, label: "Días" },
    { value: timeLeft.hours, label: "Hrs" },
    { value: timeLeft.minutes, label: "Min" },
    { value: timeLeft.seconds, label: "Seg" },
  ];

  return (
    <div className="text-center">
      <p className="text-xs text-muted-foreground mb-2 uppercase tracking-wider font-medium">{label}</p>
      <div className="flex items-center gap-2 justify-center">
        {units.map((u, i) => (
          <div key={u.label} className="flex items-center gap-2">
            <div className="bg-shell-dark text-primary-foreground rounded-lg px-3 py-2 min-w-[48px]">
              <div className="text-xl font-heading font-bold leading-none">{String(u.value).padStart(2, "0")}</div>
              <div className="text-[9px] text-primary-foreground/60 uppercase mt-0.5">{u.label}</div>
            </div>
            {i < units.length - 1 && <span className="text-muted-foreground font-bold">:</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
