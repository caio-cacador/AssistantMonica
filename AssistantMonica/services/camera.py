from threading import Thread
from cv2 import imencode, VideoCapture, imshow, waitKey


class Buffer:

    def __init__(self, _type, image):
        self._type = _type
        self._image = image

    def read(self):
        s, img = imencode(self._type, self._image)
        return img.tobytes()


class Camera:

    def __init__(self, cam_configs: dict):
        self.cam = VideoCapture(cam_configs['address'])
        self.frame = None
        self.be_alive = True

    def close_connection(self):
        self.be_alive = False

    def _update_cam_attr(self):
        while self.be_alive:
            if self.cam.isOpened():
                self.cam.grab()
                (success, self.frame) = self.cam.retrieve()
        self.cam.release()

    def get_current_frame(self):
        return self.frame

    def start_update(self, stream_video: bool = False):
        thread_update_cam = Thread(target=self._update_cam_attr, args=())
        thread_update_cam.start()

        if stream_video:
            thread3 = Thread(target=self.stream_video, args=())
            thread3.start()

    def stream_video(self):
        while True:
            if self.frame is not None:
                imshow('frame', self.frame)
                if waitKey(1) & 0xFF == ord('q'):
                    self.cam.release()
                    break
