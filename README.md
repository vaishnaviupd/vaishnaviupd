# Remote Internship Outreach Agent (Compliant Starter)

This repository now contains a starter design for an AI-assisted automation that:

1. Finds **remote internship** opportunities.
2. Identifies the right contact or application channel.
3. Personalizes outreach using your profile and CV.
4. Keeps you in control with an approval step before applying/sending.

> Important: Keep everything compliant with platform terms, privacy law, and anti-spam rules.

## What this includes

- `docs/agent-architecture.md` — architecture, workflow, and compliance guardrails.
- `src/internship_agent.py` — Python scaffold for building the agent with pluggable connectors.

## Quick start

```bash
python3 -m py_compile src/internship_agent.py
python3 src/internship_agent.py
```

## Testing

Run the following checks from the repository root:

```bash
python3 -m py_compile src/internship_agent.py
python3 -m unittest discover -s tests -v
python3 src/internship_agent.py
```

What each command verifies:
- `py_compile` checks syntax/import validity.
- `unittest` validates filtering and pipeline behavior.
- Running the script executes the demo pipeline end-to-end.

## Next steps

- Add approved data sources/APIs.
- Implement contact extraction and Google Form mapping for fields you explicitly allow.
- Wire LLM personalization with strict templates and human approval.

