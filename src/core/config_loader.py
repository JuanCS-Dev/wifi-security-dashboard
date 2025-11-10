"""
YAML configuration loader with Pydantic validation.

This module handles loading, parsing, and validating dashboard configuration
from YAML files. Uses Pydantic for robust schema validation.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-09
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from pydantic import BaseModel, Field, field_validator, ValidationError


class PositionModel(BaseModel):
    """Position configuration model"""
    x: int = Field(ge=0, description="X coordinate (column)")
    y: int = Field(ge=0, description="Y coordinate (row)")
    width: int = Field(gt=0, description="Width in characters")
    height: int = Field(gt=0, description="Height in lines")


class TriggerConfigModel(BaseModel):
    """Trigger configuration model"""
    title: str = Field(min_length=1, description="Trigger description")
    condition: str = Field(min_length=1, description="Shell command condition")
    actions: Dict[str, Any] = Field(default_factory=dict, description="Trigger actions")


class ComponentConfigModel(BaseModel):
    """Component configuration model"""
    type: str = Field(description="Component type (runchart, sparkline, etc.)")
    title: str = Field(description="Component title")
    position: PositionModel = Field(description="Position and size")
    rate_ms: int = Field(ge=0, description="Update interval in milliseconds")
    plugin: str = Field(min_length=1, description="Plugin name")
    data_field: str = Field(min_length=1, description="Data field name")
    color: str = Field(default="white", description="Border/accent color")
    triggers: List[TriggerConfigModel] = Field(default_factory=list, description="Triggers")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Extra config")

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Validate component type"""
        valid_types = {
            'runchart', 'sparkline', 'barchart', 'gauge',
            'textbox', 'table', 'asciibox'
        }
        if v not in valid_types:
            raise ValueError(f"Invalid component type '{v}'. Must be one of: {valid_types}")
        return v


class PluginConfigModel(BaseModel):
    """Plugin configuration model"""
    name: str = Field(min_length=1, description="Plugin name")
    enabled: bool = Field(default=True, description="Enable/disable plugin")
    module: str = Field(min_length=1, description="Python module path")
    config: Dict[str, Any] = Field(default_factory=dict, description="Plugin-specific config")


class TerminalSizeModel(BaseModel):
    """Terminal size configuration"""
    width: int = Field(default=120, gt=0, description="Terminal width")
    height: int = Field(default=46, gt=0, description="Terminal height")


class SettingsModel(BaseModel):
    """Dashboard settings model"""
    refresh_rate_ms: int = Field(default=100, ge=10, le=1000, description="UI refresh rate")
    terminal_size: TerminalSizeModel = Field(default_factory=TerminalSizeModel)
    theme: str = Field(default="default", description="Color theme")
    educational_mode: bool = Field(default=True, description="Enable educational features")
    max_event_history: int = Field(
        default=100,
        ge=10,
        le=10000,
        description="Maximum number of events to keep in history (for debugging)"
    )


class EducationalConfigModel(BaseModel):
    """Educational mode configuration"""
    enabled: bool = Field(default=True, description="Enable educational mode")
    tips_file: str = Field(default="config/educational/tips.yml", description="Tips file path")
    overlay_key: str = Field(default="?", description="Key to show help overlay")
    auto_rotate: bool = Field(default=True, description="Auto-rotate tips")
    rotation_interval: int = Field(default=30000, ge=1000, description="Rotation interval (ms)")


class KeyboardConfigModel(BaseModel):
    """Keyboard shortcuts configuration"""
    quit: str = Field(default="q", description="Quit key")
    pause: str = Field(default="p", description="Pause key")
    help: str = Field(default="?", description="Help key")
    next_page: str = Field(default="n", description="Next page key")
    prev_page: str = Field(default="b", description="Previous page key")
    toggle_educational: str = Field(default="e", description="Toggle educational mode")


class DashboardConfig(BaseModel):
    """
    Main dashboard configuration model.

    This is the root configuration object that encompasses all settings,
    plugins, and components for the dashboard.
    """
    version: str = Field(description="Config version")
    title: str = Field(description="Dashboard title")
    settings: SettingsModel = Field(default_factory=SettingsModel)
    plugins: List[PluginConfigModel] = Field(default_factory=list, description="Plugin configs")
    components: List[ComponentConfigModel] = Field(default_factory=list, description="Components")
    educational: EducationalConfigModel = Field(
        default_factory=EducationalConfigModel,
        description="Educational mode config"
    )
    keyboard: KeyboardConfigModel = Field(
        default_factory=KeyboardConfigModel,
        description="Keyboard shortcuts"
    )

    @field_validator('version')
    @classmethod
    def validate_version(cls, v):
        """Validate version format"""
        if not v.startswith('2.'):
            raise ValueError(f"Config version must be 2.x, got '{v}'")
        return v

    @field_validator('plugins')
    @classmethod
    def validate_plugins_unique(cls, v):
        """Ensure plugin names are unique"""
        names = [p.name for p in v]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(f"Duplicate plugin names found: {set(duplicates)}")
        return v


class ConfigLoader:
    """
    YAML configuration loader with validation.

    This class handles loading dashboard configuration from YAML files
    and validating them using Pydantic models.

    Example:
        >>> config = ConfigLoader.load('config/dashboard.yml')
        >>> print(config.title)
        'WiFi Security Dashboard'
        >>> for plugin in config.plugins:
        ...     print(plugin.name)
    """

    @staticmethod
    def load(config_path: str) -> DashboardConfig:
        """
        Load and validate dashboard configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            Validated DashboardConfig object

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is malformed
            ValidationError: If config doesn't match schema
        """
        path = Path(config_path)

        # Check file exists
        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                f"Expected location: {path.absolute()}"
            )

        # Load YAML
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(
                f"Failed to parse YAML configuration:\n{e}"
            )

        # Validate with Pydantic
        try:
            config = DashboardConfig(**raw_config)
        except ValidationError as e:
            # Format validation errors nicely
            errors = []
            for error in e.errors():
                field = ' -> '.join(str(loc) for loc in error['loc'])
                msg = error['msg']
                errors.append(f"  - {field}: {msg}")

            # Re-raise with formatted message
            raise ValueError(
                f"Configuration validation failed:\n" + '\n'.join(errors)
            ) from e

        return config

    @staticmethod
    def load_raw(config_path: str) -> Dict[str, Any]:
        """
        Load raw YAML without validation (for debugging).

        Args:
            config_path: Path to YAML file

        Returns:
            Raw dictionary from YAML

        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def validate(raw_config: Dict[str, Any]) -> DashboardConfig:
        """
        Validate raw config dictionary.

        Args:
            raw_config: Raw configuration dictionary

        Returns:
            Validated DashboardConfig

        Raises:
            ValidationError: If validation fails
        """
        return DashboardConfig(**raw_config)
