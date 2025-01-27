from func.model import create_db
from views import MainApplication

if __name__ == "__main__":
    create_db()
    app = MainApplication()
    app.mainloop()