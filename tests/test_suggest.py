import contextlib
import importlib.util
import io
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

    def write_blueprint(self, repo_dir: Path, spec: dict) -> None:
        blueprint = init_orch.default_blueprint(repo_dir.name, spec["preset"], spec)
        (repo_dir / "init-orch.md").write_text(blueprint, encoding="utf-8")

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

    def test_dotfiles_do_not_count_as_python_entrypoints(self) -> None:
        repo_dir = self.make_repo("qmon_sindy")
        (repo_dir / ".gitignore").write_text("# Python\n__pycache__/\n", encoding="utf-8")

        self.assertFalse(init_orch.has_python_shebang(repo_dir / ".gitignore"))
        self.assertEqual(init_orch.detect_python_entrypoint(repo_dir), "")

    def test_python_repo_with_tests_and_pytest_docs_prefers_pytest_check(self) -> None:
        repo_dir = self.make_repo("qmon_sindy")
        (repo_dir / "README.md").write_text(
            "# qmon_sindy\n\nThis repo uses pytest for the test suite.\n",
            encoding="utf-8",
        )
        (repo_dir / "tests").mkdir()
        (repo_dir / "setup.py").write_text("from setuptools import setup\n", encoding="utf-8")
        (repo_dir / ".gitignore").write_text("# Python\n__pycache__/\n", encoding="utf-8")

        evidence = self.collect(repo_dir)
        repo_brief = evidence["repoBrief"]
        verification, _confidence = init_orch.build_verification_suggestions(repo_brief, evidence["spec"])

        self.assertIn("pytest", repo_brief["codeChecks"])
        self.assertNotIn("python3 -m py_compile ./.gitignore", repo_brief["codeChecks"])
        self.assertTrue(any("Run `pytest`" in requirement for item in verification for requirement in item["required"]))

    def test_package_json_without_test_script_does_not_infer_npm_test(self) -> None:
        repo_dir = self.make_repo("webby")
        (repo_dir / "package.json").write_text(
            json.dumps({"name": "webby", "scripts": {"lint": "eslint ."}}),
            encoding="utf-8",
        )

        evidence = self.collect(repo_dir)
        repo_hints = evidence["repoHints"]
        repo_brief = evidence["repoBrief"]

        self.assertEqual(repo_hints["suggestedCheck"], "npm run lint")
        self.assertNotIn("npm test", repo_brief["codeChecks"])
        self.assertIn("npm run lint", repo_brief["codeChecks"])

    def test_makefile_without_test_target_does_not_infer_make_test(self) -> None:
        repo_dir = self.make_repo("maker")
        (repo_dir / "Makefile").write_text("build:\n\tpython3 -m build\n", encoding="utf-8")

        evidence = self.collect(repo_dir)
        repo_hints = evidence["repoHints"]

        self.assertNotIn("make test", repo_hints["suggestedChecks"])
        self.assertNotEqual(repo_hints["suggestedCheck"], "make test")

    def test_pnpm_script_commands_are_used_when_present(self) -> None:
        repo_dir = self.make_repo("frontend")
        (repo_dir / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
        (repo_dir / "package.json").write_text(
            json.dumps({"name": "frontend", "scripts": {"test": "vitest run", "lint": "eslint ."}}),
            encoding="utf-8",
        )

        evidence = self.collect(repo_dir)
        repo_brief = evidence["repoBrief"]

        self.assertEqual(evidence["repoHints"]["suggestedCheck"], "pnpm test")
        self.assertEqual(repo_brief["codeChecks"][0], "pnpm test")
        self.assertIn("pnpm lint", repo_brief["codeChecks"])

    def test_ci_test_command_beats_python_compile_fallback(self) -> None:
        repo_dir = self.make_repo("scripty")
        (repo_dir / "scripty").write_text("#!/usr/bin/env python3\nprint('ok')\n", encoding="utf-8")
        (repo_dir / ".github" / "workflows").mkdir(parents=True)
        (repo_dir / ".github" / "workflows" / "ci.yml").write_text(
            "jobs:\n"
            "  test:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: pytest -q\n",
            encoding="utf-8",
        )

        evidence = self.collect(repo_dir)
        repo_brief = evidence["repoBrief"]

        self.assertEqual(evidence["repoHints"]["suggestedCheck"], "pytest -q")
        self.assertEqual(repo_brief["codeChecks"][0], "pytest -q")
        self.assertIn("python3 -m py_compile ./scripty", repo_brief["codeChecks"])

    def test_low_confidence_summary_becomes_question_not_auto_update(self) -> None:
        repo_dir = self.make_repo("mystery-repo")
        raw_spec = init_orch.base_blueprint_spec("mystery-repo")
        raw_spec["preset"] = "engineering-generic"
        raw_spec["workflowPreset"] = "engineering"
        raw_spec["domainPreset"] = "generic"
        self.write_blueprint(repo_dir, raw_spec)

        evidence = self.collect(repo_dir)
        suggestions = init_orch.generate_suggestions(evidence["repoBrief"], evidence["rawSpec"], evidence["spec"])

        self.assertEqual(suggestions["confidence"]["summary"], "low")
        self.assertNotIn("summary", suggestions["project"])
        self.assertIn(
            "Should the project summary emphasize the runtime, the workflow model, or the target ecosystems most strongly?",
            suggestions["questions"],
        )

    def test_suggestion_report_includes_evidence_and_rationale(self) -> None:
        repo_dir = self.make_repo("frontend")
        (repo_dir / "package.json").write_text(
            json.dumps({"name": "frontend", "scripts": {"test": "vitest run"}}),
            encoding="utf-8",
        )

        evidence = self.collect(repo_dir)
        suggestions = init_orch.generate_suggestions(evidence["repoBrief"], evidence["rawSpec"], evidence["spec"])
        report = init_orch.format_suggestion_report(evidence["repoBrief"], suggestions, evidence["spec"])

        self.assertIn("Evidence summary:", report)
        self.assertIn("- verification:", report)
        self.assertIn("why:", report)
        self.assertIn("evidence categories:", report)

    def test_rendered_agents_markdown_keeps_clean_bullets(self) -> None:
        spec = init_orch.normalize_spec(init_orch.build_preset_spec("qmon_sindy", "engineering-generic"))
        rendered = init_orch.render_agents_file(spec, {"items": [], "summary": "", "version": 1})

        self.assertIn("\n- Keep guidance easy for humans to update.\n", rendered)
        self.assertIn("\n- `implementer`: Make focused code changes and verify the result.\n", rendered)
        self.assertNotIn("\n        - `implementer`", rendered)
        self.assertIn("Generated from `init-orch.md`. Do not edit directly.", rendered)
        self.assertNotIn("## Role Responsibilities", rendered)
        self.assertNotIn("## Imported Capabilities", rendered)

    def test_default_presets_start_with_find_skills_import_template(self) -> None:
        engineering = init_orch.build_preset_spec("demo", "engineering-generic")
        web_app = init_orch.build_preset_spec("demo", "engineering-web-app")

        for spec in (engineering, web_app):
            self.assertEqual(len(spec["imports"]), 1)
            self.assertEqual(spec["imports"][0]["id"], "find-skills")
            self.assertEqual(spec["imports"][0]["type"], "skillPack")
            self.assertEqual(spec["imports"][0]["source"], "https://skills.sh/vercel-labs/skills/find-skills")

    def test_default_blueprint_emphasizes_priority_order_and_render_loop(self) -> None:
        blueprint = init_orch.default_blueprint("demo", "engineering-generic")

        self.assertIn("The top-level JSON keys below follow the same order", blueprint)
        self.assertIn("The default `find-skills` entry is an optional template you can keep, copy, or delete.", blueprint)
        self.assertIn("## Render Loop", blueprint)
        self.assertNotIn("## Workflow\n\n1. Review or edit the spec block above only if you want to override the defaults.", blueprint)
        self.assertIn('"id": "find-skills"', blueprint)
        self.assertIn("Optional template import for external skills.", blueprint)

    def test_render_targets_dry_run_does_not_write_files(self) -> None:
        repo_dir = self.make_repo("dry-run-demo")
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = init_orch.render_targets(
                repo_dir,
                ["cursor"],
                repo_dir / "init-orch.md",
                dry_run=True,
            )

        self.assertTrue(result["dryRun"])
        self.assertIn("Zubeldia render dry-run", output.getvalue())
        self.assertFalse((repo_dir / ".cursor").exists())
        self.assertNotIn('"lastRenderedAt": "DRY_RUN"', (repo_dir / "init-orch.md").read_text(encoding="utf-8"))

    def test_choose_refinement_fields_skips_known_answers_by_default(self) -> None:
        existing_notes = {
            "commonWork": "small bug fixes",
            "primaryVerification": "pytest -q",
            "sensitivePaths": "infra/",
            "existingConventions": "",
        }
        repo_hints = {"suggestedCheck": "pytest -q"}

        fields = init_orch.refinement_field_specs(existing_notes, repo_hints)
        pending = init_orch.choose_refinement_fields(fields, update_existing=False)

        self.assertEqual([field["key"] for field in pending], ["existingConventions"])

    def test_review_suppresses_unchanged_setup_recommendations(self) -> None:
        repo_dir = self.make_repo("review-demo")
        init_orch.render_targets(repo_dir, ["cursor"], repo_dir / "init-orch.md")

        report = init_orch.review_blueprint(repo_dir, repo_dir / "init-orch.md")

        self.assertNotIn("unchanged recommendation(s) suppressed", report)
        self.assertIn("No major recommendations right now.", report)
        self.assertNotIn("1. Review imported capability `paperclip`", report)
        self.assertIn("Parity:", report)
        self.assertIn("target-specific drift:", report)

    def test_parity_report_explains_shared_and_target_specific_outputs(self) -> None:
        repo_dir = self.make_repo("parity-demo")
        init_orch.render_targets(repo_dir, ["cursor"], repo_dir / "init-orch.md")
        blueprint_text = (repo_dir / "init-orch.md").read_text(encoding="utf-8")
        raw_spec = init_orch.parse_blueprint_block(blueprint_text, init_orch.SPEC_MARKERS, "spec")
        spec = init_orch.normalize_spec(raw_spec)
        metadata = init_orch.load_generated_metadata(blueprint_text)

        snapshot = init_orch.build_parity_snapshot(repo_dir, spec, metadata)
        report = init_orch.format_parity_report(repo_dir, spec, metadata, snapshot)

        self.assertIn("Shared source of truth:", report)
        self.assertIn("Target-specific outputs:", report)
        self.assertIn(".cursor/rules/core.mdc", report)
        self.assertIn(".claude/settings.json", report)
        self.assertIn("Not yet rendered for: claude", report)

    def test_response_style_defaults_exist_in_normalized_spec(self) -> None:
        spec = init_orch.normalize_spec(init_orch.build_preset_spec("demo", "engineering-generic"))

        self.assertEqual(spec["responseStyle"]["tone"], "direct")
        self.assertEqual(spec["responseStyle"]["verbosity"], "balanced")
        self.assertEqual(spec["responseStyle"]["structure"], "answer-first")
        self.assertEqual(spec["responseStyle"]["defaultLength"], "short")
        self.assertTrue(spec["responseStyle"]["rules"])
        self.assertTrue(spec["responseStyle"]["examples"])

    def test_response_style_profiles_differ_by_preset(self) -> None:
        engineering = init_orch.normalize_spec(init_orch.build_preset_spec("demo", "engineering-generic"))
        research = init_orch.normalize_spec(init_orch.build_preset_spec("demo", "research-generic"))
        docs = init_orch.normalize_spec(init_orch.build_preset_spec("demo", "engineering-docs"))

        self.assertEqual(engineering["responseStyle"]["tone"], "direct")
        self.assertEqual(engineering["responseStyle"]["structure"], "answer-first")

        self.assertEqual(research["responseStyle"]["tone"], "analytical")
        self.assertEqual(research["responseStyle"]["verbosity"], "detailed")
        self.assertEqual(research["responseStyle"]["structure"], "findings-first")
        self.assertTrue(
            any("Separate findings, hypotheses, assumptions, and open questions explicitly." in rule for rule in research["responseStyle"]["rules"])
        )

        self.assertEqual(docs["responseStyle"]["tone"], "editorial")
        self.assertEqual(docs["responseStyle"]["structure"], "reader-first")
        self.assertTrue(
            any("Prefer concrete wording, examples, and scannable structure over abstract commentary." in rule for rule in docs["responseStyle"]["rules"])
        )

        self.assertNotEqual(engineering["responseStyle"]["tone"], research["responseStyle"]["tone"])
        self.assertNotEqual(engineering["responseStyle"]["tone"], docs["responseStyle"]["tone"])

    def test_response_style_rendering_reflects_preset_bias(self) -> None:
        research = init_orch.normalize_spec(init_orch.build_preset_spec("demo", "research-generic"))
        docs = init_orch.normalize_spec(init_orch.build_preset_spec("demo", "engineering-docs"))

        research_rendered = init_orch.render_claude_rule(research)
        docs_rendered = init_orch.render_cursor_core_rule(docs)

        self.assertIn("- Tone: analytical", research_rendered)
        self.assertIn("- Structure: findings-first", research_rendered)
        self.assertIn("Separate findings, hypotheses, assumptions, and open questions explicitly.", research_rendered)

        self.assertIn("- Tone: editorial", docs_rendered)
        self.assertIn("- Structure: reader-first", docs_rendered)
        self.assertIn("Prefer concrete wording, examples, and scannable structure over abstract commentary.", docs_rendered)

    def test_response_style_renders_into_generated_guidance(self) -> None:
        raw_spec = init_orch.build_preset_spec("demo", "engineering-generic")
        raw_spec["responseStyle"] = {
            "tone": "terse",
            "verbosity": "low",
            "structure": "answer-first",
            "defaultLength": "very-short",
            "rules": [
                "Lead with the answer.",
                "Drop filler and pleasantries.",
            ],
            "examples": [
                "Do: `Bug in auth middleware. Fix <= check.`",
                "Avoid: `Sure, I'd be happy to help...`",
            ],
        }
        spec = init_orch.normalize_spec(raw_spec)

        agents = init_orch.render_agents_file(spec, {"items": [], "summary": "", "version": 1})
        cursor_core = init_orch.render_cursor_core_rule(spec)
        claude_rule = init_orch.render_claude_rule(spec)

        for rendered in (agents, cursor_core, claude_rule):
            self.assertIn("## Response Style", rendered)
            self.assertIn("- Tone: terse", rendered)
            self.assertIn("- Verbosity: low", rendered)
            self.assertIn("- Structure: answer-first", rendered)
            self.assertIn("- Default length: very-short", rendered)
            self.assertIn("Lead with the answer.", rendered)
            self.assertIn("Drop filler and pleasantries.", rendered)
            self.assertIn("Bug in auth middleware. Fix <= check.", rendered)


if __name__ == "__main__":
    unittest.main()
