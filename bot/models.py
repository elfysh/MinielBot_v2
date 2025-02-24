from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    dialog_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_nickname = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    wake_up_time = Column(Time)
    sleep_time = Column(Time)


class Theme(Base):
    __tablename__ = 'themes'
    theme_id = Column(Integer, primary_key=True, autoincrement=True)
    theme_title = Column(String, nullable=False)

class Image(Base):
    __tablename__ = 'images'
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(Integer, ForeignKey('themes.theme_id'))
    image_url = Column(String, nullable=False)
    theme = relationship('Theme', backref='images')

class Log(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    dialog_id = Column(Integer, ForeignKey('users.dialog_id'))
    theme_id = Column(Integer, ForeignKey('themes.theme_id'))
    send_time = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', backref='logs')
    theme = relationship('Theme', backref='logs')

class TextTemplate(Base):
    __tablename__ = 'texttemplates'
    temptale_id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(Integer, ForeignKey('themes.theme_id'))
    message_text = Column(String, nullable=False)
    theme = relationship('Theme', backref='text_templates')