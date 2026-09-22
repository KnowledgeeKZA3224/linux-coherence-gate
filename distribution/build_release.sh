#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMMIT="$(git rev-parse HEAD)"
VERSION="${1:-$(git rev-parse --short=12 "$COMMIT")}"
SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-$(git show -s --format=%ct "$COMMIT")}"
UTC="$(date -u -d "@${SOURCE_DATE_EPOCH}" +%Y-%m-%dT%H:%M:%SZ)"

OUT="dist"
NAME="sc-linux-coherence-gate-${VERSION}"
STAGE="${OUT}/${NAME}"
ARTIFACT="${OUT}/${NAME}.tar.gz"

rm -rf "$STAGE"
mkdir -p "$STAGE"

cp -a README.md LIVE_PROOF.md HOW_IT_WORKS.md LICENSE "$STAGE"/
cp -a kernel_integration "$STAGE"/
cp -a distribution/DEPLOYMENT_BOUNDARY.md "$STAGE"/
cp -a distribution/INVARIANTS.json "$STAGE"/

cat > "$STAGE/RELEASE_RECEIPT.json" <<EOF
{
  "genesis_commit": "$COMMIT",
  "source_date_epoch": $SOURCE_DATE_EPOCH,
  "built_at_utc": "$UTC",
  "release_name": "$NAME",
  "purpose": "authorized defensive pre-execution governance distribution",
  "execution_rule": "Nothing executes until it proves itself."
}
EOF

(
  cd "$STAGE"
  find . -type f ! -name 'MANIFEST.sha256' -print0 |
    sort -z |
    xargs -0 sha256sum > MANIFEST.sha256
)

tar --sort=name --mtime="@${SOURCE_DATE_EPOCH}" --owner=0 --group=0 --numeric-owner -cf - -C "$OUT" "$NAME" |
  gzip -n > "$ARTIFACT"
sha256sum "$ARTIFACT" > "$ARTIFACT.sha256"

echo "artifact=$ARTIFACT"
cat "$ARTIFACT.sha256"
