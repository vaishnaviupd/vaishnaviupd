import unittest

from src.internship_agent import Opportunity, RuleBasedFilter, run_pipeline


class RuleBasedFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.filter = RuleBasedFilter()

    def test_keeps_remote_internship(self) -> None:
        opp = Opportunity(
            source="board",
            role="Software Engineer Intern",
            company="Acme",
            url="https://example.com/1",
            remote_flag=True,
            description="Great internship for students",
        )
        self.assertTrue(self.filter.keep(opp))

    def test_rejects_non_remote_internship(self) -> None:
        opp = Opportunity(
            source="board",
            role="Data Analyst Intern",
            company="Acme",
            url="https://example.com/2",
            remote_flag=False,
            description="On-site internship",
        )
        self.assertFalse(self.filter.keep(opp))

    def test_rejects_senior_role_even_if_remote(self) -> None:
        opp = Opportunity(
            source="board",
            role="Senior Data Intern",
            company="Acme",
            url="https://example.com/3",
            remote_flag=True,
            description="Remote and distributed",
        )
        self.assertFalse(self.filter.keep(opp))


class PipelineTests(unittest.TestCase):
    def test_pipeline_generates_pending_approval_message(self) -> None:
        opportunities = [
            Opportunity(
                source="board",
                role="Business Analyst Intern",
                company="Beta",
                url="https://example.com/4",
                remote_flag=True,
                description="Remote internship role",
            )
        ]

        results = run_pipeline(opportunities, {"name": "Candidate"})

        self.assertEqual(results, ["Draft generated pending approval: Beta - Business Analyst Intern"])


if __name__ == "__main__":
    unittest.main()
