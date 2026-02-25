"""Compliant starter scaffold for a remote internship outreach agent.

This module provides structure only (not direct platform automation for restricted flows).
Plug in approved sources/connectors and keep a human approval gate before submission.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Opportunity:
    source: str
    role: str
    company: str
    url: str
    remote_flag: bool
    posted_at: Optional[datetime] = None
    description: str = ""


@dataclass
class Contact:
    name: str
    channel: str  # email, application_portal, form_link, etc.
    destination: str
    confidence: float


@dataclass
class ApplicationDraft:
    opportunity: Opportunity
    tailored_summary: str
    outreach_message: str
    form_field_map: Dict[str, str] = field(default_factory=dict)


class OpportunitySource:
    """Interface for data ingestion from approved job sources."""

    def fetch(self) -> List[Opportunity]:
        raise NotImplementedError


class RuleBasedFilter:
    include_terms = ("intern", "internship", "student")
    remote_terms = ("remote", "work from home", "distributed")
    exclude_terms = ("senior", "on-site", "onsite")

    def keep(self, opp: Opportunity) -> bool:
        text = f"{opp.role} {opp.description}".lower()
        has_intern = any(t in text for t in self.include_terms)
        has_remote = opp.remote_flag or any(t in text for t in self.remote_terms)
        has_excluded = any(t in text for t in self.exclude_terms)
        return has_intern and has_remote and not has_excluded


class Personalizer:
    """Replace with LLM-backed implementation using strict prompt constraints."""

    def create_draft(self, opp: Opportunity, cv_profile: Dict[str, str]) -> ApplicationDraft:
        summary = (
            f"Candidate fit for {opp.role} at {opp.company}: "
            f"focus on relevant projects, internship readiness, and remote collaboration."
        )
        message = (
            f"Hello, I am interested in the remote {opp.role} opportunity at {opp.company}. "
            "I have attached my CV and would value the chance to be considered."
        )
        return ApplicationDraft(opportunity=opp, tailored_summary=summary, outreach_message=message)


class ApprovalGate:
    """Human-in-the-loop approval gate."""

    def is_approved(self, draft: ApplicationDraft) -> bool:
        # Keep this explicit in production (CLI/UI approval).
        return False


class Executor:
    """Execution stub; integrate only with channels you are authorized to use."""

    def submit(self, draft: ApplicationDraft) -> str:
        return f"Draft not submitted (approval or connector missing): {draft.opportunity.url}"


def run_pipeline(opportunities: List[Opportunity], cv_profile: Dict[str, str]) -> List[str]:
    filt = RuleBasedFilter()
    personalizer = Personalizer()
    approval = ApprovalGate()
    executor = Executor()

    results: List[str] = []
    for opp in opportunities:
        if not filt.keep(opp):
            continue
        draft = personalizer.create_draft(opp, cv_profile)
        if approval.is_approved(draft):
            results.append(executor.submit(draft))
        else:
            results.append(f"Draft generated pending approval: {opp.company} - {opp.role}")
    return results


if __name__ == "__main__":
    sample_data = [
        Opportunity(
            source="example-board",
            role="Data Analyst Intern",
            company="Acme",
            url="https://example.com/jobs/123",
            remote_flag=True,
            description="Remote internship focused on analytics and SQL.",
        )
    ]

    profile = {
        "name": "Your Name",
        "skills": "Python, SQL, Analytics",
        "projects": "Business dashboard, forecasting project",
    }

    for line in run_pipeline(sample_data, profile):
        print(line)
