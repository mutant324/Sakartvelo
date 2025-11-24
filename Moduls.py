from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# db будет импортировано из app.py! db = SQLAlchemy()
# Здесь db не привязан к app — привяжем позже

db = SQLAlchemy()

# Общая модель (без изменений)
class IncomingData(db.Model):
    __tablename__ = 'incoming_data'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)
    key = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(500))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)  # Без () для динамики
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 =  db.Column(db.String(500),nullable=True)
    image_path2 =  db.Column(db.String(500),nullable=True)

# Специализированные модели (без изменений, кроме Photo)
class News(db.Model):
    __bind_key__ = 'news'
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)
    image_path = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)


class Info(db.Model):
    __bind_key__ = 'info'
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)
    image_path = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)


class History(db.Model):
    __bind_key__ = 'history'
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)
    image_path = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)


class Photo(db.Model):
    __bind_key__ = 'photo'  # Исправлено: lowercase, соответствует config
    __tablename__ = 'photos'  # Plural для consistency
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)  # НОВОЕ: добавлено для шаблона и adm()
    image_path = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)


    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)

    # Если нужно: text/key — добавь аналогично другим

# НОВОЕ: Модели для переводов (зеркало оригиналов, bind_key='translated')
class TranslatedNews(db.Model):
    __bind_key__ = 'translated'
    __tablename__ = 'translated_news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Переведённый
    intro = db.Column(db.String(500), nullable=False)  # Переведённый
    text = db.Column(db.Text(10000), nullable=False)          # Переведённый (или None для photo-подобных)
    image_path = db.Column(db.String(200))             # Оригинал (не переводим)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    original_id = db.Column(db.Integer, nullable=True) # Ссылка на оригинал (опционально)
    lang = db.Column(db.String(10), default='en')      # Язык перевода
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)


class TranslatedInfo(db.Model):
    __bind_key__ = 'translated'
    __tablename__ = 'translated_info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)
    image_path = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    original_id = db.Column(db.Integer, nullable=True)
    lang = db.Column(db.String(10), default='en')
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)


class TranslatedHistory(db.Model):
    __bind_key__ = 'translated'
    __tablename__ = 'translated_history'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text(10000), nullable=False)
    image_path = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    original_id = db.Column(db.Integer, nullable=True)
    lang = db.Column(db.String(10), default='en')
    text2 = db.Column(db.Text(10000), nullable=True)
    text3 = db.Column(db.Text(10000), nullable=True)

    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)


class TranslatedPhoto(db.Model):
    __bind_key__ = 'translated'
    __tablename__ = 'translated_photos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # Переведённый
    intro = db.Column(db.String(500), nullable=False)  # Переведённый
    image_path = db.Column(db.String(200))             # Оригинал
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    original_id = db.Column(db.Integer, nullable=True)
    lang = db.Column(db.String(10), default='en')
    image_path1 = db.Column(db.String(500), nullable=True)
    image_path2 = db.Column(db.String(500), nullable=True)

    # Без text и key, как в оригинальной Photo