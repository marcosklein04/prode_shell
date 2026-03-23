import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Eye, EyeOff, Trophy, Mail, Lock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import loginBg from "@/assets/login-bg.jpg";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigate("/dashboard");
    }, 1200);
  };

  return (
    <div className="min-h-screen flex">
      {/* Left - Image */}
      <div className="hidden lg:flex flex-1 relative overflow-hidden">
        <img src={loginBg} alt="Mundial" className="absolute inset-0 w-full h-full object-cover" width={1920} height={1080} />
        <div className="absolute inset-0 bg-gradient-to-r from-shell-dark/90 via-shell-dark/70 to-transparent" />
        <div className="relative z-10 flex flex-col justify-end p-12">
          <div className="animate-fade-in">
            <h2 className="text-5xl font-heading font-extrabold text-primary-foreground leading-tight mb-4">
              Viví la emoción<br />del <span className="text-gradient-shell">Mundial</span>
            </h2>
            <p className="text-primary-foreground/70 text-lg max-w-md">
              Demostrá que sabés de fútbol. Pronosticá, competí con tus compañeros y ganá premios increíbles.
            </p>
          </div>
        </div>
      </div>

      {/* Right - Form */}
      <div className="flex-1 lg:max-w-xl flex flex-col justify-center px-6 md:px-16 py-12 bg-background relative">
        {/* Mobile bg */}
        <div className="lg:hidden absolute inset-0 -z-10">
          <img src={loginBg} alt="" className="w-full h-full object-cover opacity-10" />
        </div>

        <div className="w-full max-w-sm mx-auto animate-fade-in">
          {/* Logo */}
          <div className="flex items-center gap-3 mb-10">
            <div className="w-12 h-12 rounded-2xl gradient-shell flex items-center justify-center glow-red">
              <Trophy className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-heading font-extrabold text-2xl leading-tight">
                <span className="text-primary">Prode</span> Mundial
              </h1>
              <p className="text-xs text-muted-foreground font-medium">by Shell Argentina</p>
            </div>
          </div>

          <h2 className="font-heading text-xl font-bold mb-1">¡Bienvenido!</h2>
          <p className="text-sm text-muted-foreground mb-8">Ingresá con tu cuenta para comenzar a jugar</p>

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1.5 block">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  type="email"
                  placeholder="tu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10 h-12 rounded-xl"
                  required
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1.5 block">Contraseña</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 pr-10 h-12 rounded-xl"
                  required
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" checked={remember} onChange={() => setRemember(!remember)} className="rounded border-border accent-primary w-4 h-4" />
                <span className="text-sm text-muted-foreground">Recordarme</span>
              </label>
              <button type="button" className="text-sm text-primary hover:underline font-medium">¿Olvidaste tu contraseña?</button>
            </div>

            <Button type="submit" disabled={loading} className="w-full h-12 rounded-xl gradient-shell text-primary-foreground font-heading font-bold text-base hover:opacity-90 transition-opacity border-0">
              {loading ? (
                <div className="w-5 h-5 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
              ) : (
                "Ingresar"
              )}
            </Button>
          </form>

          <p className="text-center text-xs text-muted-foreground mt-8">
            ¿No tenés cuenta?{" "}
            <button className="text-primary font-semibold hover:underline">Solicitá acceso</button>
          </p>
        </div>
      </div>
    </div>
  );
}
