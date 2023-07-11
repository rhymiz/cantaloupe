# Cantaloupe

An extensible framework for building browser automations.

> #### Note: This library is still very much WIP 🧪. This means that breaking changes can be introduced at any point in time.

## Getting Started

### Installation

```bash
$ pip install cantaloupe
```

### Usage

```bash
$ poetry run cantaloupe --help
```

## Development

### Requirements

* Python >= 3.10
* [Poetry](https://python-poetry.org/docs/#installation)


### Creating plugins

Plugins are created by implementing the cantaloupe hookspec. 
See [cantaloupe/hookspecs.py](src/cantaloupe/hookspecs.py) for the hookspecs.
