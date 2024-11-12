from sqlalchemy.orm import Session
from models import User  # Предполагается, что модель User уже создана и проинициализированна

def save_user_to_database(db: Session, user_info):
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        user = User(email=user_info["email"], name=user_info.get("name"))
        db.add(user)
        db.commit()
    return user.id
