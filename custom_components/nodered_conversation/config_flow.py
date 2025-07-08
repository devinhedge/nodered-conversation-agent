"""Config flow for NodeRed Conversation integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

# pylint: disable=import-error
from homeassistant import config_entries  # type: ignore
from homeassistant.core import HomeAssistant  # type: ignore
from homeassistant.data_entry_flow import FlowResult  # type: ignore
from homeassistant.exceptions import HomeAssistantError  # type: ignore

from .const import (
    CONF_NODERED_URL,
    CONF_NODERED_USER,
    CONF_NODERED_PASS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NODERED_URL): str,
        vol.Optional(CONF_NODERED_USER): str,
        vol.Optional(CONF_NODERED_PASS): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect."""
    try:
        async with aiohttp.ClientSession() as session:
            auth = None
            if data.get(CONF_NODERED_USER) and data.get(CONF_NODERED_PASS):
                auth = aiohttp.BasicAuth(data[CONF_NODERED_USER], data[CONF_NODERED_PASS])
            async with session.get(data[CONF_NODERED_URL], auth=auth) as response:
                if response.status != 200:
                    raise CannotConnect
    except aiohttp.ClientError:
        raise CannotConnect
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.exception("Unexpected exception")
        raise UnknownError from err

class ConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for NodeRed Conversation."""

    VERSION = 1
    DOMAIN = DOMAIN

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except UnknownError:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="NodeRed Conversation", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

class OptionsFlow(config_entries.OptionsFlow):
    """NodeRed config flow options handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="NodeRed Conversation", data=user_input)

        schema = {
            vol.Required(
                CONF_NODERED_URL,
                default=self.config_entry.data.get(CONF_NODERED_URL, ""),
            ): str,
            vol.Optional(
                CONF_NODERED_USER,
                default=self.config_entry.data.get(CONF_NODERED_USER, ""),
            ): str,
            vol.Optional(
                CONF_NODERED_PASS,
                default=self.config_entry.data.get(CONF_NODERED_PASS, ""),
            ): str,
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

class UnknownError(HomeAssistantError):
    """Error to indicate an unknown error occurred."""
