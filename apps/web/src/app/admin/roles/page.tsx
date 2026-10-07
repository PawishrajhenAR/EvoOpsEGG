"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

type ProfileRow = {
  id: string;
  email: string;
  display_name: string;
  roles: string[];
};

const ROLE_KEYS = ["operator", "approver", "admin"] as const;

export default function AdminRolesPage() {
  const [rows, setRows] = useState<ProfileRow[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    setError(null);
    const supabase = createClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();
    if (!user) {
      setError("Not signed in");
      setLoading(false);
      return;
    }

    const claimed = await supabase.rpc("claim_bootstrap_admin");
    if (claimed.data === true) {
      setInfo("Bootstrap admin claimed for your account.");
    }

    const { data: profiles, error: pErr } = await supabase
      .from("profiles")
      .select("id, email, display_name");
    if (pErr) {
      setError(pErr.message);
      setLoading(false);
      return;
    }

    const { data: ur } = await supabase
      .from("user_roles")
      .select("user_id, roles(key)");

    const roleMap = new Map<string, string[]>();
    ur?.forEach((row) => {
      const key = (row.roles as unknown as { key: string } | null)?.key;
      if (!key) return;
      const list = roleMap.get(row.user_id) || [];
      list.push(key);
      roleMap.set(row.user_id, list);
    });

    setRows(
      (profiles || []).map((p) => ({
        ...p,
        roles: roleMap.get(p.id) || [],
      })),
    );
    setLoading(false);
  }

  useEffect(() => {
    void load();
  }, []);

  async function toggleRole(userId: string, roleKey: string, has: boolean) {
    setError(null);
    const supabase = createClient();
    const { error: err } = has
      ? await supabase.rpc("revoke_role", {
          target_user_id: userId,
          role_key: roleKey,
        })
      : await supabase.rpc("grant_role", {
          target_user_id: userId,
          role_key: roleKey,
        });
    if (err) {
      setError(err.message);
      return;
    }
    await load();
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 px-6 py-12">
      <div className="mx-auto max-w-4xl space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-emerald-400">
              Admin
            </p>
            <h1 className="mt-2 text-3xl font-semibold">Roles</h1>
          </div>
          <Link href="/dashboard" className="text-sm text-zinc-400 hover:text-zinc-200">
            ← Dashboard
          </Link>
        </div>

        {info ? <p className="text-sm text-emerald-300">{info}</p> : null}
        {error ? <p className="text-sm text-red-400">{error}</p> : null}
        {loading ? <p className="text-sm text-zinc-400">Loading…</p> : null}

        <div className="overflow-x-auto rounded-xl border border-zinc-800">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-zinc-900 text-zinc-400">
              <tr>
                <th className="px-4 py-3">User</th>
                {ROLE_KEYS.map((k) => (
                  <th key={k} className="px-4 py-3 capitalize">
                    {k}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="border-t border-zinc-800">
                  <td className="px-4 py-3">
                    <div className="font-medium">{row.display_name || "—"}</div>
                    <div className="text-zinc-400">{row.email}</div>
                  </td>
                  {ROLE_KEYS.map((k) => {
                    const has = row.roles.includes(k);
                    return (
                      <td key={k} className="px-4 py-3">
                        <button
                          type="button"
                          onClick={() => toggleRole(row.id, k, has)}
                          className={`rounded px-2 py-1 text-xs ${
                            has
                              ? "bg-emerald-500/20 text-emerald-300"
                              : "bg-zinc-800 text-zinc-400"
                          }`}
                        >
                          {has ? "Granted" : "Grant"}
                        </button>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
