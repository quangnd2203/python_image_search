from enum import Enum


class BodyPrompt(str, Enum):
    FACE = "A photo of only the face of a person"
    UPPER_BODY = "A photo of the upper body of a person"
    FULL_BODY = "A photo of the full body of a person"
    LEFT_ARM = "A photo of the left arm of a person"
    RIGHT_ARM = "A photo of the right arm of a person"
