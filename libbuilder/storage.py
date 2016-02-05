import pipe
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm, Column, String, create_engine, SmallInteger

from .specification import default_specification

TYPES_MAP = {
    int: SmallInteger, str: String
}


def build_orm_class(table_name, base_class, specification):
    klass_fields = {
        field: Column(TYPES_MAP[field_type]) for field, field_type in
        specification.items()
    }
    klass_fields['__tablename__'] = table_name
    klass_fields['read_identifier'] = Column(String, primary_key=True)
    return type(table_name, (base_class,), klass_fields)


@pipe.Pipe
def write_to_sqlite(records_iterator, table_name, output, specification=None):
    specification = specification or default_specification

    engine = create_engine('sqlite:///%s' % output)
    session = orm.sessionmaker(bind=engine)()
    Base = declarative_base()
    mapper_klass = build_orm_class(table_name, Base, specification)
    Base.metadata.create_all(engine)

    batch_counter = 0
    for record in records_iterator:
        session.add(mapper_klass(**record))
        batch_counter += 1
        if batch_counter > 40000:
            session.commit()
            batch_counter = 0

    session.commit()
