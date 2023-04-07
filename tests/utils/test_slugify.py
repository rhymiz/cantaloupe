from cantaloupe.utils.string_utils import slugify


def test_slugify() -> None:
    assert slugify("Hello World") == "hello-world"


def test_slugify_with_sub() -> None:
    assert slugify("Hello World", "_") == "hello_world"


def test_slugify_with_non_word_characters() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_with_leading_and_trailing_whitespace() -> None:
    assert slugify(" Hello, World! ") == "hello-world"
