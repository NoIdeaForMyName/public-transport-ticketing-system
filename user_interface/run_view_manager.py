from Views.MainMenuView import MainMenuView
from ViewManager import ViewManager


def main():
    main_view = MainMenuView()
    manager = ViewManager(initial_view=main_view)
    manager.start()


if __name__ == "__main__":
    main()
