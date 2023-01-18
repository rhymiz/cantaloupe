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


## Plugins


# Contributing