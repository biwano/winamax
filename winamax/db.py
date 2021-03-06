import sqlalchemy
from sqlalchemy import create_engine, Table, Index, Column, Numeric, BigInteger, Integer, String, MetaData, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import json
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('db.log')
fh.setLevel(level=logging.DEBUG)
logger.addHandler(fh)

class History(Base):
   __tablename__ = 'history'
   
   outcome_id = Column(Integer, primary_key = True)
   time = Column(BigInteger, primary_key = True)
   data = Column(String)

class Match(Base):
   __tablename__ = 'match'
   
   match_id = Column(Integer, primary_key = True)
   sport_id = Column(Integer)
   category_id = Column(Integer)
   tournament_id = Column(Integer)
   value= Column(String)

class Config(Base):
   __tablename__ = 'config'
   
   key = Column(String, primary_key = True)
   value= Column(String)

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

def get_config_be(session, key):
      try:
          config = session.query(Config).filter_by(key=key).one()
      except NoResultFound as e:
          config = Config(key=key)
          session.add(config)
      return config

def update_config(key, value):
    with Session()() as session:
        config = get_config_be(session, key)
        config.value = json.dumps(value)

def get_config(key):
    with Session()() as session:
        config = get_config_be(session, key)
        if config.value:
            return json.loads(config.value)
        return None

        

def update_match(match):
    match_id = match["matchId"]
    with Session()() as session:
        try:
            db_match = session.query(Match).filter_by(match_id=match_id).one()
            logger.debug(f"Updating match: {match_id}")
        except NoResultFound as e:
            logger.info(f"Creating match: {match_id}")
            db_match = Match(match_id=match_id,
              sport_id=match["sportId"],
              category_id=match["categoryId"],
              tournament_id=match["tournamentId"],
              )
            session.add(db_match)
        db_match.value = json.dumps(match)

def delete_match(match_id):
    with Session()() as session:
        logger.info(f"Deleting match: {match_id}")
        session.query(Match).filter_by(match_id=match_id).delete()


def delete_outcome_history(outcome_id):
    with Session()() as session:
        logger.info(f"Deleting outcome history: {outcome_id}")
        session.query(History).filter_by(outcom_id=outcome_id).delete()

def historize_outcome(outcome):
    time = datetime.now().timestamp()
    outcome_id = outcome["outcomeId"]
    with Session()() as session:
        logger.debug(f"historizing outcome: {outcome_id}")
        history = History(
            outcome_id=outcome_id,
            time=time,
            data=json.dumps(outcome))
        session.add(history)