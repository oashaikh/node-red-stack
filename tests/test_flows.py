"""Validate that flows.json is structurally sound and references match up."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FLOWS = ROOT / "node-red-data" / "flows.json"


@pytest.fixture(scope="module")
def flows() -> list[dict]:
    return json.loads(FLOWS.read_text())


def test_flows_file_is_valid_json(flows: list[dict]) -> None:
    assert isinstance(flows, list)
    assert len(flows) > 0


def test_every_node_has_id_and_type(flows: list[dict]) -> None:
    for node in flows:
        assert "id" in node, f"node missing id: {node}"
        assert "type" in node, f"node missing type: {node['id']}"


def test_node_ids_are_unique(flows: list[dict]) -> None:
    ids = [n["id"] for n in flows]
    assert len(ids) == len(set(ids)), "duplicate node ids"


def test_wires_reference_existing_nodes(flows: list[dict]) -> None:
    ids = {n["id"] for n in flows}
    for node in flows:
        for wire_group in node.get("wires", []):
            for target in wire_group:
                assert target in ids, f"node {node['id']} wires to missing {target}"


def test_mqtt_nodes_reference_a_broker(flows: list[dict]) -> None:
    brokers = {n["id"] for n in flows if n["type"] == "mqtt-broker"}
    for node in flows:
        if node["type"] in {"mqtt in", "mqtt out"}:
            assert node["broker"] in brokers, (
                f"{node['type']} node {node['id']} references missing broker {node['broker']}"
            )


def test_each_flow_node_has_a_tab(flows: list[dict]) -> None:
    """Non-config nodes (anything with a .z attribute) must reference a tab."""
    tabs = {n["id"] for n in flows if n["type"] == "tab"}
    for node in flows:
        if "z" in node:
            assert node["z"] in tabs, f"{node['id']} z={node['z']} doesn't match any tab"
