# AGENTS.md

Instructions for AI agents working in the Cybersecurity Knowledge repository.

## Required reading

Before you create, edit or review anything in this repository, read [GUIDELINE.md](GUIDELINE.md). It is the single source of truth for scope, structure, note format, writing style and quality checks. Do not duplicate its rules here. If this file and the GUIDELINE ever disagree, the GUIDELINE wins.

## Quick reminders

These are the rules that are most often broken. The full versions are in the GUIDELINE.

- Write everything in English.
- Use hyphens only. Never use em dashes or en dashes.
- Use natural, plain language. Avoid filler phrases and hype words (see [section 7](GUIDELINE.md#7-writing-style)).
- Explain concepts with a definition, an analogy, the mechanism, a concrete example and the boundaries (see [section 5](GUIDELINE.md#5-how-to-explain-a-concept)).
- Follow the note structure in [section 4](GUIDELINE.md#4-anatomy-of-a-note) and the naming rules in [section 3](GUIDELINE.md#3-repository-structure-and-naming).
- Do not invent facts, sources or version numbers. Cite primary sources.
- Never add secrets, credentials or personal data.
- Reflect every added, moved, renamed or deleted file in [ToC.md](ToC.md) and run `python3 scripts/check-toc.py`.
- Stay within the scope described in [README.md](README.md#scope).

## Workflow

1. Read the GUIDELINE and the README.
2. Check whether the topic already has a note, and extend it if so.
3. Write or edit the material, following the note template.
4. Run through the quality checklist in [section 10](GUIDELINE.md#10-quality-checklist), including the dash search.
5. Update the relevant area `README.md` and `ToC.md` so the new note is listed.
6. Report what changed, which sources were used and anything left unverified.
