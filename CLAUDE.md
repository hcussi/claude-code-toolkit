# CLAUDE.md

This project uses [`AGENTS.md`](AGENTS.md) as the canonical guide for agents
working in this repo. Read it first; it covers the repo's structure, the
published-vs-tooling split, the consistency invariants (enforced by a pre-commit
lint hook), how to add an agent or skill, and the house rules.

Quick reminders (see `AGENTS.md` for the full version):

- Never use em dashes anywhere.
- Single root `.gitignore` only.
- Never commit or push unless explicitly asked; run
  `./.claude/scripts/lint-toolkit.sh` to verify consistency first.
- Published items live in `agents/`, `skills/`, and `docs/`; repo maintenance
  tooling lives in `.claude/` and is not shipped.
