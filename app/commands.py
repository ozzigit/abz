from app import app


@app.cli.command("init_db")
def init_db():
    """set values in db"""
    print('fdfsdfsd')


@app.cli.command("clear_db")
def del_tables():
    """del all tables in db"""
    print("all tables is deleted")
