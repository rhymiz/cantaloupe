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
    FORWARD = "forward"
    SCREENSHOT = "screenshot"
    GET_BY_TEXT = "get_by_text"
    GET_BY_ROLE = "get_by_role"
    GET_BY_TITLE = "get_by_title"
    GET_BY_LABEL = "get_by_label"
    SET_VARIABLE = "set_variable"
    USE_VARIABLE = "use_variable"
    GET_BY_TEST_ID = "get_by_test_id"
    GET_BY_ALT_TEXT = "get_by_alt_text"
    GET_BY_PLACEHOLDER = "get_by_placeholder"

    @staticmethod
    def page_level() -> list["Action"]:
        """actions that can be used on the page object"""
        return [
            Action.GO,
            Action.BACK,
            Action.RELOAD,
            Action.FORWARD,
            Action.SCREENSHOT,
        ]

    @staticmethod
    def recommended() -> list["Action"]:
        """
        recommended playwright locators.
        https://playwright.dev/docs/locators

        example:
            * `page.getByText()`
            * `page.getByTestId()`
        """
        return [
            Action.GET_BY_TEXT,
            Action.GET_BY_ROLE,
            Action.GET_BY_LABEL,
            Action.GET_BY_TITLE,
            Action.GET_BY_TEST_ID,
            Action.GET_BY_ALT_TEXT,
            Action.GET_BY_PLACEHOLDER,
        ]


class Browser(str, enum.Enum):
    """Playwright supported browsers"""

    EDGE = "edge"
    CHROME = "chrome"
    SAFARI = "webkit"
    WEBKIT = "webkit"
    FIREFOX = "firefox"
    CHROMIUM = "chromium"
