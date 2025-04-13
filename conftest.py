import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(
        "postgresql://lotfi:lotfi@localhost:5432/library_db", echo=True
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    return TestClient(app)
