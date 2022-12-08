from database import sesssionLocal

def get_db():
    db = sesssionLocal()
    try:
        yield db
    finally:
        db.close()