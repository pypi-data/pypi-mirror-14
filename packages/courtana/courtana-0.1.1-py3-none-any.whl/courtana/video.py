# -*- coding: utf-8 -*-

"""
Video object
"""

import os
import cv2


class Video(object):

    """
    Video
    """

    def __init__(self, filepath):
        # Full video path and containing folder
        self.file = filepath
        self.dir = os.path.dirname(filepath)

        # OpenCV VideoCapture object
        self.cap = cv2.VideoCapture(filepath)

        # Video properties
        self.nframes = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # Current frame
        self.frame_idx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.frame = self.read_frame()

        # All frames
        self.frames = range(self.nframes)

    def __str__(self):
        return "Video ({}x{}) with {} frames @ {} FPS.".format(
            self.width,
            self.height,
            self.nframes,
            self.fps
            )

    def __del__(self):
        self.cap.release()
        # cv2.destroyAllWindows()

    # *******
    # Methods
    # =======

    def read_frame(self, i=None):
        """Returns a video frame.

        If a specific frame `i` is asked for, returns that frame and
        then resumes to its previous reading position.

        Parameters:
        ===========
        :i: Number of the frame desired. If None, reads the current one.
            Default is None.
        """
        assert(self.cap.isOpened())

        current_frame = self.frame_idx
        if i is not None:
            self.frame_idx = i

        ret, self.frame = self.cap.read()

        if i is not None:
            self.frame_idx = current_frame

        if ret:
            return self.frame
        else:
            raise Exception("Failed to read frame.")

    def show_frame(self, i=None, window='window', resize=False):
        frame = self.read_frame(i)
        if resize:
            frame = cv2.resize(frame,
                               dsize=(0, 0),
                               fx=0.5,
                               fy=0.5,
                               interpolation=cv2.INTER_AREA)
        cv2.imshow(window, frame)
        cv2.waitKey(0)

    def play(self, begin=None, end=None, step=1, window='window', wait_time=1,
             show_trackdata=False):
        if begin is None:
            begin = 0

        if end is None:
            end = self.nframes

        if show_trackdata is True and self.trackdata is None:
            raise AttributeError("Need a `trackdata` attribute")

        for i in self.frames[begin:end:step]:
            frame = self.read_frame(i)
            cv2.putText(frame,
                        "Frame " + str(i),
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        1,
                        cv2.LINE_AA)
            if show_trackdata:
                try:
                    draw_fly(frame,
                             self.trackdata.f.loc[i],
                             color=(150, 25, 198))
                    draw_fly(frame,
                             self.trackdata.m.loc[i],
                             color=(198, 150, 25))
                except KeyError:
                    if i > self.trackdata.ok_frames[-1]:
                        print("Frame", i, "went over tracked limits")
                        break
                    else:
                        print("Problem with frame", i)
            cv2.imshow(window, frame)
            cv2.waitKey(wait_time)
        cv2.destroyAllWindows()

    # **********
    # Properties
    # ==========

    @property
    def frame_idx(self):
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    @frame_idx.setter
    def frame_idx(self, value):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, value)


# 0 - CV_CAP_PROP_POS_MSEC
#   Current position of the video file in milliseconds or video capture
#   timestamp.

# 1 - CV_CAP_PROP_POS_FRAMES
#   0-based index of the frame to be decoded/captured next.

# 2 - CV_CAP_PROP_POS_AVI_RATIO
#   Relative position of the video file: 0 - start of the film, 1 - end
#   of the film.

# 3 - CV_CAP_PROP_FRAME_WIDTH
#   Width of the frames in the video stream.

# 4 - CV_CAP_PROP_FRAME_HEIGHT
#   Height of the frames in the video stream.

# 5 - CV_CAP_PROP_FPS
#   Frame rate.

# 6 - CV_CAP_PROP_FOURCC
#   4-character code of codec.

# 7 - CV_CAP_PROP_FRAME_COUNT
#   Number of frames in the video file.

# 8 - CV_CAP_PROP_FORMAT
#   Format of the Mat objects returned by retrieve() .

# 9 - CV_CAP_PROP_MODE
#   Backend-specific value indicating the current capture mode.

# 10 - CV_CAP_PROP_BRIGHTNESS
#   Brightness of the image (only for cameras).

# 11 - CV_CAP_PROP_CONTRAST
#   Contrast of the image (only for cameras).

# 12 - CV_CAP_PROP_SATURATION
#   Saturation of the image (only for cameras).

# 13 - CV_CAP_PROP_HUE
#   Hue of the image (only for cameras).

# 14 - CV_CAP_PROP_GAIN
#   Gain of the image (only for cameras).

# 15 - CV_CAP_PROP_EXPOSURE
#   Exposure (only for cameras).

# 16 - CV_CAP_PROP_CONVERT_RGB
#   Boolean flags indicating whether images should be converted to RGB.

# 17 - CV_CAP_PROP_WHITE_BALANCE
#   Currently not supported

# 18 - CV_CAP_PROP_RECTIFICATION
#   Rectification flag for stereo cameras (note: only supported by
#   DC1394 v 2.x backend currently)


def draw_fly(frame, data, **kwargs):
    """Draw fly.
    Represents a fly's position and orientation in an OpenCV image with
    an arrow.
    :frame: an OpenCV image
    :data: a line of the DataFrame corresponding to the frame to visualize
    `kwargs` are passed to the arrowedLine method.
    """
    if data.isnull().all():
        return

    head_x = int(data["head_x"])
    head_y = int(data["head_y"])
    tail_x = int(data["tail_x"])
    tail_y = int(data["tail_y"])

    kwargs['thickness'] = kwargs.get('thickness', 2)
    kwargs['tipLength'] = kwargs.get('tipLength', 0.4)
    cv2.arrowedLine(frame, (tail_x, tail_y), (head_x, head_y), **kwargs)
