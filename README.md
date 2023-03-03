# Browser Automate
One DSL to rule them all.


## What is this?
Browser Automate is a DSL for automating browser tasks. 
Currently, it is a wrapper around [Playwright](https://playwright.dev/docs/intro).

The goal is to eventually create a workflow engine that can be extended to support other automation frameworks and languages.


:warning: This project is still in early development and is not ready for production use.


## Resources
* [Playwright](https://playwright.dev/docs/intro)


## Example Workflow

```yaml
name: "Google Search"
author: "Lemuel Boyce"
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


## Hooks
TBD


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
* ✅ import workflows from `automate.contrib.workflows`
  * ✅ merge workflow steps into caller

# Contributing
TBD

# Ideas
Workflows can be published by developers to a marketplace and can be used in other workflows.
To achieve this, we need to create a workflow engine that can be extended safely, with a clean public API.

Example:
* a workflow that can be used to login to a website, which can be used in other workflows


reusable workflow structure:

```directory
workflow/
  manifest.yml
  workflow.yml
  assets/
    logo.png
```

a manifest.yml file will define the schema and inputs required to fullfill the workflow.

```yaml
name: "Login"
author: "Lemuel Boyce"
description: "Login to a website"
inputs:
  - name: "username"
    type: "string"
  - name: "password"
    type: "string"
```