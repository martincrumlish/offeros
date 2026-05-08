import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
NODE_SCRIPT_COMMANDS = {"build-vsl"}


COMMANDS = {
    "init": ["init_offer_project.py"],
    "intake": ["init_offer_project.py"],
    "plan": ["build_visual_asset_plan.py", "--plan-only"],
    "build-assets": ["build_visual_asset_plan.py"],
    "build-sales-page": ["build_sales_page.py"],
    "build-emails": ["build_email_sequence.py"],
    "build-workbook": ["build_workbook.py"],
    "build-vsl": ["build_vsl_deck.js"],
    "build-dashboard": ["generate_delivery_dashboard.py"],
    "validate": ["validate_offer_outputs.py", "--strict"],
}


BUILD_ALL = [
    "build-assets",
    "build-sales-page",
    "build-emails",
    "build-workbook",
    "build-vsl",
    "build-dashboard",
    "validate",
]


def run_python(script_args: list[str], forwarded: list[str]) -> int:
    script = SCRIPT_ROOT / script_args[0]
    if not script.exists():
        raise SystemExit(f"OfferOS studio script not found: {script}")
    command = [sys.executable, str(script), *script_args[1:], *forwarded]
    return subprocess.run(command, check=False).returncode


def run_node(script_args: list[str], forwarded: list[str]) -> int:
    script = SCRIPT_ROOT / script_args[0]
    if not script.exists():
        raise SystemExit(f"OfferOS studio script not found: {script}")
    command = ["node", str(script), *script_args[1:], *forwarded]
    return subprocess.run(command, check=False).returncode


def run_command(name: str, forwarded: list[str]) -> int:
    if name == "build-all":
        for child in BUILD_ALL:
            code = run_command(child, forwarded)
            if code != 0:
                return code
        return 0
    script_args = COMMANDS.get(name)
    if not script_args:
        raise SystemExit(f"Unknown OfferOS command: {name}")
    if name in NODE_SCRIPT_COMMANDS:
        return run_node(script_args, forwarded)
    return run_python(script_args, forwarded)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OfferOS production studio dispatcher. Builders live in the plugin; generated projects contain source data and artifacts."
    )
    parser.add_argument("command", choices=sorted([*COMMANDS.keys(), "build-all"]))
    parser.add_argument(
        "--mode",
        default="guided",
        choices=["guided", "auto", "validate-only"],
        help="Run posture recorded for humans; source builders stay deterministic.",
    )
    args, forwarded = parser.parse_known_args()
    if args.command == "validate" or args.mode != "validate-only":
        return run_command(args.command, forwarded)
    return run_command("validate", forwarded)


if __name__ == "__main__":
    raise SystemExit(main())
