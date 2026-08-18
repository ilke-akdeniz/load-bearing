# Load-Bearing agent instructions

This file is the Codex adapter for this repository.
The detailed project guide remains `CLAUDE.md`.
Do not duplicate that file here; duplication creates drift between agents.

## Startup

- Before any substantive repository change, read `CLAUDE.md` and follow it as the canonical project instruction file.
- Interpret references to "Claude" in `CLAUDE.md` as applying to the active coding agent, unless the instruction names a Claude Code-specific command, mode, UI feature, or file-discovery behavior.
- For quick read-only questions, you may answer from the loaded `AGENTS.md` plus targeted inspection, but read `CLAUDE.md` before writing prose, editing files, committing, or making editorial judgments.

## Interop with Claude Code

- Claude Code reads `CLAUDE.md` as its project memory.
- Codex reads this `AGENTS.md` automatically, then should consult `CLAUDE.md` when work requires the full protocol.
- Do not add `@AGENTS.md` to `CLAUDE.md` unless the user explicitly asks to invert the canonical file relationship.
- When switching between Codex and Claude Code, inspect `git status` and recent commits before acting.
- Treat any existing uncommitted changes as user or other-agent work unless the user says otherwise.

## Project workflow summary

- The book's authoritative documents are `README.md`, `00_toc.md`, `docs/LEDGER.md`, and `docs/DECISIONS.md`.
- If a planned change contradicts `docs/DECISIONS.md`, stop and report the conflict instead of proceeding.
- For chapter drafting or review, apply the anti-repetition protocol from `docs/LEDGER.md`.
- Record substantive editorial decisions in `docs/DECISIONS.md` using the existing Context / Options / Decision / Why / Consequence shape.
- Keep chapter status changes in `00_toc.md` aligned with the rules in `CLAUDE.md`.
- Run `tools/check-drift.py` before committing changes that affect book structure, terminology, chapter status, or cross-file consistency.

## Git

- Commit after making repository changes, unless the user explicitly asks not to.
- Never push.
- Keep commits scoped to one pass of work and avoid amending or rebasing the author's commits.
