import enum


class Event(str, enum.Enum):
    GO = "go"
    TYPE = "type"
    CLEAR = "clear"
    PRESS = "press"
    FOCUS = "focus"
    CLICK = "click"
    HOVER = "hover"
    SELECT = "select"


class Browser(str, enum.Enum):
    CHROMIUM = "chromium"
