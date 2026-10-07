import Link from "next/link";
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { SignOutButton } from "@/components/SignOutButton";

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: profile } = await supabase
    .from("profiles")
    .select("display_name, email")
    .eq("id", user.id)
    .maybeSingle();

  const { data: roleRows } = await supabase
    .from("user_roles")
    .select("roles(key, name)")
    .eq("user_id", user.id);

  const roles =
    roleRows
      ?.map((row) => {
        const r = row.roles as unknown as { key: string; name: string } | null;
        return r?.key;
      })
      .filter(Boolean) ?? [];

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 px-6 py-12">
      <div className="mx-auto max-w-3xl space-y-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-emerald-400">
              EvoOps
            </p>
            <h1 className="mt-2 text-3xl font-semibold">Dashboard</h1>
            <p className="mt-2 text-zinc-400">
              Signed in as {profile?.email || user.email}
            </p>
          </div>
          <SignOutButton />
        </div>

        <section className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-5">
          <h2 className="text-lg font-medium">Profile</h2>
          <p className="mt-2 text-sm text-zinc-300">
            Display name: {profile?.display_name || "—"}
          </p>
          <p className="mt-1 text-sm text-zinc-300">
            Roles: {roles.length ? roles.join(", ") : "none yet"}
          </p>
          {!roles.length ? (
            <p className="mt-3 text-sm text-amber-300">
              No roles assigned. If you are the first user, open Admin after
              claiming bootstrap admin, or ask an admin to grant a role.
            </p>
          ) : null}
        </section>

        <div className="flex flex-wrap gap-3">
          <Link
            href="/admin/roles"
            className="rounded-md border border-zinc-700 px-4 py-2 text-sm hover:border-emerald-500"
          >
            Admin · Roles
          </Link>
          <Link
            href="/"
            className="rounded-md border border-zinc-700 px-4 py-2 text-sm hover:border-zinc-500"
          >
            Home
          </Link>
        </div>
      </div>
    </main>
  );
}
