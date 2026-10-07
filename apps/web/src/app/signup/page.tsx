"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setMessage(null);
    const supabase = createClient();
    const { data, error: err } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { display_name: displayName || undefined } },
    });
    setLoading(false);
    if (err) {
      setError(err.message);
      return;
    }

    if (data.session) {
      // First user can claim admin when no admins exist yet
      await supabase.rpc("claim_bootstrap_admin");
      router.push("/dashboard");
      router.refresh();
      return;
    }

    setMessage(
      "Check your email to confirm signup (or disable email confirm in Supabase Auth settings for local dev).",
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 flex items-center justify-center px-4">
      <form
        onSubmit={onSubmit}
        className="w-full max-w-md space-y-4 rounded-xl border border-zinc-800 bg-zinc-900/60 p-8"
      >
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-emerald-400">
            EvoOps
          </p>
          <h1 className="mt-2 text-2xl font-semibold">Create account</h1>
        </div>
        <label className="block text-sm">
          Display name
          <input
            className="mt-1 w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          Email
          <input
            className="mt-1 w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          Password
          <input
            className="mt-1 w-full rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2"
            type="password"
            required
            minLength={6}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error ? <p className="text-sm text-red-400">{error}</p> : null}
        {message ? <p className="text-sm text-emerald-300">{message}</p> : null}
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-emerald-500 py-2 text-sm font-medium text-zinc-950 hover:bg-emerald-400 disabled:opacity-60"
        >
          {loading ? "Creating…" : "Sign up"}
        </button>
        <p className="text-sm text-zinc-400">
          Already have an account?{" "}
          <Link className="text-emerald-400 hover:underline" href="/login">
            Sign in
          </Link>
        </p>
      </form>
    </main>
  );
}
