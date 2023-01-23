# Utilities to translate between DSL and Playwright


from collections import defaultdict

from ..enums import Action

EVENT_TO_PLAYWRIGHT: dict[str, str] = defaultdict(
    str,
    {
        Action.GO: "goto",
        Action.TYPE: "type",
        Action.CLEAR: "clear",
        Action.PRESS: "press",
        Action.FOCUS: "focus",
        Action.CLICK: "click",
        Action.HOVER: "hover",
        Action.SELECT: "selectOption",
        Action.GET_BY_TEXT: "getByText",
        Action.GET_BY_ROLE: "getByRole",
        Action.GET_BY_TITLE: "getByTitle",
        Action.GET_BY_LABEL: "getByLabel",
        Action.GET_BY_ALT_TEXT: "getByAltText",
        Action.GET_BY_PLACEHOLDER: "getByPlaceholder",
    },
)


def translate_to_playwright(event_name: str) -> str:
    """
    convert workflow event names to playwright methods.

    arg: event_name str: name passed in from workflow
    """
    return EVENT_TO_PLAYWRIGHT[event_name]


def translate_to_dsl(event_name: str) -> str:
    """
    convert playwright methods to workflow event names.

    arg: event_name str: name passed in from playwright
    """
    return {v: k for k, v in EVENT_TO_PLAYWRIGHT.items()}[event_name]