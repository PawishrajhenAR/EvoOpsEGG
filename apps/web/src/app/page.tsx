import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-6 px-6 py-16">
        <p className="text-sm font-medium tracking-[0.2em] text-emerald-400 uppercase">
          EvoOps
        </p>
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
          Self-evolving AI operations
        </h1>
        <p className="max-w-xl text-lg text-zinc-400">
          Phase 1: sign in, claim bootstrap admin, and assign operator /
          approver / admin roles.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link
            className="rounded-md bg-emerald-500 px-4 py-2 text-sm font-medium text-zinc-950 hover:bg-emerald-400"
            href="/login"
          >
            Sign in
          </Link>
          <Link
            className="rounded-md border border-zinc-700 px-4 py-2 text-sm font-medium text-zinc-200 hover:border-zinc-500"
            href="/signup"
          >
            Create account
          </Link>
          <a
            className="rounded-md border border-zinc-700 px-4 py-2 text-sm font-medium text-zinc-200 hover:border-zinc-500"
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
          >
            API docs
          </a>
        </div>
      </div>
    </main>
  );
}
