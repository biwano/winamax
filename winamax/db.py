import sqlalchemy
from sqlalchemy import create_engine, Table, Index, Column, Numeric, BigInteger, Integer, String, MetaData, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()

class History(Base):
   __tablename__ = 'history'
   
   outcome_id = Column(Integer, primary_key = True)
   time = Column(BigInteger, primary_key = True)
   data = Column(String)

#Index('myindex', Log.bot, Log.market, Log.time)



global SESSION
SESSION = None
def get_session():
  global SESSION
  if not SESSION:
    engine = create_engine(f"sqlite:///db.sqlite", echo = False)
    SESSION = sessionmaker(bind = engine)
    Base.metadata.create_all(engine)
  return SESSION


def Session():
  @contextmanager            
  def session():
      session = get_session()()
      try: 
          yield session
          session.commit()
      except Exception as e:
          import traceback
          traceback.print_exc()
          session.rollback()
          session.close()
          raise(e)
      finally:
          session.close()
  return session
