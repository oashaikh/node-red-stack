# node-red-stack

A drop-in **Node-RED + Mosquitto** stack you can clone into any project as
the local automation layer for IoT prototyping or device-in-the-loop test
rigs.

## What this repo does

- Boots Node-RED and Mosquitto via docker-compose, on a shared network so
  Node-RED can address Mosquitto at `mosquitto:1883`.
- Tracks `flows.json` in source control so the automation logic ships with
  the repo (instead of living only inside the container's volume).
- Tracks `settings.js` in source control so editor + auth + logging behaviour
  is reproducible.
- Includes scripts to push/pull `flows.json` between local disk and the
  container so an editor-driven workflow stays in sync with git.
- Ships pytest tests that validate `flows.json` structurally — IDs unique,
  wires resolve, MQTT nodes reference a real broker, every flow node sits on
  a tab. Catches the kinds of breakage that only show up when you import on
  a fresh machine.

## Project layout

- `docker-compose.yml` - Node-RED + Mosquitto with healthcheck.
- `node-red-data/`
  - `flows.json` - the actual automation. Tracked.
  - `settings.js` - Node-RED runtime settings. Tracked.
  - `.config*.json`, `lib/`, etc. - generated, .gitignored.
- `mosquitto/config/mosquitto.conf` - dev-only broker config.
- `scripts/export-flows.sh` - container -> git.
- `scripts/import-flows.sh` - git -> container.
- `tests/test_flows.py` - structural validation of flows.json.

## Quick start

```bash
cp .env.example .env                 # set CREDENTIAL_SECRET if you'll use creds
docker compose up -d
open http://localhost:1880           # Node-RED editor
```

The sample flow:
- subscribes to `home/+/temp` and prints to debug,
- injects a fake `home/test/temp` reading every 30s and publishes it to MQTT.

You should see your own publishes echo back through the subscription.

## Editor-driven workflow

1. Edit flows in the browser (http://localhost:1880).
2. Hit **Deploy** in the editor.
3. Pull the result back into git:

   ```bash
   make export    # -> node-red-data/flows.json
   git diff       # see what changed
   ```

If a teammate updates the flow:

```bash
git pull
make import      # push the new flows.json into the running container
```

## Connecting your own publishers/subscribers

From the host, point any MQTT client at `localhost:1883`:

```bash
mosquitto_sub -h localhost -p 1883 -t "home/#"
mosquitto_pub -h localhost -p 1883 -t "home/kitchen/temp" -m '{"temp_c":21.4}'
```

From another container on the same docker network, use `mosquitto:1883`.

## Running the validation tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

These tests run without docker — they only inspect `flows.json` structurally.
Worth running in CI before any deploy.

## Why bother tracking settings.js and flows.json

Node-RED's default workflow keeps both in a Docker volume, which means:
- Flows live outside source control (no review, no rollback, no diff).
- Reproducing a working stack on a fresh machine means re-clicking the UI.
- Recovery from a corrupted volume means rebuilding from memory.

Tracking them in git solves all three. The tradeoff is that flows.json
changes on every UI deploy — accept that and get used to `make export`
becoming part of your commit ritual.

## Security note

The default `mosquitto.conf` is `allow_anonymous true` for local dev. Before
exposing the broker beyond `localhost`, switch to a `password_file` and
disable anonymous. Same goes for Node-RED — set up `adminAuth` in
`settings.js` if anyone other than you can reach port 1880.
