from pytest import fixture
from sqlalchemy.orm import scoped_session, sessionmaker

from database import Base, engine


@fixture(autouse=True, scope="function")
def db_engine_fixture():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@fixture(scope="function")
def db_session_factory(db_engine_fixture):
    return scoped_session(sessionmaker(bind=db_engine_fixture))


@fixture(scope="function")
def db_session(db_session_factory):
    session = db_session_factory()
    yield session
    session.rollback()
    session.close()
