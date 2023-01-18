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
    SET_VARIABLE = "set_variable"
    USE_VARIABLE = "use_variable"


class Browser(str, enum.Enum):
    CHROMIUM = "chromium"
