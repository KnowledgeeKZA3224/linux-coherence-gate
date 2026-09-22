#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="${1:-$(git rev-parse --short=12 HEAD)}"
OUT="dist"
NAME="sc-linux-coherence-gate-${VERSION}"
STAGE="${OUT}/${NAME}"

rm -rf "$STAGE"
mkdir -p "$STAGE"

cp -a README.md LIVE_PROOF.md HOW_IT_WORKS.md LICENSE "$STAGE"/
cp -a kernel_integration "$STAGE"/
cp -a distribution/DEPLOYMENT_BOUNDARY.md "$STAGE"/
cp -a distribution/INVARIANTS.json "$STAGE"/

COMMIT="$(git rev-parse HEAD)"
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cat > "$STAGE/RELEASE_RECEIPT.json" <<EOF
{
  "genesis_commit": "$COMMIT",
  "built_at_utc": "$UTC",
  "release_name": "$NAME",
  "purpose": "authorized defensive pre-execution governance distribution",
  "execution_rule": "Nothing executes until it proves itself."
}
EOF

find "$STAGE" -type f -print0 | sort -z | xargs -0 sha256sum > "$STAGE/MANIFEST.sha256"

tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner -czf "$OUT/$NAME.tar.gz" -C "$OUT" "$NAME"
sha256sum "$OUT/$NAME.tar.gz" > "$OUT/$NAME.tar.gz.sha256"

echo "artifact=$OUT/$NAME.tar.gz"
cat "$OUT/$NAME.tar.gz.sha256"
