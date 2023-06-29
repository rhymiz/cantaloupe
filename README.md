# Cantaloupe

The browser automation framework for developers.

## Getting Started

### Requirements

* Python >= 3.10
* [Node.js](https://nodejs.org/en/) >= 14.0.0
* [Poetry](https://python-poetry.org/docs/#installation)

## What is this?

Cantaloupe is a DSL for automating browser tasks.
Currently, it is a wrapper around [Playwright](https://playwright.dev/docs/intro).

The goal is to eventually create a workflow engine that can be extended to support other automation frameworks and
languages.

:warning: This project is still in early development and is not ready for production use.

## Resources

* [Playwright](https://playwright.dev/docs/intro)

## Example Workflow

```yaml
name: "Google Search"
steps:
  - action: go
    input: "https://www.google.com"
  - action: click
    selector: "input[title=\"Search\"]"
  - action: type
    selector: "input[title=\"Search\"]"
    input: "rhymiz"
  - action: click
    selector: "input[value=\"Google Search\"] >> nth=0"
  - action: code
    input: |
      if (page.title === "Hello") {
        console.log("on hello page")
      }
```

## Actions

* go
* code (raw playwright code)
* type
* back
* clear
* press
* focus
* click
* hover
* reload
* select
* import
* forward
* screenshot
* get_by_text
* get_by_role
* get_by_title
* get_by_label
* set_variable
* use_variable
* get_by_test_id
* get_by_alt_text
* get_by_placeholder

## Adding new framework support

To add support for a new framework, you must implement the following methods:

* cantaloupe_build_spec
* cantaloupe_render_step


The following methods are optional:

* cantaloupe_setup
* cantaloupe_teardown
* cantaloupe_workflow_build_begin
* cantaloupe_workflow_build_complete
* cantaloupe_build_config_files

```python
from pathlib import Path

from slugify import slugify

from cantaloupe.plugins.hookspec import hookimpl
from cantaloupe.models import Step
from cantaloupe.types import Spec


@hookimpl
def cantaloupe_build_spec(context: "Context", workflow: "Workflow", steps: list[Step]) -> Spec:
  filename = f"{slugify(workflow.name, separator='_')}.js"
  # do something with the steps and assign the result to content
  return Spec(
          name=filename,
          content="...",
          path=Path(context.output_dir, filename),
  )


@hookimpl
def cantaloupe_render_step(step: Step) -> str:
  # do something with the step and return the result
  return "..."
```

## TODO:

* 📝 persist generated files to a given directory
* 📝 inspect selectors used in steps a suggest more stable/unique alternatives
* 📝 add native assertion support
* 📝 add http proxy configuration support
* ✅ add support for custom templates
* ✅ improve template selection logic
* 📝 add test/testsuite status reporter
    * 📝 post testsuite start
    * 📝 post test start
    * 📝 post step start
    * 📝 post step end
    * 📝 post test end
    * 📝 post testsuite end

# Contributing

TBD
