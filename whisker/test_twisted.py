#!/usr/bin/env python
# whisker/test_twisted.py
# Copyright (c) Rudolf Cardinal (rudolf@pobox.com).
# See LICENSE for details.

import argparse
import logging

from twisted.internet import reactor

from whisker.api import (
    Pen,
    PenStyle,
    BrushStyle,
    BrushHatchStyle,
    Brush,
    Rectangle,
)
from whisker.constants import DEFAULT_PORT
from whisker.logging import (
    configure_logger_for_colour,
    # print_report_on_all_logs,
)
from whisker.twistedclient import WhiskerTask

log = logging.getLogger(__name__)

DEFAULT_DISPLAY_NUM = 0
DEFAULT_AUDIO_NUM = 0
DEFAULT_INPUT_LINE = 0
DEFAULT_OUTPUT_LINE = 64
DEFAULT_MEDIA_DIR = r"C:\Program Files\WhiskerControl\Server Test Media"
DEFAULT_BITMAP = "santa_fe.bmp"
DEFAULT_VIDEO = "mediaexample.wmv"
DEFAULT_WAV = "telephone.wav"

AUDIO = "audio"
DISPLAY = "display"
DOC = "doc"
VIDEO = "_video"


class MyWhiskerTask(WhiskerTask):
    def __init__(self,
                 display_num: int,
                 audio_num: int,
                 input_line: str,
                 output_line: str,
                 media_dir: str,
                 bitmap: str,
                 video: str,
                 wav: str) -> None:
        super().__init__()  # call base class init
        self.display_num = display_num
        self.audio_num = audio_num
        self.input = input_line
        self.output = output_line
        self.media_dir = media_dir
        self.bitmap = bitmap
        self.video = video
        self.wav = wav
        # ... anything extra here

    def fully_connected(self) -> None:
        print("SENDING SOME TEST/DEMONSTRATION COMMANDS")
        self.whisker.get_network_latency_ms()
        self.whisker.report_name("Whisker Twisted client prototype")
        self.whisker.timestamps(True)
        self.whisker.timer_set_event("TimerFired", 1000, 9)
        self.whisker.timer_set_event("EndOfTask", 12000)

        # ---------------------------------------------------------------------
        # Audio
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # Display
        # ---------------------------------------------------------------------
        bg_col = (0, 0, 100)
        pen = Pen(width=3, colour=(255, 255, 150), style=PenStyle.solid)
        brush = Brush(
            colour=(255, 0, 0), bg_colour=(0, 255, 0),
            opaque=True, style=BrushStyle.hatched,
            hatch_style=BrushHatchStyle.bdiagonal)
        self.whisker.claim_display(number=self.display_num, alias=DISPLAY)
        display_size = self.whisker.display_get_size(DISPLAY)
        log.info("display_size: {}".format(display_size))
        self.whisker.display_scale_documents(DISPLAY, True)
        self.whisker.display_create_document(DOC)
        self.whisker.display_set_background_colour(DOC, bg_col)
        self.whisker.display_blank(DISPLAY)
        self.whisker.display_create_document("junk")
        self.whisker.display_delete_document("junk")
        self.whisker.display_show_document(DISPLAY, DOC)
        with self.whisker.display_cache_wrapper(DOC):
            self.whisker.display_add_obj_text(
                DOC, "_text", (50, 50), "hello there!",
                italic=True)
            self.whisker.display_add_obj_line(
                DOC, "_line", (25, 25), (200, 200), pen)
            self.whisker.display_add_obj_arc(
                DOC, "_arc",
                Rectangle(left=100, top=100, width=200, height=200),
                (25, 25), (200, 200), pen)
            self.whisker.display_add_obj_bezier(
                DOC, "_bezier",
                (100, 100), (150, 100),
                (150, 200), (100, 200),
                pen)
            self.whisker.display_add_obj_chord(
                DOC, "_chord",
                Rectangle(left=300, top=0, width=100, height=100),
                (100, 150), (400, 175),
                pen, brush)
            self.whisker.display_add_obj_ellipse(
                DOC, "_ellipse",
                Rectangle(left=0, top=200, width=200, height=100),
                pen, brush)
            self.whisker.display_add_obj_pie(
                DOC, "_pie",
                Rectangle(left=0, top=300, width=200, height=100),
                (10, 320), (180, 380),
                pen, brush)
            self.whisker.display_add_obj_polygon(
                DOC, "_polygon",
                [(400, 200), (450, 300), (400, 400), (300, 300)],
                pen, brush, alternate=True)
            self.whisker.display_add_obj_rectangle(
                DOC, "_rectangle",
                Rectangle(left=500, top=0, width=200, height=100),
                pen, brush)
            self.whisker.display_add_obj_roundrect(
                DOC, "_roundrect",
                Rectangle(left=500, top=200, width=100, height=200),
                150, 250,
                pen, brush)
            self.whisker.display_add_obj_camcogquadpattern(
                DOC, "_camcogquad",
                (500, 400),
                10, 10,
                [1, 2, 4, 8, 16, 32, 64, 128],
                [255, 254, 253, 252, 251, 250, 249, 248],
                [1, 2, 3, 4, 5, 6, 7, 8],
                [128, 64, 32, 16, 8, 4, 2, 1],
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 0, 255),
                (100, 100, 100))
        self.whisker.display_set_event(DOC, "_polygon", "poly_touched")
        self.whisker.display_clear_event(DOC, "_polygon")
        self.whisker.display_set_event(DOC, "_camcogquad", "play")
        self.whisker.display_set_event(DOC, "_roundrect", "pause")
        self.whisker.display_set_event(DOC, "_rectangle", "stop")
        self.whisker.display_set_obj_event_transparency(DOC, "_rectangle",
                                                        False)
        self.whisker.display_bring_to_front(DOC, "_chord")
        self.whisker.display_send_to_back(DOC, "_chord")
        self.whisker.display_keyboard_events(DOC)
        self.whisker.display_event_coords(False)
        self.whisker.display_set_audio_device(DISPLAY, AUDIO)
        self.whisker.display_add_obj_video(DOC, VIDEO, (600, 0), self.video)
        self.whisker.video_set_volume(DOC, VIDEO, 90)
        self.whisker.video_timestamps(True)
        video_dur_ms = self.whisker.video_get_duration_ms(DOC, VIDEO)
        log.info("video_dur_ms: {}".format(video_dur_ms))
        video_pos_ms = self.whisker.video_get_time_ms(DOC, VIDEO)
        log.info("video_pos_ms: {}".format(video_pos_ms))

    def incoming_event(self, event: str, timestamp: int = None) -> None:
        print("Event: {e} (timestamp {t})".format(e=event, t=timestamp))
        if event == "EndOfTask":
            # noinspection PyUnresolvedReferences
            reactor.stop()
        elif event == "play":
            self.whisker.video_play(DOC, VIDEO)
        elif event == "pause":
            self.whisker.video_pause(DOC, VIDEO)
        elif event == "stop":
            self.whisker.video_stop(DOC, VIDEO)
        elif event == "back":
            self.whisker.video_seek_relative(DOC, VIDEO, -1000)
        elif event == "forward":
            self.whisker.video_seek_relative(DOC, VIDEO, 1000)
        elif event == "start":
            self.whisker.video_seek_absolute(DOC, VIDEO, 0)


