---
name: telegram-content-radar
description: Find original Telegram content ideas from public channels.
version: 0.2.5
author: Igor Zinchenko, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [telegram, content, research, copywriting, competitors]
    related_skills: []
---

# Telegram Content Radar

Find useful signals in public Telegram channels and turn them into original, audience-fit content angles. This skill extracts topics, audience problems, delivery mechanics, and useful formats. It does not rewrite competitors' posts or copy their phrasing, stories, conclusions, visuals, recommendations, or personal authority.

## When to Use

- A user wants to monitor public Telegram channels for content ideas.
- A user needs a structured weekly scan of competitors or adjacent authors.
- A user wants to turn external signals into posts grounded in their own experience.

Do not use for private channels without permission, copying competitors, trading signals, or impersonating an author.

## Operating Modes

1. **Setup** - learn the user's editorial context, create a private workspace, and connect the read-only Telegram collector.
2. **Scan** - collect recent posts, filter weak or off-limits material, and create scored finding cards.
3. **Ideation** - turn selected signals into own angles, preserving the user's position and evidence.
4. **Review** - produce a weekly report, update the idea bank, and learn which topics/formats worked after publication.

Never jump from raw posts straight to a draft. The distinct angle and supporting evidence must come before writing.

## Private Workspace

The installed skill contains only methodology, scripts, and empty templates. Every user keeps their own workspace outside the skill directory:

```text
content-radar-workspace/
├── .env
├── .gitignore
├── config.yaml
├── editorial-profile.md
├── sources/telegram-channels.csv
├── findings/
├── ideas/
└── reports/weekly/
```

Copy the files from `templates/` to create this workspace. Do not put channels, credentials, findings, or drafts in the public skill repository.

## Mandatory Editorial Interview

**This is a hard gate before the first meaningful scan.** The agent must conduct a compact editorial interview, save the answers in the private `editorial-profile.md` and `config.yaml`, and use them as the scoring context. It must not infer the author's audience, voice, authority, or goals from competitor posts.

The interview must establish:

1. **Core reader** - who they are, their current stage, their job or context, the problem that brought them here, and what they are tired of in this niche.
2. **Author position** - honest role, lived experience, available proof, and claims the author will not make.
3. **Channel goal** - what the author wants readers to understand, decide, test, avoid, or change; and the main success metric for the next 1–3 months.
4. **Content map** - core lanes, adjacent lanes, and topics that look relevant but are off-position.
5. **Reader-job map** - for each core lane: reader pain, useful outcome, author's available proof, and fitting formats.
6. **Voice and boundaries** - depth, personal/educational ratio, preferred formats, taboo topics, prohibited claims, and topics requiring caution.
7. **Evidence inventory** - active experiments, cases, mistakes, data, artefacts, research, and topics where the author has no right to speak yet.
8. **Decision rules** - what makes a source signal relevant, draft-ready, uncertain, or an automatic discard.

Use `templates/editorial-profile.example.md`. Ask in compact batches and reuse answers the author has already supplied. A full scan may not be called complete while the core reader, author role, channel goal, core lanes, taboo topics, or evidence inventory are unknown. In that case, ask targeted questions and mark any early result as **provisional**.

## Mandatory Security Rule: Telegram Login

The collector uses a Telegram **user account** through the official Telegram API to read public channels. It never sends posts, reactions, messages, or join requests.

- Never ask the user to send a Telegram login code, 2FA password, API ID, API hash, phone number, or session file in chat.
- Never submit a login code or 2FA password through an agent-managed terminal process.
- For the first login, give the user a command to run in their own local Terminal window. They must type the code and any 2FA password directly there.
- After the user says the local login is complete, verify only non-secret facts: a session file exists and a JSONL collection file contains the expected channel rows and post count.
- Keep `.env`, `*.session`, and collected raw posts out of Git.

## First-Time Setup Workflow

Follow this sequence exactly.

1. **Create the workspace.** Copy `templates/.env.example`, `templates/config.example.yaml`, `templates/editorial-profile.example.md`, `templates/telegram-channels.example.csv`, and `templates/.gitignore.example` into the user's chosen workspace.
2. **Run editorial intake.** Fill the profile before selecting channels. Do not decide the user's voice, audience, or taboos from competitor posts.
3. **Get Telegram API credentials.** Tell the user to open `https://my.telegram.org` → `API development tools`, create an application, and copy `App api_id` and `App api_hash` into their local `.env`. Do not ask them to show or paste the values.
4. **Add the phone locally.** The user adds `TG_PHONE` in international format to `.env`. Do not request the number in chat.
5. **Add channels.** Fill `sources/telegram-channels.csv`. Every source must have a role, priority, and note about what is useful or excluded.
6. **Install the collector locally.** Create a workspace-local virtual environment and install `telethon` using `requirements.txt`. Do not install it globally unless the user explicitly prefers that.
7. **Provide, do not execute, the first-login command.** Give the user a command for their own local Terminal. It must set `CONTENT_RADAR_HOME` and point to this skill's `scripts/fetch_telegram_posts.py`.
8. **Wait for user confirmation.** The user enters Telegram's code and, if enabled, their 2FA password only in that local Terminal. Never ask for either secret in the conversation.
9. **Verify safely.** After confirmation, check that `collector/telegram.session` exists and that a JSONL output has non-zero channel and post counts. Do not display secrets.

## Scan Workflow

1. Read the editorial profile, configuration, and active channel list first.
2. Collect a defined window, normally 7–14 days and 20–30 messages per channel.
3. Parse the raw JSONL programmatically. Verify the number of attempted channels, successful rows, failures, and total text posts before reporting totals.
4. Ignore ads, reposts without commentary, bare links, operational trading signals, generic news, and any material excluded in the editorial profile.
5. Deduplicate repeated posts, repeated thesis, and already-captured ideas before scoring.
6. Create a finding card only when there is a reusable principle, audience pain, format mechanism, or a genuinely distinct angle available to the user.
7. Store rejected patterns separately when they explain an important boundary, but do not bloat the idea bank.

