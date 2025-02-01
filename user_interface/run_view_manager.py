from Views.MainMenuView import MainMenuView
from ViewManager import ViewManager


def main():
    start_view = MainMenuView(None)

    manager = ViewManager(initial_view=start_view, device_mode="real")

    start_view.manager = manager

    manager.start()


if __name__ == "__main__":
    main()