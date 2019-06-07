from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:roota1b2c3@localhost:3306/maquinadebuscaPython', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# 'mysql+pymysql://root1a2b3c:root1a2b3c@85.10.205.173:3306/maquinadebuscapy'
# 'mysql+pymysql://root:roota1b2c3@localhost:3306/maquinadebuscaPython'

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    #import yourapplication.models
    Base.metadata.create_all(bind=engine)
