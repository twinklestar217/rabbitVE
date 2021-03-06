from .base_detector import BaseDetector

import cv2


class CVDNN(BaseDetector):
    def __init__(self, conf_threshold):
        super(CVDNN, self).__init__()
        self.conf_threshold = conf_threshold

    def load_model(self, path):
        proto, caffemodel = path
        self.net = cv2.dnn.readNetFromCaffe(proto, caffemodel)

    def detection(self, frame):
        frameOpenCVDnn = frame.copy()
        frameHeight = frameOpenCVDnn.shape[0]
        frameWidth = frameOpenCVDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpenCVDnn, 1.0, (300, 300), [104, 117, 123], False, False)

        self.net.setInput(blob)
        detections = self.net.forward()
        bboxes = []
        h, w, c = frame.shape
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                # # 太扁了,影响检测，整合到一个合适的尺寸
                # dx = x2 - x1
                # dy = y2 - y1
                # center_x = (x1 + x2) // 2
                # center_y = (y1 + y2) // 2
                # max_size = max([dx, dy])
                # step = max_size // 2
                # x1 = max([0, center_x - step])
                # x2 = min([w, center_x + step])
                # y1 = max([0, center_y - step])
                # y2 = min([h, center_y + step])
                ###########################
                bboxes.append([y1, x2, y2, x1])
                cv2.rectangle(frameOpenCVDnn, (x1, y1), (x2, y2), (0, 255, 0), int(frameHeight / 150), 8)
                # cv2.rectangle(frameDraw, (left, top), (right, bottom), (0, 255, 0), int(frameHeight / 150), 8)
                # bboxes.append([top, right, bottom, left])
                ### 横向是x，纵向是y

        return frameOpenCVDnn, bboxes
