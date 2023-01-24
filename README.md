# Browser Automate
Playwright code generation framework


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
* code (raw code block)
* type
* press
* focus
* clear
* click
* hover
* select
* set_variable
* use_variable


## Hooks
TBD


## TODO:
* persist generated files to a given directory
* inspect selectors used in steps a suggest more stable/unique alternatives
* add native assertion support
* add http proxy configuration support
* add test/testsuite status reporter
  * post testsuite start
  * post test start
  * post step start
  * post step end
  * post test end
  * post testsuite end


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