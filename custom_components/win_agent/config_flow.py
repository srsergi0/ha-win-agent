"""Config flow for Windows Direct Agent integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_DEVICE_ID,
    CONF_DEVICE_NAME,
    DEFAULT_NAME,
    DEFAULT_DEVICE_ID,
)

_LOGGER = logging.getLogger(__name__)

class WinAgentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Windows Direct Agent."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step (zero IP required)."""
        if user_input is not None:
            device_name = user_input.get(CONF_DEVICE_NAME, DEFAULT_NAME).strip()
            device_id = user_input.get(CONF_DEVICE_ID, DEFAULT_DEVICE_ID).strip()

            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=device_name,
                data={
                    CONF_DEVICE_ID: device_id,
                    CONF_DEVICE_NAME: device_name,
                },
            )

        schema = vol.Schema({
            vol.Optional(CONF_DEVICE_NAME, default=DEFAULT_NAME): str,
            vol.Optional(CONF_DEVICE_ID, default=DEFAULT_DEVICE_ID): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={
                "instructions": "No necesitas configurar la IP aquí. Toda la conexión se configura directamente desde la app de escritorio ElectroBun en tu PC."
            },
        )
