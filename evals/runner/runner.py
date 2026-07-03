"""Minimum viable cmmc-advisor eval runner.

Loads a scenario YAML, invokes Claude as the subject running the real
shipped skill: SKILL.md (frontmatter stripped) is the system prompt, the
repo root is the working directory, and Read/Grep/Glob are enabled so the
routing table actually exercises references/. Captures the answer and the
list of files the subject consulted, runs precheck, then invokes the
evaluator via scoring.py. Writes a results JSON to evals/results/.

Usage:
    python -m evals.runner.runner evals/scenarios/<scenario>.yaml

Defaults the rubric to evals/rubrics/cmmc-answer-quality.md. Override with
--rubric <path>.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from claude_agent_sdk import (
        query,
        ClaudeAgentOptions,
        AssistantMessage,
        TextBlock,
        ToolUseBlock,
        ResultMessage,
    )
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

from evals.runner.precheck import run_precheck
from evals.runner.scoring import score_response


SUBJECT_MODEL = "claude-opus-4-7"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUBRIC = REPO_ROOT / "evals" / "rubrics" / "cmmc-answer-quality.md"
RESULTS_DIR = REPO_ROOT / "evals" / "results"


REQUIRED_SCENARIO_KEYS = ("id", "prompt")


def _load_scenario(path: Path) -> dict:
    with path.open() as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"scenario file {path} did not parse to a dict")
    missing = [k for k in REQUIRED_SCENARIO_KEYS if k not in data or not data[k]]
    if missing:
        raise ValueError(
            f"scenario file {path} is missing required keys: {missing}"
        )
    return data


def _load_rubric(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_skill_system_prompt() -> str:
    """The real SKILL.md body, frontmatter stripped, so the subject runs
    exactly what production users install."""
    text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return text.strip()


async def _invoke_subject(prompt: str) -> tuple[str, list[str]]:
    if not SDK_AVAILABLE:
        raise RuntimeError(
            "claude-agent-sdk not installed. Run pip install -r requirements.txt"
        )
    options = ClaudeAgentOptions(
        model=SUBJECT_MODEL,
        system_prompt=_load_skill_system_prompt(),
        cwd=str(REPO_ROOT),
        allowed_tools=["Read", "Grep", "Glob"],
        permission_mode="default",  # allowed_tools covers the read-only set;
        # bypassPermissions is rejected when the harness runs as root
        max_turns=25,
    )
    chunks: list[str] = []
    files_consulted: list[str] = []
    final_result: str | None = None
    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    chunks.append(block.text)
                elif isinstance(block, ToolUseBlock) and block.name == "Read":
                    fp = (block.input or {}).get("file_path")
                    if fp:
                        files_consulted.append(fp)
        elif isinstance(msg, ResultMessage):
            final_result = getattr(msg, "result", None)
    return (final_result or "".join(chunks)), files_consulted


async def run_scenario(scenario_path: Path, rubric_path: Path) -> dict:
    scenario = _load_scenario(scenario_path)
    rubric = _load_rubric(rubric_path)

    print(f"[runner] scenario: {scenario.get('id')}")
    print(f"[runner] invoking subject ({SUBJECT_MODEL})...")
    response, files_consulted = await _invoke_subject(scenario["prompt"])
    print(f"[runner] subject response: {len(response)} chars")
    print(f"[runner] files consulted: {len(files_consulted)}")

    precheck = run_precheck(response, scenario)
    print(f"[runner] precheck hard_fail_flags: {precheck['hard_fail_flags'] or '(none)'}")

    print(f"[runner] invoking evaluator...")
    score = await score_response(scenario, response, rubric, precheck)
    print(
        f"[runner] score: weighted={score.weighted:.2f} passed={score.passed} "
        f"hard_fail={score.hard_fail_flag or '(none)'}"
    )

    return {
        "scenario_id": scenario.get("id"),
        "scenario_path": str(scenario_path),
        "rubric_path": str(rubric_path),
        "subject_model": SUBJECT_MODEL,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "files_consulted": files_consulted,
        "response": response,
        "precheck": precheck,
        "score": asdict(score),
    }


def _write_result(result: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    sid = result.get("scenario_id", "unknown")
    path = out_dir / f"{ts}-{sid}.json"
    path.write_text(json.dumps(result, indent=2, default=str))
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="cmmc-advisor eval runner")
    parser.add_argument("scenario", type=Path, help="path to scenario YAML")
    parser.add_argument(
        "--rubric",
        type=Path,
        default=DEFAULT_RUBRIC,
        help=f"path to rubric markdown (default: {DEFAULT_RUBRIC.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=RESULTS_DIR,
        help=f"results directory (default: {RESULTS_DIR.relative_to(REPO_ROOT)})",
    )
    args = parser.parse_args()

    if not args.scenario.exists():
        print(f"scenario not found: {args.scenario}", file=sys.stderr)
        return 1
    if not args.rubric.exists():
        print(f"rubric not found: {args.rubric}", file=sys.stderr)
        return 1

    result = asyncio.run(run_scenario(args.scenario, args.rubric))
    out_path = _write_result(result, args.out_dir)
    print(f"[runner] wrote {out_path.relative_to(REPO_ROOT)}")
    return 0 if result["score"]["passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
