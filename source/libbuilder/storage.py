import itertools

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm, Column, String, create_engine, SmallInteger
import pipe

from .specification import DEFAULT_SPECIFICATION, PRIMARI_KEY

TYPES_MAP = {
    int: SmallInteger, str: String
}


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


def build_orm_class(table_name, base_class, specification):
    klass_fields = {
        field: Column(TYPES_MAP[field_type]) for field, field_type in
        specification.items()
    }
    klass_fields['__tablename__'] = table_name
    klass_fields[PRIMARI_KEY] = Column(String, primary_key=True)
    return type(table_name, (base_class,), klass_fields)


@pipe.Pipe
def write_to_sqlite(
        records_iterator, table_name, output, group_size, specification=None
    ):
    specification = specification or DEFAULT_SPECIFICATION

    Base = declarative_base()
    engine = create_engine('sqlite:///%s' % output)
    mapper_klass = build_orm_class(table_name, Base, specification)
    Base.metadata.create_all(engine)

    session = orm.sessionmaker(bind=engine)()
    for records in grouper(records_iterator, group_size):
        session.bulk_save_objects(
            mapper_klass(**record) for record in filter(None, records)
        )

    session.commit()
