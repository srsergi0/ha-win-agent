"""Sensor platform for Windows Direct Agent."""
from __future__ import annotations

from typing import Any
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SIGNAL_WIN_AGENT_UPDATE
from .coordinator import WinAgentCoordinator

SENSOR_DESCRIPTIONS = [
    {
        "key": "cpu_load",
        "name": "CPU Load",
        "icon": "mdi:cpu-64-bit",
        "unit": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "memory_usage",
        "name": "Memory Usage",
        "icon": "mdi:memory",
        "unit": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "storage_usage",
        "name": "Primary Storage Usage",
        "icon": "mdi:harddisk",
        "unit": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "gpu_load",
        "name": "GPU Load",
        "icon": "mdi:expansion-card",
        "unit": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "battery_level",
        "name": "Battery Level",
        "icon": "mdi:battery",
        "unit": PERCENTAGE,
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "active_window",
        "name": "Active Window",
        "icon": "mdi:window-maximize",
    },
    {
        "key": "media_playing_info",
        "name": "Media Playing Info",
        "icon": "mdi:music",
    },
    {
        "key": "idle_time",
        "name": "User Idle Time",
        "icon": "mdi:timer-sand",
        "unit": UnitOfTime.SECONDS,
        "device_class": SensorDeviceClass.DURATION,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "network_ssid",
        "name": "Network SSID / Type",
        "icon": "mdi:wifi",
    },
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Windows Direct Agent sensors."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        WinAgentSensor(coordinator, desc)
        for desc in SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)

class WinAgentSensor(CoordinatorEntity[WinAgentCoordinator], SensorEntity):
    """Representation of a Windows Agent sensor."""

    def __init__(self, coordinator: WinAgentCoordinator, desc: dict[str, Any]) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.desc = desc
        self._key = desc["key"]
        self._attr_unique_id = f"{coordinator.device_id}_{self._key}"
        self._attr_name = f"{coordinator.device_name} {desc['name']}"
        self._attr_icon = desc.get("icon")
        self._attr_native_unit_of_measurement = desc.get("unit")
        self._attr_device_class = desc.get("device_class")
        self._attr_state_class = desc.get("state_class")

    async def async_added_to_hass(self) -> None:
        """Register dispatcher update callback."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_WIN_AGENT_UPDATE.format(self.coordinator.device_id),
                self._handle_update,
            )
        )

    def _handle_update(self) -> None:
        """Handle updated sensor data."""
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return information about the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.device_id)},
            name=self.coordinator.device_name,
            manufacturer="Custom WinAgent",
            model="Windows Direct Agent",
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return self.coordinator.sensor_data.get(self._key)
