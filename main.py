import yaml

from src.automate.main import load_workflow


def main() -> None:
    with open("automate.yml", "r") as file:
        data = yaml.safe_load(file)
        load_workflow(data)


if __name__ == "__main__":
    main()
