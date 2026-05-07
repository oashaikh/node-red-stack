#!/usr/bin/env bash
# Push a local flows.json into the running Node-RED container and reload.
# Usage: ./scripts/import-flows.sh
set -euo pipefail

container="${1:-nrs-node-red}"
source="node-red-data/flows.json"

docker cp "$source" "$container":/data/flows.json
docker exec "$container" pkill -HUP node-red || true
echo "imported flows -> container $container; sent SIGHUP to reload"
