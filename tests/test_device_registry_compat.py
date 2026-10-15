"""Regression checks for Home Assistant's single-config-entry DeviceEntry API."""

import ast
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / "custom_components/icloud3/utils/entity_reg_util.py"


def _source():
    return SOURCE.read_text(encoding="utf-8")


def test_deprecated_deviceentry_properties_are_not_used():
    """These properties are removed in HA 2027.10."""
    source = _source()
    assert "device_data.primary_config_entry" not in source
    assert "device_data.config_entries" not in source


def test_device_owner_guard_uses_single_config_entry_id():
    """Only react to registry updates belonging to iCloud3."""
    source = _source()
    assert "device_data.config_entry_id != Gb.config_entry_id" in source


def test_registry_snapshot_stores_config_entry_id_as_scalar():
    """Device registry metadata must store the string owner, not a set/list."""
    source = _source()
    assert "data_item['config_entry_id'] = device_data.config_entry_id" in source


def test_entity_registry_module_parses():
    ast.parse(_source(), filename=str(SOURCE))
