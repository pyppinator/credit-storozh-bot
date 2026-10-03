import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, func, desc
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///credit_storozh.db"

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

class Rate(Base):
    __tablename__ = "rates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    rate = Column(Text)
    updated_at = Column(String(50))

class PendingChange(Base):
    """Отложенные уведомления (накапливаются ночью, рассылаются утром)"""
    __tablename__ = "pending_changes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    bank = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    old_rate = Column(Text)
    new_rate = Column(Text)
    created_at = Column(String(50))

def init_db():
    Base.metadata.create_all(engine)

# === ПОДПИСКИ ===

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

def delete_all_user_subscriptions(user_id):
    session = SessionLocal()
    count = session.query(Subscription).filter_by(user_id=user_id).delete()
    session.commit()
    session.close()
    return count

def get_subscribers(bank, product):
    session = SessionLocal()
    rows = session.query(Subscription.user_id).filter_by(bank=bank, product=product).distinct().all()
    session.close()
    return [r[0] for r in rows]

def update_rate_for_all(bank, product, new_rate):
    session = SessionLocal()
    session.query(Subscription).filter_by(bank=bank, product=product).update({"last_rate": new_rate})
    session.commit()
    session.close()

# === СТАВКИ ===

def get_rate_from_db(bank, product):
    session = SessionLocal()
    row = session.query(Rate.rate).filter_by(bank=bank, product=product).first()
    session.close()
    return row[0] if row else None

def update_rate_in_db(bank, product, rate):
    session = SessionLocal()
    existing = session.query(Rate).filter_by(bank=bank, product=product).first()
    if existing:
        existing.rate = rate
        existing.updated_at = datetime.now().isoformat()
    else:
        new_rate = Rate(
            bank=bank, product=product,
            rate=rate, updated_at=datetime.now().isoformat()
        )
        session.add(new_rate)
    session.commit()
    session.close()

def get_all_rates():
    session = SessionLocal()
    rows = session.query(Rate.bank, Rate.product, Rate.rate, Rate.updated_at).all()
    session.close()
    return rows

def get_last_update_time():
    session = SessionLocal()
    row = session.query(func.max(Rate.updated_at)).scalar()
    session.close()
    return row

# === ОТЛОЖЕННЫЕ УВЕДОМЛЕНИЯ ===

def add_pending_change(user_id, bank, product, old_rate, new_rate):
    session = SessionLocal()
    change = PendingChange(
        user_id=user_id, bank=bank, product=product,
        old_rate=old_rate, new_rate=new_rate,
        created_at=datetime.now().isoformat()
    )
    session.add(change)
    session.commit()
    session.close()

def get_pending_changes():
    session = SessionLocal()
    rows = session.query(
        PendingChange.id, PendingChange.user_id,
        PendingChange.bank, PendingChange.product,
        PendingChange.old_rate, PendingChange.new_rate
    ).all()
    session.close()
    return rows

def clear_pending_changes():
    session = SessionLocal()
    session.query(PendingChange).delete()
    session.commit()
    session.close()

# === ЗАЯВКИ ===

def add_request(user_id, username, text):
    session = SessionLocal()
    req = Request(user_id=user_id, username=username, text=text, created_at=datetime.now().isoformat())
    session.add(req)
    session.commit()
    session.close()

# === СТАТИСТИКА ===

def get_unique_products():
    session = SessionLocal()
    rows = session.query(Subscription.bank, Subscription.product).distinct().all()
    session.close()
    return rows

def get_all_subscriptions():
    session = SessionLocal()
    rows = session.query(
        Subscription.user_id, Subscription.username,
        Subscription.bank, Subscription.product,
        Subscription.last_rate, Subscription.created_at
    ).order_by(Subscription.created_at.desc()).all()
    session.close()
    return rows

def get_grouped_subscriptions():
    session = SessionLocal()
    rows = session.query(Subscription).order_by(Subscription.user_id, Subscription.created_at).all()
    session.close()

    grouped = {}
    for sub in rows:
        key = sub.user_id
        if key not in grouped:
            grouped[key] = {
                "user_id": sub.user_id,
                "username": sub.username,
                "subscriptions": []
            }
        grouped[key]["subscriptions"].append({
            "bank": sub.bank,
            "product": sub.product,
            "rate": sub.last_rate,
            "created_at": sub.created_at
        })
    return list(grouped.values())

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