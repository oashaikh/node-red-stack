#!/usr/bin/env bash
# Pull the live flows.json out of the Node-RED container into source control.
# Usage: ./scripts/export-flows.sh
set -euo pipefail

container="${1:-nrs-node-red}"
target="node-red-data/flows.json"

docker cp "$container":/data/flows.json "$target"
echo "exported flows -> $target"
