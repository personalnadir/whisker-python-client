#!/usr/bin/env python
# whisker/test_rawsockets.py
# Copyright (c) Rudolf Cardinal (rudolf@pobox.com).
# See LICENSE for details.

import argparse
import logging

from whisker.constants import (
    DEFAULT_PORT,
    EVENT_PREFIX,
    PING_ACK,
    REPORT_NAME,
    TEST_NETWORK_LATENCY,
    TIMER_SET_EVENT,
    WHISKER_STATUS,
)
from whisker.rawsocketclient import Whisker


def test_whisker(server, port, verbose_network=True):
    w = Whisker()
    print("Connecting to {}:{}".format(server, port))
    if not w.connect_both_ports(server, port):
        raise RuntimeError("Failed to connect")

    w.send(REPORT_NAME + " Whisker python demo program")
    w.send(WHISKER_STATUS)
    reply = w.send_immediate(TIMER_SET_EVENT + " 1000 9 TimerFired")
    print("... reply to TimerSetEvent was: {}".format(reply))
    reply = w.send_immediate(TIMER_SET_EVENT + " 12000 0 EndOfTask")
    print("... reply to TimerSetEvent was: {}".format(reply))
    w.send(TEST_NETWORK_LATENCY)

    for line in w.getlines_mainsock():
        if verbose_network:
            print("SERVER: " + line)  # For info only.
        if line == "Ping":
            # If the server has sent us a Ping, acknowledge it.
            w.send(PING_ACK)
        if line[:7] == EVENT_PREFIX:
            # The server has sent us an event.
            event = line[7:]
            if verbose_network:
                print("EVENT RECEIVED: " + event)  # For info only.
            # Event handling for the behavioural task is dealt with here.
            if event == "EndOfTask":
                break  # Exit the for loop.


if __name__ == '__main__':
    logging.getLogger("whisker").setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser("Test Whisker raw socket client")
    parser.add_argument('--server', default='localhost',
                        help="Server (default: localhost)")
    parser.add_argument('--port', default=DEFAULT_PORT, type=int,
                        help="Port (default: {})".format(DEFAULT_PORT))
    args = parser.parse_args()

    test_whisker(server=args.server, port=args.port)