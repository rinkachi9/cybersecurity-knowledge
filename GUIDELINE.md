# Guideline

This document describes how to approach the Cybersecurity Knowledge repository: what belongs in it, how notes are organized, how concepts must be explained and what quality bar every note has to meet. It applies to people and to AI agents alike.

## Table of Contents

1. [Purpose and audience](#1-purpose-and-audience)
2. [Core principles](#2-core-principles)
3. [Repository structure and naming](#3-repository-structure-and-naming)
4. [Anatomy of a note](#4-anatomy-of-a-note)
5. [How to explain a concept](#5-how-to-explain-a-concept)
6. [Examples, code and diagrams](#6-examples-code-and-diagrams)
7. [Writing style](#7-writing-style)
8. [Sources, references and verification](#8-sources-references-and-verification)
9. [Rules specific to this repository](#9-rules-specific-to-this-repository)
10. [Quality checklist](#10-quality-checklist)
11. [Maintenance and versioning](#11-maintenance-and-versioning)
12. [Working with AI agents](#12-working-with-ai-agents)

## 1. Purpose and audience

The repository is a long term reference for cybersecurity. It has two jobs:

- **Teach.** Someone with general technical background but no experience in the specific topic should be able to read a note and come away with a correct mental model.
- **Recall.** Someone who already knows the topic should be able to find the exact detail they need quickly, without wading through introductions.

To serve both, every note is layered. It starts with a short plain language summary, then builds up to precise detail. A reader can stop at any layer and still have learned something true.

The primary audience is the future version of the author. Write as if explaining to a smart colleague who was not in the room when you learned the topic. Do not assume they remember the context, the tools you used or the problem you were solving at the time.

## 2. Core principles

**Depth over breadth.** A note that explains one idea thoroughly is worth more than five that name-drop ten. Cover a topic completely before moving on: what it is, why it exists, how it works, when to use it, when not to use it, and how it fails.

**Explain the why, not only the what.** Facts without reasons are trivia. For every rule, tool or technique, state the problem it solves. A reader who understands the problem can reconstruct the solution and can tell when it does not apply.

*Example.* "Use parameterized queries" is a rule. "Parameterized queries keep data and code separate, so input can never change the structure of the statement" is understanding.

**Precision.** Use the correct technical term, define it on first use and keep using it consistently. Do not swap synonyms for variety, because a reader may assume two words mean two things. Quantify when you can: "about 10 ms on a warm cache" beats "fast".

**Show, then generalize.** Introduce an abstraction with a concrete case first, or immediately after. People learn patterns from instances.

**Be honest about uncertainty.** If something is unverified, simplified or version dependent, say so in the note. A clearly marked gap is better than a confident error.

**One idea, one place.** Each concept has a single home note. Other notes link to it. Duplicated explanations drift apart and become contradictory.

**Make it verifiable.** Claims link to sources. Examples can be run or reproduced. Numbers say where they came from.

## 3. Repository structure and naming

### 3.1 Layout

Content is organized by knowledge area, and each area is a top level directory. The list of planned areas is in the [README](README.md#knowledge-areas).

```text
ToC.md                  # full tree of every file in the repository
_assets/
    <area>/             # images, diagram sources, media and other files used by notes
<area>/
    README.md           # entry point: what the area covers, reading order, links to notes
    <topic>.md          # a single note
    <subarea>/          # optional, groups related notes
        README.md
        <topic>.md
        <topic>/        # optional, when a topic has its own scripts or files
            README.md   # the note itself
            scripts/    # scripts that belong to this topic only
```

Guidance:

- **Prefer flat over deep.** Two levels below the repository root (area and subarea) is usually enough. Add a subarea when an area has more than about twelve files or when a group of notes clearly belongs together.
- **One note, one main idea.** If a note needs a table of contents longer than about ten entries, it is probably several notes.
- **Every area and subarea has a `README.md`.** It is the entry point, and it lists the notes in a recommended reading order with a one line description each. Areas that are planned but not written yet have a `README.md` that says so and lists planned topics.
- **Media goes to `_assets/<area>/`, scripts stay with their topic.** Images, diagram sources, downloadable files and media go to `_assets/<area>/`. A script lives next to the material it belongs to: when a topic gets scripts, the note becomes a directory `<topic>/` with `README.md` (the note) and a `scripts/` directory. There is no global `scripts/` directory.
- **Keep `ToC.md` complete.** See [section 3.4](#34-table-of-contents).

*Analogy.* Think of a library. Areas are sections, area READMEs are the catalog cards for a section, and notes are the books. A book that tries to cover an entire section belongs on several shelves.

### 3.2 Naming

| Item | Convention | Example |
| --- | --- | --- |
| Directories | lowercase, words separated by hyphens | `query-performance/` |
| Note files | lowercase, hyphens, descriptive noun phrase, `.md` | `b-tree-indexes.md` |
| Images and media | note name, then a short description, stored in `_assets/<area>/` | `_assets/cryptography/pki-chain-of-trust.png` |
| Diagram sources | same base name as the rendered image, source format as extension | `_assets/cryptography/pki-chain-of-trust.drawio` |
| Scripts | lowercase, hyphens, verb phrase, stored in the `scripts/` directory of their topic | `network-security/pcap-analysis/scripts/parse-pcap-summary.py` |
| Entry points | always `README.md` | `<area>/README.md` |
| Table of contents | always `ToC.md` in the repository root | `ToC.md` |

Names describe the content, not its status or origin. Avoid `notes.md`, `misc.md`, `new-draft-2.md` or dates in file names. Do not use spaces or uppercase letters, so that links and shell commands behave the same on every system.

### 3.3 Links

- Use relative links between notes, for example `[indexes](../query-performance/b-tree-indexes.md)`.
- Link to a heading when you point at a specific part: `[isolation levels](transactions.md#isolation-levels)`.
- Link text describes the target ("the section on isolation levels"), never "click here".
- When a prerequisite is needed, link it in the note's front section instead of re-explaining it.

### 3.4 Table of contents

`ToC.md` in the repository root is the complete map of the repository. It is an indented tree with one entry for every file: root documents, area and subarea `README.md` files, notes, assets and scripts. Each entry is a relative link followed by a short description.

- **Every change is reflected in `ToC.md`.** Adding, moving, renaming or deleting a note, an asset or a script updates `ToC.md` in the same change. Changing the title or purpose of a note updates its description there.
- **Planned areas are marked.** An area that has only a `README.md` is marked `(planned)`.
- **Verify before finishing.** Compare `ToC.md` with the output of `git ls-files --cached --others --exclude-standard` and check that every link resolves.
- **`ToC.md` is not a replacement for area READMEs.** The area README keeps the recommended reading order and the context. `ToC.md` keeps the complete list.

## 4. Anatomy of a note

Every note follows the same skeleton, so a reader always knows where to look. Sections that do not apply may be dropped, but their order stays. Notes have no front matter: a note starts with its title.

```markdown
# <Title>

## Summary
Two to four sentences in plain language. What is this, and why should the reader care?

## Prerequisites
Links to notes the reader should know first. State the assumed knowledge.

## Core concepts
Precise definitions, the mechanism, the vocabulary. Build from simple to complex.

## Worked example
A concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it
Benefits, costs, alternatives, and the situations where this is the wrong choice.

## Common mistakes
Frequent misunderstandings and failure modes, with the fix for each.

## Practice
Questions or small exercises, with answers or hints kept at the bottom.

## Further reading
Annotated links to primary sources, one sentence on why each is worth reading.
```

Notes on the skeleton:

- **No metadata block.** The directory tells the area, the title is the first line, and open gaps are marked with `TODO:` lines.
- **Summary first.** A reader who only reads the summary must not come away with a wrong idea. Avoid teasers such as "we will see how this works".
- **Motivation before mechanism.** People remember mechanisms better when they know what they were invented to fix.
- **Practice is part of the note.** Retrieval practice is what turns reading into knowledge. Even three good questions are valuable.

### 4.1 Migrated notes

Notes that were migrated from an older source (`Security.html`) keep their original content and are brought up to the standard over time.

- Sections of the skeleton that the original did not have contain a single line that starts with `TODO:`. Replace it with real content, or delete the section if it does not apply.
- Search for open gaps with `grep -rn "^TODO:" --include="*.md" .`. A note without `TODO:` lines has met the skeleton, but still has to be checked against sources (see [section 8](#8-sources-references-and-verification)).
- Content that was migrated has not been verified against sources.
- The dash and emoji rules of [section 7](#7-writing-style) apply to migrated content as well. Dashes were replaced by hyphens and emoji by words during migration.

## 5. How to explain a concept

Every concept that gets its own section or note is explained with the same five moves. This is the core of the standard.

1. **Definition.** One or two precise sentences. Say what the thing is and what distinguishes it from things that look similar.
2. **Intuition through analogy.** A comparison to something familiar. State where the analogy holds and where it breaks.
3. **Mechanism.** How it actually works, step by step, with the correct terminology.
4. **Concrete example.** A small, realistic case that uses real values and can be reproduced.
5. **Boundaries.** When to use it, when not to, what commonly goes wrong.

### 5.1 Writing good analogies

An analogy is a bridge to a known idea, not a decoration.

- **Map the parts explicitly.** "The index is the book's back-of-book index, the page number is the row location."
- **Choose a familiar source.** Everyday objects and systems work best: libraries, kitchens, traffic, post offices, buildings.
- **Say where it breaks.** Every analogy misleads somewhere. Naming the limit prevents the reader from carrying a false belief forward.
- **Use one analogy per idea.** Stacking three metaphors confuses more than it clarifies.
- **Never let the analogy replace the mechanism.** It opens the door, and the precise explanation must still follow.

### 5.2 Writing good examples

- **Minimal but real.** Small enough to hold in your head, realistic enough to feel like something you would meet in practice.
- **Complete.** The reader can run it or reproduce it without guessing at missing pieces.
- **Show expected output.** Say what happens, including the failure case, so the reader can check their understanding.
- **Progress in difficulty.** Start with the simplest case, then add one complication at a time.
- **Contrast.** Show the wrong way next to the right way, and explain why the first fails.

### 5.3 Depth checklist for a concept

Before a concept is considered explained, you should be able to answer:

- What problem does it solve, and what happened before it existed?
- What are its precise definition and its key properties?
- How does it work internally, at least at one level below the surface?
- What are the alternatives, and how do they differ?
- What does it cost (time, complexity, money, risk)?
- How does it fail, and how would you notice?
- What is the most common misconception about it?

### 5.4 A full example of the standard

The following shows the five moves applied to one concept in this repository.

**Concept: Defense in depth**

*Definition.* Defense in depth is the practice of stacking several independent security controls, so that the failure of one control does not lead to a full compromise.

*Analogy.* Think of a medieval castle. An attacker must cross a moat, climb a wall, get past guards and then break into the keep. Each layer is imperfect, but together they make the attack slow, noisy and expensive. The important detail is that the layers are independent: a drawbridge that fails open should not also disable the wall.

*Example.*

A web application stores customer data in a database. The layers might be:

1. A web application firewall filters obviously malicious requests.
2. The application validates input and uses parameterized queries.
3. The database account used by the application has `SELECT` and `INSERT` on two tables and nothing else.
4. The database is only reachable from the application subnet.
5. Data at rest is encrypted, so a stolen disk is not a stolen dataset.

If an attacker finds a SQL injection in layer 2, layers 3 to 5 still limit what they can read, change or exfiltrate.

*Pitfall.* Treating the layers as a checklist. Five controls that all depend on the same admin password are one control, not five.

Notice the pattern: the definition is precise, the analogy explains the idea in familiar terms, the example is concrete and reproducible, and the pitfall warns about a mistake that real practitioners make.

## 6. Examples, code and diagrams

### 6.1 Code

- Use fenced code blocks and always declare the language (` ```python `, ` ```sql `, ` ```bash `).
- Examples must be **tested**. If you cannot run it, mark it clearly as untested.
- State the **versions** of languages, tools and libraries involved.
- Keep examples **self contained**: imports, setup and sample data included.
- **Comment the why**, not the what. `# retry because the API rate limits at 10 req/s` helps. `# increment i` does not.
- Do not paste large listings. Show the relevant part and link to the full file if needed.
- Output is shown in its own block, labeled as output.

### 6.2 Diagrams

- Prefer text based diagrams so they are diffable and versioned with the note. Use a fenced `mermaid` block for flows, sequences, state machines, attack trees, architectures and timelines. Use a fenced `text` block for ASCII diagrams such as trees and data layouts.
- Mermaid renders on GitHub and in most editors. Keep each diagram small enough to read without zooming, and split it when it grows past about 15 nodes.
- A diagram earns its place by showing something prose cannot: structure, flow over time, relationships. Do not add one for decoration.
- Every diagram has a caption or a sentence before it saying what to look at, and the same information is available in the surrounding text for readers who cannot see the image.
- If you use an image, put it in `_assets/<area>/`, keep its editable source (for example `.drawio`, `.excalidraw` or `.svg`) in the same directory, and add descriptive alt text.
- Images taken from other people (vendor infographics, slides) are allowed only for personal study. Credit the author in the alt text or caption and prefer redrawing them as Mermaid or SVG when the note is reviewed.

### 6.2.1 Scripts, files and media

- **Scripts** live in a `scripts/` directory next to the topic they belong to (see [section 3.1](#31-layout)). The note shows the relevant part and links to the full script. A script states its language and tool versions in a header comment, is self contained and says how to run it.
- **Downloadable files** (checklists, configuration templates, exported rules, small datasets) go to `_assets/<area>/`. Only files that are safe to publish belong here: no secrets, no real client or personal data, no live malware. Samples, captures and dumps are excluded by `.gitignore` on purpose.
- **Large media** (video, large captures) is linked from a public source instead of being committed. If a large file is essential, discuss it first because it stays in the git history forever.
- **Every asset and script** appears in `ToC.md`.

### 6.3 Tables

Use tables for comparisons across the same dimensions (features, costs, trade offs). Do not use tables for prose that happens to have two columns. Keep cells short.

### 6.4 Data

Use synthetic or public data only. If a dataset is needed, either generate it in the example or link to its public source. Never include personal, confidential or client data.

## 7. Writing style

The writing must sound like a knowledgeable person explaining something to a colleague. It should be plain, direct and specific.

### 7.1 Language

- **Everything is written in English.** This includes notes, comments in code, commit messages and file names.
- Use one variant of English consistently (American spelling is the default here).
- Prefer short sentences. If a sentence needs two readings, split it.
- Use the active voice and concrete subjects. "The scheduler drops the task" beats "the task is dropped".
- Prefer plain words over inflated ones. Write "use", not "utilize". Write "help", not "facilitate".
- Define acronyms on first use in each note, then use the acronym.

### 7.2 Punctuation: hyphens only

Use ordinary hyphens (`-`) and nothing longer. **Do not use em dashes or en dashes** in any file in this repository. They are a recognizable marker of machine generated text and they make prose harder to read.

Instead, rewrite the sentence:

| Instead of | Write |
| --- | --- |
| The cache, which is fast, is not durable | The cache is fast, but it is not durable |
| Two options: fast, or safe | There are two options: fast or safe |
| It works, in theory | It works in theory |

Guidance:

- Use commas, periods, colons and parentheses for pauses and asides.
- Use a hyphen for compound modifiers ("read-only replica", "low-level API") and for number ranges written with digits.
- If a sentence seems to need a dash, it is usually two sentences, or it needs a comma.

### 7.3 Avoiding machine sounding language

Text produced by language models has recognizable habits. Remove them, whether you wrote the text or an assistant did.

- No filler openers: "It is important to note that", "In today's fast-paced world", "Let's dive in", "In conclusion".
- No vague intensifiers or hype: "powerful", "seamless", "robust", "game changing", "cutting edge", "leverage", "delve", "landscape", "tapestry", "crucial" without a reason.
- No empty triads and rhetorical patterns ("fast, scalable, and reliable"), or the "It's not just X, it's Y" construction.
- No summary sentence that only repeats the paragraph.
- No decorative emojis and no exclamation marks.
- No headings that are questions or slogans. Use plain descriptive headings.
- Do not over-format. Bullet lists are for parallel items, not for every thought. Bold is for a term being defined or for a rare warning.
- Be specific. Replace "many companies use this" with a named example, or with nothing.

**Before:**

> It is important to note that database indexes are a powerful tool that can seamlessly boost your query performance, making your applications faster and more scalable!

**After:**

> An index lets the database find rows without reading the whole table. A lookup by customer ID on a table with 5 million rows drops from a full scan to a few page reads. The cost is slower writes, because every insert must update the index.

### 7.4 Formatting conventions

- One top level heading (`#`) per file, matching the title. Then `##` and `###`. Do not skip levels.
- Headings use sentence case: "Query performance", not "Query Performance".
- Use backticks for code, commands, file names, and identifiers. Use *italics* for the first mention of a new term when it is being defined.
- Wrap nothing by hand. Write one paragraph per line, so diffs stay readable.
- End every file with a single newline.
- Numbers: use digits for measurements and counts above nine, write out smaller numbers in prose, and always include units.

## 8. Sources, references and verification

- **Prefer primary sources.** Specifications, official documentation, original papers and source code beat blog posts and videos. Use secondary sources to find primary ones.
- **Cite what you use.** Put links in the "Further reading" section, or inline for a specific claim. Include enough to find the source if the link dies: title, author or organization, year.
- **Write in your own words.** Summaries are paraphrased. Quote only when the exact wording matters, keep quotes short, and mark them clearly.
- **Record the date.** For anything that changes over time (versions, prices, limits, recommendations), write the version and the date it was checked in the text, for example "Checked against NIST CSF 2.0, 2026-09".
- **Separate fact, interpretation and opinion.** Mark opinions as opinions ("In my experience", "I prefer this because").
- **Check claims that sound too good.** Reproduce numbers when you can. Look for a second source for anything surprising.

Typical primary sources for this repository: MITRE ATT&CK, NIST publications (SP 800 series), OWASP projects, CIS Benchmarks, vendor advisories, CVE and NVD entries, and peer reviewed papers.

## 9. Rules specific to this repository

Scope for this repository is cybersecurity. In addition to the general rules above:

- **Authorized use only.** Every offensive technique must be framed in the context of a lab, a CTF, a penetration test with written permission, or defensive research. State this context explicitly in the note.
- **Defense first.** Each attack note ends with a section on detection and mitigation. Knowing how to break something is only half of the note.
- **No live secrets.** Use placeholders such as `<API_KEY>` and reserved documentation addresses (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `example.com`).
- **Reference identifiers.** When a note discusses a known weakness, link the CVE, CWE or ATT&CK technique ID so the reader can verify the claim.

If a note drifts into another domain, keep the part that serves this repository, link to the sibling repository for the rest and do not duplicate it.

## 10. Quality checklist

Run this list before marking a note as `reviewed`.

**Content**

- [ ] The summary is correct on its own and written in plain language.
- [ ] Every new term is defined at its first use.
- [ ] The problem the topic solves is stated before the mechanism.
- [ ] There is at least one worked example that can be reproduced.
- [ ] At least one analogy is used, and its limit is stated.
- [ ] Trade offs, alternatives and failure modes are covered.
- [ ] Common mistakes are listed with their fixes.
- [ ] Versions and dates are recorded where relevant.

**Accuracy**

- [ ] Claims are backed by sources, and the sources are linked.
- [ ] Code was run, and the output shown is real.
- [ ] Numbers are reproducible or have a stated origin.

**Style**

- [ ] The note is entirely in English.
- [ ] No em dashes or en dashes anywhere (search for them before committing).
- [ ] No filler phrases, hype words or decorative emojis.
- [ ] Headings are descriptive and in sentence case.
- [ ] Links are relative and work.

**Hygiene**

- [ ] No secrets, personal data or confidential material.
- [ ] File and directory names follow the naming rules.
- [ ] The note is linked from its area `README.md`.
- [ ] `ToC.md` reflects every added, moved, renamed or deleted file, and its links resolve.

A quick way to check the dash rule from the repository root:

```bash
grep -rnP "\x{2013}|\x{2014}" --include="*.md" .
```

## 11. Maintenance and versioning

- **Small, focused commits.** One note or one logical change per commit. Explain the reason in the message.
- **Commit message format.** A short imperative subject in English, for example `Add note on B-tree indexes`. Add a body when the reason is not obvious.
- **Branching.** Use short lived branches for larger additions. Small edits can go directly to the main branch.
- **Review cycle.** New notes contain `TODO:` lines until the skeleton is filled. After that, check the content against sources and record what was checked in the text.
- **Refresh.** Revisit notes on fast moving topics regularly, update the recorded check date and fix what changed. Delete or rewrite content that is no longer true instead of leaving it with a warning.
- **Refactor structure early.** When a note grows too large, split it. When two notes overlap, merge them or extract the shared part into its own note and link to it.
- **Keep the index honest.** Every new note is added to its area `README.md` and to `ToC.md` in the same commit. Every move, rename or deletion is reflected in both as well.

## 12. Working with AI agents

AI assistants are welcome collaborators. The rules are the same as for a human contributor, and the human author remains responsible for correctness.

- **Read this file first.** `AGENTS.md` and `CLAUDE.md` point here. This GUIDELINE is the only place where conventions are defined.
- **Do not invent facts.** If a detail is uncertain, say so in the note or leave it out. Never fabricate citations, version numbers, benchmarks or quotes.
- **Verify before writing.** Use primary sources for claims, and record them.
- **Follow the style rules strictly.** In particular the ban on em dashes and en dashes, and the ban on filler language (see [section 7](#7-writing-style)).
- **Stay in scope.** Do not add content unrelated to the request. Do not restructure the repository without being asked.
- **Prefer editing to creating.** Extend an existing note when the topic already has a home. Create a new file only when the topic deserves its own note.
- **Update `ToC.md` with every change.** Any file added, moved, renamed or deleted must be reflected in `ToC.md` before the task is finished (see [section 3.4](#34-table-of-contents)).
- **Ask when a decision is unclear.** Structure, scope and naming decisions belong to the author.
- **Never commit secrets or personal data,** and never run destructive git operations without explicit approval.
- **Show your work.** When adding a note, summarize what was written, which sources were used and what remains unverified.
