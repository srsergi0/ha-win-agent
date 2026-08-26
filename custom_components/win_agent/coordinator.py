"""Data coordinator and event hub for Windows Direct Agent."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    EVENT_WIN_AGENT_COMMAND,
    EVENT_WIN_AGENT_TELEMETRY,
    EVENT_WIN_AGENT_STATE_UPDATE,
    SIGNAL_WIN_AGENT_UPDATE,
)

_LOGGER = logging.getLogger(__name__)

class WinAgentCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage inbound data from the Windows PC agent."""

    def __init__(self, hass: HomeAssistant, device_id: str, device_name: str) -> None:
        """Initialize the coordinator."""
        self.device_id = device_id
        self.device_name = device_name
        self.sensor_data: dict[str, Any] = {}
        self._unsub_telemetry: Any = None
        self._unsub_state: Any = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{device_id}",
        )

    async def async_setup(self) -> None:
        """Subscribe to Home Assistant event bus for incoming PC updates."""
        @callback
        def handle_telemetry_event(event: Event) -> None:
            data = event.data or {}
            target_id = data.get("device_id")
            if not target_id or target_id == self.device_id:
                incoming_sensors = data.get("sensors", {})
                self.sensor_data.update(incoming_sensors)
                self.async_set_updated_data(dict(self.sensor_data))
                async_dispatcher_send(self.hass, SIGNAL_WIN_AGENT_UPDATE.format(self.device_id))

        @callback
        def handle_state_update_event(event: Event) -> None:
            data = event.data or {}
            target_id = data.get("device_id")
            if not target_id or target_id == self.device_id:
                key = data.get("key") or data.get("entity_key")
                val = data.get("state") or data.get("value")
                if key is not None:
                    self.sensor_data[key] = val
                    self.async_set_updated_data(dict(self.sensor_data))
                    async_dispatcher_send(self.hass, SIGNAL_WIN_AGENT_UPDATE.format(self.device_id))

        self._unsub_telemetry = self.hass.bus.async_listen(
            EVENT_WIN_AGENT_TELEMETRY, handle_telemetry_event
        )
        self._unsub_state = self.hass.bus.async_listen(
            EVENT_WIN_AGENT_STATE_UPDATE, handle_state_update_event
        )

    def async_send_command(self, command: str, extra_data: dict[str, Any] | None = None) -> None:
        """Dispatch a command event on the Home Assistant Event Bus to be picked up by the PC."""
        event_payload = {
            "device_id": self.device_id,
            "command": command,
            **(extra_data or {}),
        }
        _LOGGER.debug("Firing win_agent_command event: %s", event_payload)
        self.hass.bus.async_fire(EVENT_WIN_AGENT_COMMAND, event_payload)

    def update_state_locally(self, key: str, value: Any) -> None:
        """Optimistically update local state."""
        self.sensor_data[key] = value
        self.async_set_updated_data(dict(self.sensor_data))
        async_dispatcher_send(self.hass, SIGNAL_WIN_AGENT_UPDATE.format(self.device_id))

    def cleanup(self) -> None:
        """Clean up listeners."""
        if self._unsub_telemetry:
            self._unsub_telemetry()
        if self._unsub_state:
            self._unsub_state()
