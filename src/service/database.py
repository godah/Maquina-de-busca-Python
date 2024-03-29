from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite = 'sqlite:///F:\\test.db'
maquinadebuscapy = 'mysql+pymysql://root1a2b3c:root1a2b3c@85.10.205.173:3306/maquinadebuscapy'
localhostpc = 'mysql+pymysql://root:roota1b2c3@localhost:3306/maquinadebuscaPython'
localhostnote = 'mysql+pymysql://root1a2b3c:root1a2b3c@localhost:3306/maquinadebuscaPython'

engine = create_engine(localhostnote, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
db = Base.metadata

def init_db():
    Base.metadata.create_all(bind=engine)