## Finding Card

Use `templates/finding-card-template.md`. For every retained source signal, record:

- source, post link, and date;
- topic and format;
- opening hook;
- core conflict or audience problem;
- why the delivery may work;
- useful principle or mechanism;
- what cannot be reused;
- the user's distinct angle, evidence, and possible format;
- score and decision.

Do not reproduce more source text than needed for attribution or a short analytical reference.

## Scoring and Originality Gate

Score five dimensions from 0 to 3, using `references/scoring-model.md`:

- relevance to the user's channel;
- reader usefulness;
- availability of a genuine own angle;
- original-post potential;
- hook or format strength.

- 0–7: reject.
- 8–11: retain in the idea bank.
- 12–15: develop into a draft-ready angle.

A score never overrides the originality gate. Reject if the post would depend on copied wording, the competitor's personal story, their unverified recommendation, or borrowed authority.

### Audience-Fit Gate

Topic overlap is not audience fit. Before calling an idea `Now` or draft-ready, confirm the source post and the author's core reader overlap in **reader context, problem, desired outcome, and acceptable author position**. A post about the same broad topic but aimed at a different reader job, level, or promise is off-position. If the overlap cannot be established from the editorial interview and source signal, use `Question for author` or `Maybe / needs evidence`, never a confident recommendation.

The transformation must be:

> external signal → independent check → own experience, data, or position → distinct practical takeaway

## Mandatory Report Delivery Gate

**This step is required after every scan, including a one-channel test.** Before asking the author to choose an idea, collecting evidence, creating an idea card, or offering a draft:

1. Save a completed report in the private workspace under `reports/weekly/`, using `templates/weekly-report-template.md`.
2. Deliver the report summary in chat in a readable, visual format. Use light section emojis such as `📊`, `✨`, `🚫`, and `👉` to make scanning easier; do not decorate every line.
3. State coverage, selected original angles, rejected patterns, and exactly one next decision for the author.
4. Confirm the report’s declared channel and post totals match the parsed JSONL before presenting it.
5. Present every qualified original angle - there is no default cap, so do not arbitrarily reduce a scan to 1–3 choices. Group them as `Now`, `Later`, `Maybe / needs evidence`, and `Question for author`; invite the author to keep or discard each. Create linked `Later` backlog tasks for every angle the author keeps but does not choose to develop now, including the evidence or decision still needed.

A report saved silently is not delivered. The author must see it before the workflow can advance. Only after the author chooses an angle may the agent collect a case, create an idea card, and offer a draft. The remaining strong angles stay in the private idea backlog rather than disappearing from the next scan.

### Question for Author Rule

Use `Question for author` when the agent cannot honestly decide whether an otherwise viable angle fits the author’s voice, lived experience, audience, or current priorities. State the uncertainty and ask one short keep-or-discard question. Do not hide a clearly weak, prohibited, or derivative angle behind a question: discard it with a reason.

## Ideation and Draft Handoff

For every idea that survives the gate, make an idea card using `templates/idea-card-template.md` before drafting. It must answer:

1. What will our post say that the source did not?
2. What real evidence or experience makes us entitled to say it?
3. What does the reader understand, decide, or do differently afterwards?
4. Which format fits the author's voice: work log, observation, explanation, decision diary, framework, checklist, or community question?
5. What would invalidate or limit the point?

Only then offer a draft. If the user asked for ideas rather than drafts, stop at the angle and outline.

## Weekly Review

Use `templates/weekly-report-template.md`. The report must contain:

- period, channels scanned, posts reviewed, failed/inaccessible sources;
- every qualified original angle and its score, grouped as `Now`, `Later`, `Maybe / needs evidence`, and `Question for author`; do not impose a default numeric cap;
- the best original angles, not copied post summaries;
- rejected patterns and why they were excluded;
- ideas already covered or too close to recent posts;
- next actions: draft, research, collect evidence, ask the audience, or discard;
- after publication: the user's observed outcome and a note on what to reuse or avoid.

## Output Layers

Produce three layers, not a link dump:

1. **Raw findings** - collected source posts in JSONL.
2. **Idea bank** - transformed angles with the user's own evidence and position.
3. **Weekly report** - prioritised original opportunities and next actions.

## Verification

Before calling a run successful, verify all of the following:

- The editorial profile exists, or any missing fields are explicitly flagged.
- A local Telegram session exists after the user completes local login.
- The output has one row for every active channel attempted.
- The declared post total matches the parsed JSONL total.
- Any channel failures are named clearly.
- Every selected idea has a distinct angle and evidence, not just a source link.
- The report contains no copied text beyond a minimal attribution or necessary short reference.
- The report was both saved in `reports/weekly/` and presented to the author before ideation or drafting began.
- Every unchosen strong angle is either a linked `Later` backlog task with its missing evidence/decision, a `Question for author` item with a clear keep-or-discard question, or deliberately discarded with a reason.
- Secrets, session files, and raw private workspace data are excluded from Git.

## Pitfalls

- A Telegram bot cannot silently read arbitrary competitor channels. Use the user-account collector only for public-channel research.
- Public channels may restrict access, rename handles, or return no recent text posts. Record that result rather than guessing.
- Do not treat view count as proof that a topic is useful for a different audience.
- Do not turn an expert's recommendation into the user's position without independent research or personal experience.
- Do not force every useful signal into a post. A good discarded finding can still sharpen the user's editorial boundaries.
