EVENT_TO_PLAYWRIGHT: dict[str, str] = {
    "go": "goto",
    "code": "",
    "type": "type",
    "clear": "clear",
    "press": "press",
    "focus": "focus",
    "click": "click",
    "hover": "hover",
    "select": "selectOption",
    "set_variable": "",
    "use_variable": ""
}


def translate_to_playwright(event_name: str) -> str:
    """
    convert workflow event names to playwright methods.

    arg: event_name str: name passed in from workflow
    """
    return EVENT_TO_PLAYWRIGHT[event_name]
