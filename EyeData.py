import json


class EyeData:
    eyeX: float = 0
    eyeY: float = 0
    eyeLBlink: float = 0
    eyeRBlink: float = 0

    def __int__(self, eyeX: float = 0, eyeY: float = 0, eyeLBlink: float = 0, eyeRBlink: float = 0):
        self.eyeX = eyeX
        self.eyeY = eyeY
        self.eyeLBlink = eyeLBlink
        self.eyeRBlink = eyeRBlink

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)