def main() -> None:
    logging.basicConfig()
    logging.getLogger("whisker").setLevel(logging.DEBUG)
    configure_logger_for_colour(logging.getLogger())  # configure root logger
    # print_report_on_all_logs()

    parser = argparse.ArgumentParser("Test Whisker raw socket client")
    parser.add_argument('--server', default='localhost',
                        help="Server (default: localhost)")
    parser.add_argument('--port', default=DEFAULT_PORT, type=int,
                        help="Port (default: {})".format(DEFAULT_PORT))
    parser.add_argument(
        '--display_num', default=DEFAULT_DISPLAY_NUM, type=int,
        help="Display number to use (default: {})".format(DEFAULT_DISPLAY_NUM))
    parser.add_argument(
        '--audio_num', default=DEFAULT_AUDIO_NUM, type=int,
        help="Audio device number to use (default: {})".format(
            DEFAULT_AUDIO_NUM))
    parser.add_argument(
        '--input', default=DEFAULT_INPUT_LINE, type=int,
        help="Input line number to use (default: {})".format(
            DEFAULT_INPUT_LINE))
    parser.add_argument(
        '--output', default=DEFAULT_OUTPUT_LINE, type=int,
        help="Output line number to use (default: {})".format(
            DEFAULT_OUTPUT_LINE))
    parser.add_argument(
        '--media_dir', default=DEFAULT_MEDIA_DIR, type=str,
        help="Media directory to use (default: {})".format(
            DEFAULT_MEDIA_DIR))
    parser.add_argument(
        '--bitmap', default=DEFAULT_BITMAP, type=str,
        help="Bitmap to use (default: {})".format(DEFAULT_BITMAP))
    parser.add_argument(
        '--video', default=DEFAULT_VIDEO, type=str,
        help="Video to use (default: {})".format(DEFAULT_VIDEO))
    parser.add_argument(
        '--wav', default=DEFAULT_WAV, type=str,
        help="WAV file to use (default: {})".format(DEFAULT_WAV))
    args = parser.parse_args()

    print("Module run explicitly. Running a Whisker test.")
    w = MyWhiskerTask(
        display_num=args.display_num,
        audio_num=args.audio_num,
        input_line=args.input,
        output_line=args.output,
        media_dir=args.media_dir,
        bitmap=args.bitmap,
        video=args.video,
        wav=args.wav,
    )
    w.connect(args.server, args.port)
    reactor.run()


if __name__ == '__main__':
    main()
