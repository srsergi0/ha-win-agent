"""Config flow for Windows Direct Agent integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    DEFAULT_PORT,
    DEFAULT_NAME,
)

_LOGGER = logging.getLogger(__name__)

class WinAgentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Windows Direct Agent."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            device_name = user_input.get(CONF_DEVICE_NAME, DEFAULT_NAME)
            device_id = user_input.get(CONF_DEVICE_ID)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://{host}:{port}/api/status", timeout=aiohttp.ClientTimeout(total=4)) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if not device_id:
                                device_id = data.get("device", {}).get("id", "win_pc")
                            if not device_name:
                                device_name = data.get("device", {}).get("name", DEFAULT_NAME)

                            await self.async_set_unique_id(device_id)
                            self._abort_if_unique_id_configured()

                            return self.async_create_entry(
                                title=device_name,
                                data={
                                    CONF_HOST: host,
                                    CONF_PORT: port,
                                    CONF_DEVICE_ID: device_id,
                                    CONF_DEVICE_NAME: device_name,
                                },
                            )
                        else:
                            errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required(CONF_HOST, default="192.168.1.50"): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Optional(CONF_DEVICE_NAME, default=DEFAULT_NAME): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
