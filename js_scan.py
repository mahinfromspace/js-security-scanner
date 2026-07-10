from pathlib import Path
import re
import sys


RISKY_PATTERNS = [
    ("document.write()", re.compile(r"\bdocument\s*\.\s*write\s*\(")),
    ("eval()", re.compile(r"\beval\s*\(")),
    ("innerHTML assignment", re.compile(r"\.\s*innerHTML\s*=")),
    ("Function() constructor", re.compile(r"\b(?:new\s+)?Function\s*\(")),
    # Final challenge rule: detects a direct variable or string passed to setTimeout.
    ("unsafe setTimeout()", re.compile(
        r"\bsetTimeout\s*\(\s*(?!\(?\s*(?:function\b|[A-Za-z_$][\w$]*\s*\)?\s*=>))(?:(?:[A-Za-z_$][\w$]*)|['\"])")),
]

SCANNED_EXTENSIONS = {".html", ".js"}
IGNORED_DIRECTORIES = {".git", "node_modules"}


def find_web_files(root):
    """Return all HTML and JavaScript files that should be scanned."""
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SCANNED_EXTENSIONS
        and not any(part in IGNORED_DIRECTORIES for part in path.parts)
    )


def scan_file(path):
    """Return every risky pattern found in one file."""
    findings = []
    text = path.read_text(encoding="utf-8", errors="ignore")

    for line_number, line in enumerate(text.splitlines(), start=1):
        code_only = line.split("//", 1)[0]
        for rule_name, pattern in RISKY_PATTERNS:
            if pattern.search(code_only):
                findings.append((line_number, rule_name, line.strip()))

    return findings


def main():
    root = Path(".")
    files = find_web_files(root)

    print(f"Scanning {len(files)} HTML/JavaScript file(s)...")
    all_findings = []

    for path in files:
        for line_number, rule_name, code in scan_file(path):
            all_findings.append((path, line_number, rule_name, code))

    if all_findings:
        print("\nSECURITY SCAN FAILED")
        for path, line_number, rule_name, code in all_findings:
            print(f"- {path}:{line_number} [{rule_name}] {code}")
        print(f"\nFound {len(all_findings)} risky pattern(s).")
        return 1

    print("SECURITY SCAN PASSED: no risky patterns were found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
