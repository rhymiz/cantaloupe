# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from yaml import Loader, load
from src.automate.main import load_workflow


def main() -> None:
    with open("automate.yml", "r") as f:
        data = load(f, Loader)
        workflow = load_workflow(data)


if __name__ == "__main__":
    main()
