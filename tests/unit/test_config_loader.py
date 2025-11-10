"""
Unit tests for ConfigLoader.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

import pytest
import tempfile
from pathlib import Path

from pydantic import ValidationError
from src.core.config_loader import (
    ConfigLoader, DashboardConfig, PositionModel,
    ComponentConfigModel, PluginConfigModel
)


class TestPositionModel:
    """Test PositionModel validation"""

    def test_valid_position(self):
        """Test valid position"""
        pos = PositionModel(x=10, y=5, width=40, height=10)
        assert pos.x == 10
        assert pos.y == 5

    def test_negative_x_raises_error(self):
        """Test negative x raises ValidationError"""
        with pytest.raises(ValidationError):
            PositionModel(x=-1, y=5, width=40, height=10)

    def test_zero_width_raises_error(self):
        """Test zero width raises ValidationError"""
        with pytest.raises(ValidationError):
            PositionModel(x=0, y=0, width=0, height=10)


class TestComponentConfigModel:
    """Test ComponentConfigModel validation"""

    def test_valid_component_config(self):
        """Test valid component config"""
        config = ComponentConfigModel(
            type="runchart",
            title="Test Chart",
            position=PositionModel(x=0, y=0, width=40, height=10),
            rate_ms=1000,
            plugin="test_plugin",
            data_field="value"
        )
        assert config.type == "runchart"
        assert config.color == "white"  # default

    def test_invalid_component_type_raises_error(self):
        """Test invalid component type raises ValidationError"""
        with pytest.raises(ValidationError, match="Invalid component type"):
            ComponentConfigModel(
                type="invalid_type",
                title="Test",
                position=PositionModel(x=0, y=0, width=40, height=10),
                rate_ms=1000,
                plugin="test",
                data_field="value"
            )

    def test_negative_rate_ms_raises_error(self):
        """Test negative rate_ms raises ValidationError"""
        with pytest.raises(ValidationError):
            ComponentConfigModel(
                type="runchart",
                title="Test",
                position=PositionModel(x=0, y=0, width=40, height=10),
                rate_ms=-100,
                plugin="test",
                data_field="value"
            )


class TestDashboardConfig:
    """Test DashboardConfig validation"""

    def test_valid_dashboard_config(self):
        """Test valid dashboard config"""
        config = DashboardConfig(
            version="2.0",
            title="Test Dashboard",
            plugins=[
                PluginConfigModel(
                    name="test_plugin",
                    enabled=True,
                    module="src.plugins.test"
                )
            ],
            components=[
                ComponentConfigModel(
                    type="runchart",
                    title="Test",
                    position=PositionModel(x=0, y=0, width=40, height=10),
                    rate_ms=1000,
                    plugin="test_plugin",
                    data_field="value"
                )
            ]
        )
        assert config.version == "2.0"
        assert config.title == "Test Dashboard"
        assert len(config.plugins) == 1
        assert len(config.components) == 1

    def test_invalid_version_raises_error(self):
        """Test invalid version raises ValidationError"""
        with pytest.raises(ValidationError, match="must be 2.x"):
            DashboardConfig(
                version="1.0",
                title="Test"
            )

    def test_duplicate_plugin_names_raises_error(self):
        """Test duplicate plugin names raises ValidationError"""
        with pytest.raises(ValidationError, match="Duplicate plugin names"):
            DashboardConfig(
                version="2.0",
                title="Test",
                plugins=[
                    PluginConfigModel(name="plugin1", enabled=True, module="test"),
                    PluginConfigModel(name="plugin1", enabled=True, module="test2")
                ]
            )


class TestConfigLoader:
    """Test ConfigLoader file operations"""

    def test_load_nonexistent_file_raises_error(self):
        """Test loading nonexistent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            ConfigLoader.load("/nonexistent/config.yml")

    def test_load_valid_yaml(self):
        """Test loading valid YAML config"""
        yaml_content = """
version: '2.0'
title: 'Test Dashboard'
settings:
  refresh_rate_ms: 100
  terminal_size:
    width: 120
    height: 46
plugins:
  - name: test_plugin
    enabled: true
    module: src.plugins.test
components:
  - type: runchart
    title: Test Chart
    position:
      x: 0
      y: 0
      width: 40
      height: 10
    rate_ms: 1000
    plugin: test_plugin
    data_field: value
"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            config = ConfigLoader.load(temp_path)
            assert config.version == "2.0"
            assert config.title == "Test Dashboard"
            assert len(config.components) == 1
            assert config.components[0].type == "runchart"
        finally:
            Path(temp_path).unlink()

    def test_load_invalid_yaml_raises_error(self):
        """Test loading invalid YAML raises error"""
        yaml_content = """
version: '2.0'
title: 'Test'
invalid yaml: [unclosed bracket
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            with pytest.raises(Exception):  # yaml.YAMLError
                ConfigLoader.load(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_load_config_missing_required_fields(self):
        """Test loading config with missing required fields raises ValueError"""
        yaml_content = """
version: '2.0'
# Missing 'title' field
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="validation failed"):
                ConfigLoader.load(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_load_raw(self):
        """Test loading raw YAML without validation"""
        yaml_content = """
version: '2.0'
title: 'Test'
custom_field: 'allowed in raw mode'
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            raw = ConfigLoader.load_raw(temp_path)
            assert raw['version'] == '2.0'
            assert raw['title'] == 'Test'
            assert raw['custom_field'] == 'allowed in raw mode'
        finally:
            Path(temp_path).unlink()

    def test_validate(self):
        """Test validating raw config dict"""
        raw_config = {
            'version': '2.0',
            'title': 'Test Dashboard',
            'plugins': [],
            'components': []
        }

        config = ConfigLoader.validate(raw_config)
        assert isinstance(config, DashboardConfig)
        assert config.title == 'Test Dashboard'
