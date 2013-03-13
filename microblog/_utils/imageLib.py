# encoding: utf-8
import Image


class ImageLib(object):
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.image = Image.open(data)

    def format_image(self, quality=100):
        self.image.save(self.filename, "PNG")

    def close(self):
        self.image.close()
