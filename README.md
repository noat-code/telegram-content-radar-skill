# Telegram Content Radar

A shareable Hermes skill for collecting public Telegram-channel posts through the official Telegram API and turning external signals into original content angles.

## What it includes

- a safe first-login workflow for Telegram API collection;
- a public-channel collector script based on Telethon;
- editorial intake for audience, author position, interests, voice, evidence, boundaries, and success criteria;
- a scan → finding card → idea card → weekly review workflow;
- empty templates for a private user workspace.

## What it does not include

It does not include any user's channels, credentials, Telegram session, source findings, drafts, or personal editorial data.

## Security

Telegram codes and 2FA passwords must be entered only by the user in their own local Terminal during first login. They must never be sent to an agent in chat.

## Repository layout

```text
skills/telegram-content-radar/
├── SKILL.md
├── requirements.txt
├── scripts/
├── references/
└── templates/
```

Publish this repository as a Hermes Tap only after reviewing the templates and testing the workflow on a fresh workspace.
