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

cp -a   README.md DIGITAL_SOVEREIGNTY_BLUEPRINT.md HOW_IT_WORKS.md LIVE_PROOF.md   PRE_EXECUTION_GAP.md PATCH_NOTES.md LICENSE   SOURCE_REFERENCE.json PATCH_SHA256   sc_preexec_gate_v2.patch scctl.py sc_gatekeeper.py   install_local.sh verify_local.sh   "$STAGE"/
cp -a scpkg deploy tests kernel_integration "$STAGE"/
mkdir -p "$STAGE/distribution" "$STAGE/results"
cp -a   distribution/README.md distribution/DEPLOYMENT_BOUNDARY.md distribution/INVARIANTS.json   distribution/ansible distribution/puppet distribution/mirrors   "$STAGE/distribution"/
cp -a   results/SOURCE_LAYER_PROOF.json   results/SOURCE_LAYER_ARTIFACTS.sha256   "$STAGE/results"/

cat > "$STAGE/RELEASE_RECEIPT.json" <<EOF
{
  "genesis_commit": "$COMMIT",
  "source_date_epoch": ${SOURCE_DATE_EPOCH},
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
tar --sort=name   --mtime="@${SOURCE_DATE_EPOCH}"   --owner=0 --group=0 --numeric-owner   -cf - -C "$OUT" "$NAME" |
  gzip -n > "$ARTIFACT"

sha256sum "$ARTIFACT" > "$ARTIFACT.sha256"

echo "artifact=$ARTIFACT"
cat "$ARTIFACT.sha256"
