from .reader import generate_records_from_fastq
from .parser import parse_records
from .storage import write_to_sqlite
from .specification import default_specification


def main_routine(fastq_files, output, dryrun, fields):
    user_spec = default_specification
    if fields is not None:
        user_spec = {
            field: default_specification[field] for field in fields.split(',')
        }

    print('Using fields: %s.' % ', '.join(user_spec))
    for fastq in fastq_files:
        print(
            'Processing file "%s" into table "%s"' %
            (fastq.name, fastq.table_name)
        )

        if dryrun:
            continue

        (
            generate_records_from_fastq(fastq) |
            parse_records(specification=user_spec) |
            write_to_sqlite(
                output=output, table_name=fastq.table_name,
                specification=user_spec
            )
        )
