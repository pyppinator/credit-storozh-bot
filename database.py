import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, func, desc
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

# Если DATABASE_URL нет — используем SQLite локально
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///credit_storozh.db"

# Render даёт ссылку с postgres://, SQLAlchemy хочет postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(255))
    bank = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    last_rate = Column(Text)
    created_at = Column(String(50))

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(255))
    text = Column(Text, nullable=False)
    created_at = Column(String(50))

def init_db():
    Base.metadata.create_all(engine)

def check_subscription_exists(user_id, bank, product):
    session = SessionLocal()
    count = session.query(Subscription).filter_by(
        user_id=user_id, bank=bank, product=product
    ).count()
    session.close()
    return count > 0

def add_subscription(user_id, username, bank, product, rate):
    session = SessionLocal()
    sub = Subscription(
        user_id=user_id, username=username,
        bank=bank, product=product,
        last_rate=rate, created_at=datetime.now().isoformat()
    )
    session.add(sub)
    session.commit()
    session.close()

def get_user_subscriptions(user_id):
    session = SessionLocal()
    rows = session.query(Subscription.bank, Subscription.product, Subscription.last_rate)\
        .filter_by(user_id=user_id).all()
    session.close()
    return rows

def get_user_subscriptions_with_id(user_id):
    session = SessionLocal()
    rows = session.query(Subscription.id, Subscription.bank, Subscription.product, Subscription.last_rate)\
        .filter_by(user_id=user_id).all()
    session.close()
    return rows

def delete_subscription_by_id(sub_id, user_id):
    session = SessionLocal()
    session.query(Subscription).filter_by(id=sub_id, user_id=user_id).delete()
    session.commit()
    session.close()

def add_request(user_id, username, text):
    session = SessionLocal()
    req = Request(user_id=user_id, username=username, text=text, created_at=datetime.now().isoformat())
    session.add(req)
    session.commit()
    session.close()

def get_unique_products():
    session = SessionLocal()
    rows = session.query(Subscription.bank, Subscription.product).distinct().all()
    session.close()
    return rows

def get_subscribers(bank, product):
    session = SessionLocal()
    rows = session.query(Subscription.user_id).filter_by(bank=bank, product=product).distinct().all()
    session.close()
    return [r[0] for r in rows]

def get_current_rate(bank, product):
    session = SessionLocal()
    row = session.query(Subscription.last_rate).filter_by(bank=bank, product=product).first()
    session.close()
    return row[0] if row else None

def update_rate_for_all(bank, product, new_rate):
    session = SessionLocal()
    session.query(Subscription).filter_by(bank=bank, product=product).update({"last_rate": new_rate})
    session.commit()
    session.close()

def get_all_subscriptions():
    session = SessionLocal()
    rows = session.query(
        Subscription.user_id, Subscription.username,
        Subscription.bank, Subscription.product,
        Subscription.last_rate, Subscription.created_at
    ).order_by(Subscription.created_at.desc()).all()
    session.close()
    return rows

def get_stats():
    session = SessionLocal()
    total_users = session.query(Subscription.user_id).distinct().count()
    total_subs = session.query(Subscription).count()
    top_products = session.query(
        Subscription.bank, Subscription.product,
        func.count(Subscription.id).label('cnt')
    ).group_by(Subscription.bank, Subscription.product).order_by(desc('cnt')).limit(5).all()
    bank_stats = session.query(
        Subscription.bank, func.count(Subscription.id).label('cnt')
    ).group_by(Subscription.bank).order_by(desc('cnt')).all()
    last_sub = session.query(func.max(Subscription.created_at)).scalar()
    session.close()
    return {
        "total_users": total_users,
        "total_subs": total_subs,
        "top_products": top_products,
        "bank_stats": bank_stats,
        "last_sub": last_sub
    }