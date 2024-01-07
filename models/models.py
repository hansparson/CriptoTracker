from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from sqlalchemy.orm import Session
from models.database import Base, SessionLocal
db = SessionLocal()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    user_name = Column(String)
    status_login = Column(Boolean)
    
    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self
    
    def save(self, commit: bool = True):
        """Save the record."""
        try:
            db.add(self)
            if commit:
                db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            return False
        return self
    
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        try:
            db.delete(self)
            if commit:
                return db.commit()
        except Exception:
            db.rollback()
        return
    
    def __repr__(self):
        """Represent instance as a unique string."""
        return f"{self.id}"


class CriptoTracking(Base):
    __tablename__ = 'cripto_tracking'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String)
    cripto_id = Column(String)

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self
    
    def save(self, commit: bool = True):
        """Save the record."""
        try:
            db.add(self)
            if commit:
                db.commit()
        except Exception as e:
            print(e)
            db.rollback()
        return self
    
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        try:
            db.delete(self)
            if commit:
                return db.commit()
        except Exception:
            db.rollback()
        return
    
    def __repr__(self):
        """Represent instance as a unique string."""
        return f"{self.reference_code}"

class DatabaseQueryModels:
    @staticmethod
    def get_user_by_id(user_id):
        user = db.query(Users).filter(Users.user_id == user_id).first()
        return user
    
    @staticmethod
    def get_user_by_email(email):
        user = db.query(Users).filter(Users.email == email).first()
        return user

    @staticmethod
    def set_login_status(email, status_login):
        user = db.query(Users).filter(Users.email == email).first().update(status_login=status_login)
        return user
    
    @staticmethod
    def get_user_list_crypto(user_id):
        list_crypto = db.query(CriptoTracking).filter(CriptoTracking.user_id == user_id)
        return list_crypto
    
    @staticmethod
    def delete_crypto_list(user_id, coin_names):
        deleted_count = db.query(CriptoTracking).filter(
            CriptoTracking.user_id == user_id,
            CriptoTracking.cripto_id.in_(coin_names)
        ).delete(synchronize_session=False)
        db.commit()
        return deleted_count
    
