"""The NodeRed Conversation integration."""
from __future__ import annotations

import logging
import json
import base64
from typing import Literal, Any

import aiohttp
import voluptuous as vol

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, intent
from homeassistant.util import ulid
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_NODERED_URL,
    CONF_NODERED_USER,
    CONF_NODERED_PASS,
    DOMAIN,
    NAME,
    VERSION,
    SERVICE_PROCESS_CONVERSATION,
    ATTR_MESSAGE,
    ERROR_CANNOT_CONNECT,
    ERROR_INVALID_AUTH,
    ERROR_UNKNOWN,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NodeRed Conversation from a config entry."""
    _LOGGER.info("Setting up %s integration version %s", NAME, VERSION)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data[CONF_NODERED_URL]

    agent = NodeRedAgent(hass, entry)
    conversation.async_set_agent(hass, entry, agent)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload NodeRed Conversation."""
    _LOGGER.info("Unloading %s integration", NAME)
    hass.data[DOMAIN].pop(entry.entry_id)
    conversation.async_unset_agent(hass, entry)
    return True

class NodeRedAgent:
    """NodeRed Conversation agent."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.history: dict[str, list[dict[str, Any]]] = {}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL
    
    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        _LOGGER.debug("Processing user input: %s", user_input.text)
        
        nodered_url = self.entry.data.get(CONF_NODERED_URL)
        nodered_user = self.entry.data.get(CONF_NODERED_USER)
        nodered_pass = self.entry.data.get(CONF_NODERED_PASS)

        if not all([nodered_url, nodered_user, nodered_pass]):
            _LOGGER.error("Missing NodeRed configuration")
            raise HomeAssistantError(ERROR_INVALID_AUTH)

        if user_input.conversation_id in self.history:
            conversation_id = user_input.conversation_id
            messages = self.history[conversation_id]
        else:
            conversation_id = ulid.ulid_now()
            messages = []

        messages.append({"role": "user", "content": user_input.text})

        content = {ATTR_MESSAGE: user_input.text, 'chatid': conversation_id, "messages": json.dumps(messages)}
        _LOGGER.debug("Content sent to NodeRed: %s", content)
        nodered_auth = base64.b64encode(f"{nodered_user}:{nodered_pass}".encode()).decode()
        
        try:
            if not isinstance(nodered_url, str):
                raise ValueError("NodeRed URL is not a string")
            result = await self._call_post_request(nodered_url, nodered_auth, content)
            result = json.loads(result)
        except (HomeAssistantError, ValueError, json.JSONDecodeError) as err:
            _LOGGER.error("Error processing request: %s", err)
            result = {
                "finish_reason": "error",
                "message": { "content": f"Error: {err}" }
            }

        _LOGGER.debug("Result from NodeRed: %s", result)

        response = result["message"]
        _LOGGER.debug("Response content: %s", response)

        intent_response = intent.IntentResponse(language=user_input.language)

        if result["finish_reason"] != "error":
            messages.append(response)
            self.history[conversation_id] = messages
            intent_response.async_set_speech(response["content"])
        else:
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                response["content"],
            )

        return conversation.ConversationResult(
            response=intent_response, conversation_id=conversation_id
        )

    async def _call_post_request(self, url: str, auth: str, data: dict[str, Any]) -> str:
        """Make a POST request to the NodeRed endpoint."""
        try:
            # Warning: SSL verification is disabled. This should be enabled in production.
            _LOGGER.warning("SSL verification is disabled. This is not recommended for production use.")
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                session.headers.update({"Authorization": f"Basic {auth}"})
                async with session.post(url, data=data) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to NodeRed endpoint: %s", err)
            raise HomeAssistantError(ERROR_CANNOT_CONNECT) from err
