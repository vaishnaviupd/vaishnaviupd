# AI Agent Blueprint: Remote Internship Outreach

## Objective

Build an AI-assisted system that discovers **remote internships**, then prepares and (optionally) submits applications or outreach messages that are customized to each company.

## Guardrails (recommended)

1. **User in the loop:** Never auto-submit without explicit approval.
2. **Respect Terms of Service:** Prefer official APIs, RSS feeds, ATS portals, and opt-in channels.
3. **No spam behavior:** Use rate limits and deduplication.
4. **Data minimization:** Share only required CV fields for each application.
5. **Auditability:** Keep logs for every draft, decision, and submission.

## High-level architecture

1. **Ingestion layer**
   - Approved job sources (company career pages, internship boards, ATS endpoints).
   - Pull cadence: every N hours.

2. **Filtering + scoring layer**
   - Keep only listings where:
     - title matches internship roles,
     - location indicates remote / distributed,
     - listing is active.
   - Score with weighted features (role fit, skill overlap, freshness, brand preference).

3. **Enrichment layer**
   - Extract hiring contact if available in the posting.
   - Detect application channel type:
     - direct ATS link,
     - Google Form,
     - email outreach,
     - platform message.

4. **Personalization layer**
   - Resume tailoring (skills ordering, summary snippet, project highlights).
   - Outreach text generation with strict template constraints:
     - concise,
     - role-specific,
     - no fabricated experience.

5. **Execution layer**
   - Draft mode by default.
   - Human approval UI/CLI.
   - Controlled submit/send only after approval.

6. **Tracking layer**
   - Store opportunity state: discovered -> drafted -> approved -> submitted -> responded.
   - Daily report of outcomes.

## Data model (minimum)

- `Opportunity`: source, role, company, url, remote_flag, posted_at, deadline.
- `Contact`: name, channel, address/profile_url, confidence.
- `ApplicationDraft`: tailored_summary, selected_cv_version, message_draft, form_field_map.
- `SubmissionEvent`: timestamp, action, status, evidence.

## Suggested stack

- Python orchestration: scheduling + pipelines.
- SQLite/Postgres for state.
- LLM API for personalization + extraction.
- Browser automation only for pages where API is unavailable and usage is permitted.

## Remote internship filters

Use strict filters first:

- include keywords: `intern`, `internship`, `summer intern`, `student`.
- remote terms: `remote`, `work from home`, `distributed`.
- exclude: `senior`, `full-time` (unless internship full-time seasonal), `on-site`.

## Example workflow

1. Fetch 200 listings.
2. Filter to remote internships.
3. Rank top 20 by fit.
4. Create drafts for top 10.
5. Present drafts for approval.
6. Submit approved applications and log confirmations.

## Risks and mitigation

- **Hallucinated personalization** -> enforce retrieval-backed prompts and fact checks.
- **Duplicate applications** -> unique key `(company, role, source_url)`.
- **Policy violations** -> source whitelist + compliance checks per channel.

## Implementation tip

Start with **draft-only mode** and manually submit for two weeks. Once quality is stable, automate narrow pieces (e.g., form pre-fill) while retaining an approval gate.
