import enum


class Action(str, enum.Enum):
    """An enum containing all fields
    currently supported by the DSL.
    """

    GO = "go"
    CODE = "code"
    TYPE = "type"
    BACK = "back"
    CLEAR = "clear"
    PRESS = "press"
    FOCUS = "focus"
    CLICK = "click"
    HOVER = "hover"
    RELOAD = "reload"
    SELECT = "select"
    IMPORT = "import"
    FORWARD = "forward"
    SCREENSHOT = "screenshot"
    GET_BY_TEXT = "get_by_text"
    GET_BY_ROLE = "get_by_role"
    GET_BY_TITLE = "get_by_title"
    GET_BY_LABEL = "get_by_label"
    SET_VARIABLE = "set_variable"
    USE_VARIABLE = "use_variable"
    WAIT_FOR_URL = "wait_for_url"
    GET_BY_TEST_ID = "get_by_test_id"
    GET_BY_ALT_TEXT = "get_by_alt_text"
    GET_BY_PLACEHOLDER = "get_by_placeholder"


class Browser(str, enum.Enum):
    """Playwright supported browsers"""

    EDGE = "edge"
    CHROME = "chrome"
    SAFARI = "webkit"
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"


class TraceVideoOpts(str, enum.Enum):
    ON = "on"
    OFF = "off"
    FIRST_TRY = "on-first-retry"
    ON_FAILURE = "retain-on-failure"


class ScreenshotOpts(str, enum.Enum):
    ON = "on"
    OFF = "off"
    ON_FAILURE = "only-on-failure"
