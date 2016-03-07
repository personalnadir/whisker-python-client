#!/usr/bin/env python
# whisker/constants.py
# Copyright (c) Rudolf Cardinal (rudolf@pobox.com).
# See LICENSE for details.

import re

# =============================================================================
# Networking
# =============================================================================

DEFAULT_PORT = 3233
BUFFERSIZE = 4096

# =============================================================================
# Other
# =============================================================================

FILENAME_SAFE_ISOFORMAT = "%Y%m%dT%H%M"  # no colons in Windows filenames

# =============================================================================
# Interface basics
# =============================================================================

EOL = '\n'
# Whisker sends (and accepts) LF between responses, and we are operating in the
# str (not bytes) domain; see below re readAll().
EOL_LEN = len(EOL)

# =============================================================================
# Server -> client
# =============================================================================

IMMPORT_REGEX = re.compile(r"^ImmPort: (\d+)")
CODE_REGEX = re.compile(r"^Code: (\w+)")
TIMESTAMP_REGEX = re.compile(r"^(.*) \[(\d+)\]$")

RESPONSE_SUCCESS = "Success"
RESPONSE_FAILURE = "Failure"
PING = "Ping"
PING_ACK = "PingAcknowledged"

EVENT_REGEX = re.compile(r"^Event: (.*)$")
KEY_EVENT_REGEX = re.compile(r"^KeyEvent: (.*)$")
CLIENT_MESSAGE_REGEX = re.compile(r"^ClientMessage: (.*)$")
INFO_REGEX = re.compile(r"^Info: (.*)$")
WARNING_REGEX = re.compile(r"Warning: (.*)$")
SYNTAX_ERROR_REGEX = re.compile(r"^SyntaxError: (.*)$")
ERROR_REGEX = re.compile(r"Error: (.*)$")

EVENT_PREFIX = "Event: "
KEY_EVENT_PREFIX = "KeyEvent: "
CLIENT_MESSAGE_PREFIX = "ClientMessage: "
INFO_PREFIX = "Info: "
WARNING_PREFIX = "Warning: "
SYNTAX_ERROR_PREFIX = "SyntaxError: "
ERROR_PREFIX = "Error: "

# =============================================================================
# Client -> server
# =============================================================================

CMD_TEST_NETWORK_LATENCY = "TestNetworkLatency"
CMD_WHISKER_STATUS = "WhiskerStatus"
CMD_REPORT_NAME = "ReportName"
CMD_TIMESTAMPS = "Timestamps"

CMD_TIMER_SET_EVENT = "TimerSetEvent"
CMD_TIMER_CLEAR_EVENT = "TimerClearEvent"
CMD_TIMER_CLEAR_ALL_EVENTS = "TimerClearAllEvents"

CMD_CLAIM_GROUP = "ClaimGroup"
CMD_LINE_CLAIM = "LineClaim"
CMD_LINE_SET_STATE = "LineSetState"
CMD_LINE_SET_EVENT = "LineSetEvent"

FLAG_INPUT = "-input"
FLAG_OUTPUT = "-output"

VAL_ON = "on"
VAL_OFF = "off"
VAL_BOTH = "both"

# *** more to do
