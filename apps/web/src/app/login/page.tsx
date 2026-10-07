import { Suspense } from "react";
import { LoginForm } from "./LoginForm";

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <main className="min-h-screen bg-zinc-950 text-zinc-400 flex items-center justify-center">
          Loading…
        </main>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
