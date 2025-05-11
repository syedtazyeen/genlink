from app.core.db import db
from app.core.config import get_config
from pymongo.database import Database

class BaseService:
    def __init__(self):
        self.db: Database = db
        self.config = get_config()
