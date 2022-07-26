from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

Base = declarative_base(metadata=SQLModel.metadata)

