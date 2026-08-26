"""The Windows Direct Agent integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    DEFAULT_DEVICE_ID,
    DEFAULT_NAME,
    EVENT_WIN_AGENT_COMMAND,
)
from .coordinator import WinAgentCoordinator

_LOGGER = logging.getLogger(__name__)

SERVICE_SHOW_DIALOG = "show_dialog"
SERVICE_SEND_NOTIFICATION = "send_notification"
SERVICE_LAUNCH_URL = "launch_url"
SERVICE_SEND_KEYS = "send_keys"
SERVICE_RUN_POWERSHELL = "run_powershell"

SCHEMA_SHOW_DIALOG = vol.Schema({
    vol.Required("title"): cv.string,
    vol.Required("message"): cv.string,
    vol.Optional("timeout_sec", default=30): cv.positive_int,
    vol.Optional("device_id"): cv.string,
    vol.Optional("buttons"): vol.All(cv.ensure_list, [vol.Schema({
        vol.Required("id"): cv.string,
        vol.Required("text"): cv.string,
        vol.Optional("style", default="Primary"): cv.string,
    })]),
})

SCHEMA_SEND_NOTIFICATION = vol.Schema({
    vol.Required("title"): cv.string,
    vol.Required("message"): cv.string,
    vol.Optional("device_id"): cv.string,
})

SCHEMA_LAUNCH_URL = vol.Schema({
    vol.Required("url"): cv.string,
    vol.Optional("device_id"): cv.string,
})

SCHEMA_SEND_KEYS = vol.Schema({
    vol.Required("keys"): cv.string,
    vol.Optional("device_id"): cv.string,
})

SCHEMA_RUN_POWERSHELL = vol.Schema({
    vol.Required("script"): cv.string,
    vol.Optional("device_id"): cv.string,
})

async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Windows Direct Agent component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Windows Direct Agent from a config entry."""
    device_id = entry.data.get(CONF_DEVICE_ID, DEFAULT_DEVICE_ID)
    device_name = entry.data.get(CONF_DEVICE_NAME, DEFAULT_NAME)

    coordinator = WinAgentCoordinator(hass, device_id, device_name)
    await coordinator.async_setup()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register custom services that broadcast to the PC
    def get_target_device_id(call_data: dict[str, Any]) -> str:
        return call_data.get("device_id") or device_id

    async def handle_show_dialog(call: ServiceCall) -> None:
        target = get_target_device_id(call.data)
        hass.bus.async_fire(EVENT_WIN_AGENT_COMMAND, {
            "device_id": target,
            "command": "show_dialog",
            "title": call.data["title"],
            "message": call.data["message"],
            "timeoutSec": call.data.get("timeout_sec", 30),
            "buttons": call.data.get("buttons"),
        })

    async def handle_send_notification(call: ServiceCall) -> None:
        target = get_target_device_id(call.data)
        hass.bus.async_fire(EVENT_WIN_AGENT_COMMAND, {
            "device_id": target,
            "command": "send_notification",
            "title": call.data["title"],
            "message": call.data["message"],
        })

    async def handle_launch_url(call: ServiceCall) -> None:
        target = get_target_device_id(call.data)
        hass.bus.async_fire(EVENT_WIN_AGENT_COMMAND, {
            "device_id": target,
            "command": "launch_url",
            "url": call.data["url"],
        })

    async def handle_send_keys(call: ServiceCall) -> None:
        target = get_target_device_id(call.data)
        hass.bus.async_fire(EVENT_WIN_AGENT_COMMAND, {
            "device_id": target,
            "command": "send_keys",
            "keys": call.data["keys"],
        })

    async def handle_run_powershell(call: ServiceCall) -> None:
        target = get_target_device_id(call.data)
        hass.bus.async_fire(EVENT_WIN_AGENT_COMMAND, {
            "device_id": target,
            "command": "run_powershell",
            "script": call.data["script"],
        })

    hass.services.async_register(DOMAIN, SERVICE_SHOW_DIALOG, handle_show_dialog, schema=SCHEMA_SHOW_DIALOG)
    hass.services.async_register(DOMAIN, SERVICE_SEND_NOTIFICATION, handle_send_notification, schema=SCHEMA_SEND_NOTIFICATION)
    hass.services.async_register(DOMAIN, SERVICE_LAUNCH_URL, handle_launch_url, schema=SCHEMA_LAUNCH_URL)
    hass.services.async_register(DOMAIN, SERVICE_SEND_KEYS, handle_send_keys, schema=SCHEMA_SEND_KEYS)
    hass.services.async_register(DOMAIN, SERVICE_RUN_POWERSHELL, handle_run_powershell, schema=SCHEMA_RUN_POWERSHELL)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator: WinAgentCoordinator = hass.data[DOMAIN].get(entry.entry_id)
    if coordinator:
        coordinator.cleanup()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
