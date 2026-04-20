import importlib.util
import json
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "init-orch"
MODULE_LOADER = SourceFileLoader("init_orch_cli", str(MODULE_PATH))
MODULE_SPEC = importlib.util.spec_from_loader("init_orch_cli", MODULE_LOADER)
init_orch = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_LOADER.exec_module(init_orch)


class SuggestRefactorTests(unittest.TestCase):
    def make_repo(self, name: str = "example-repo") -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        repo_dir = Path(temp_dir.name) / name
        repo_dir.mkdir(parents=True)
        spec = init_orch.build_preset_spec(name, "engineering-generic")
        blueprint = init_orch.default_blueprint(name, "engineering-generic", spec)
        (repo_dir / "init-orch.md").write_text(blueprint, encoding="utf-8")
        return repo_dir

    def collect(self, repo_dir: Path) -> dict:
        return init_orch.collect_suggest_evidence(repo_dir, repo_dir / "init-orch.md")

    def test_orchestration_tier_outweighs_mixed_repo_heuristics(self) -> None:
        repo_dir = self.make_repo("qumatrix")
        (repo_dir / "README.md").write_text(
            "# qumatrix\n\nMixed workspace with some scripts and notes.\n",
            encoding="utf-8",
        )
        (repo_dir / "package.json").write_text(
            json.dumps({"name": "qumatrix", "scripts": {"test": "vitest"}}),
            encoding="utf-8",
        )
        (repo_dir / "AGENTS.md").write_text(
            "# Agent Operating Guide\n\n## Mission\n\nKeep the orchestration reviewable across Cursor and Claude.\n",
            encoding="utf-8",
        )
        (repo_dir / ".cursor" / "rules").mkdir(parents=True)
        (repo_dir / ".cursor" / "rules" / "workflow.mdc").write_text("workflow rule", encoding="utf-8")
        (repo_dir / "orch").mkdir(parents=True)
        (repo_dir / "orch" / "permissions.policy.json").write_text("{}", encoding="utf-8")

        evidence = self.collect(repo_dir)
        repo_brief = evidence["repoBrief"]
        suggestions = init_orch.generate_suggestions(repo_brief, evidence["rawSpec"], evidence["spec"])

        self.assertEqual(evidence["evidenceTiers"]["orchestration"]["weight"], 3)
        self.assertEqual(evidence["evidenceTiers"]["repo"]["weight"], 1)
        self.assertIn("init-orch.md", repo_brief["orchestrationFiles"])
        self.assertIn("AGENTS.md", repo_brief["orchestrationFiles"])
        self.assertNotIn("AGENTS.md", repo_brief["repoFiles"])
        self.assertEqual(repo_brief["repoShape"], "orchestration-aware tooling repo")
        self.assertIn("orchestration contract", repo_brief["repoIdentity"])
        self.assertIn("orchestration contract", suggestions["project"]["summary"])

    def test_docs_checks_stay_in_docs_verification(self) -> None:
        repo_dir = self.make_repo("init-orch")
        (repo_dir / "README.md").write_text("# init-orch\n\nTooling docs.\n", encoding="utf-8")
        (repo_dir / "init-orch").write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")

        evidence = self.collect(repo_dir)
        repo_brief = evidence["repoBrief"]
        verification, _confidence = init_orch.build_verification_suggestions(repo_brief, evidence["spec"])
        verification_by_type = {item["changeType"]: item["required"] for item in verification}

        self.assertIn("python3 -m py_compile ./init-orch", repo_brief["codeChecks"])
        self.assertIn("docs", verification_by_type)
        self.assertIn("code", verification_by_type)
        self.assertTrue(
            any("python3 -m py_compile ./init-orch" in requirement for requirement in verification_by_type["code"])
        )
        self.assertFalse(
            any("broken links" in requirement.lower() for requirement in verification_by_type["code"])
        )
        self.assertTrue(
            any("broken links" in requirement.lower() for requirement in verification_by_type["docs"])
        )

    def test_script_first_repo_brief_keeps_orchestration_identity_and_python_checks(self) -> None:
        repo_dir = self.make_repo("init-orch")
        (repo_dir / "README.md").write_text(
            "# init-orch\n\nRepository for experimenting with agent workflow setup.\n",
            encoding="utf-8",
        )
        (repo_dir / "init-orch").write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")
        (repo_dir / "AGENTS.md").write_text(
            "# Agent Operating Guide\n\n## Mission\n\nKeep generated setup aligned across agents.\n",
            encoding="utf-8",
        )
        (repo_dir / ".claude").mkdir(parents=True)
        (repo_dir / ".claude" / "settings.json").write_text("{}", encoding="utf-8")
        (repo_dir / "orch").mkdir(parents=True)
        (repo_dir / "orch" / "evaluation.plan.json").write_text("{}", encoding="utf-8")

        evidence = self.collect(repo_dir)
        repo_brief = evidence["repoBrief"]

        self.assertEqual(repo_brief["repoShape"], "orchestration-aware tooling repo")
        self.assertIn(".claude/", repo_brief["orchestrationArtifacts"])
        self.assertIn("orch/", repo_brief["orchestrationArtifacts"])
        self.assertTrue(
            "workflow setup" in repo_brief["repoIdentity"].lower()
            or "generated setup" in repo_brief["repoIdentity"].lower()
        )
        self.assertIn("python3 -m py_compile ./init-orch", repo_brief["codeChecks"])


if __name__ == "__main__":
    unittest.main()
