#!/usr/bin/env bash
set -euo pipefail

if (( $# > 1 )); then
  echo "Usage: $0 [output.zip]" >&2
  exit 2
fi

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - "$repo_dir" "${1:-}" <<'PY'
import json
import sys
import zipfile
from pathlib import Path

root = Path(sys.argv[1])
manifest = json.loads((root / "plugin.json").read_text())
output = Path(sys.argv[2]) if sys.argv[2] else (
    root / "dist" / f"spryx-openai-{manifest['version']}.zip"
)
if output.suffix.lower() != ".zip":
    raise SystemExit("Output must be a .zip file")

# Explicit allowlist: local files and future components are never bundled by accident.
files = ["plugin.json", "mcp.json", "assets/icon.png", "README.md", "LICENSE"]
files += [f"skills/{name}/SKILL.md" for name in (
    "spryx-get-started", "spryx-inbox-triage", "spryx-pipeline-review",
    "spryx-account-brief", "spryx-task-follow-ups",
)]
for name in files:
    path = root / name
    if not path.is_file() or path.is_symlink():
        raise SystemExit(f"Expected a regular package file: {name}")

output.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in sorted(files):
        info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, (root / name).read_bytes())
print(output.resolve())
PY
