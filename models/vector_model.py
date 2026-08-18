from sqlalchemy import Column, Integer, String, Text

from pgvector.sqlalchemy import Vector

from app.database import Base


class RepositoryChunk(Base):
    """
    Stores repository code chunks together with their vector embeddings.
    """

    __tablename__ = "repository_chunks"

    id = Column(Integer,primary_key=True,index=True,)

    file_name = Column(String,nullable=False,)

    relative_path = Column(String,nullable=False,)

    chunk_number = Column(Integer,nullable=False,)

    content = Column(Text,nullable=False,)

    embedding = Column(Vector(384),nullable=False,)