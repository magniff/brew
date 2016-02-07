from .reader import generate_records_from_fastq
from .parser import parse_records
from .storage import write_to_sqlite
from .specification import DEFAULT_SPECIFICATION


def main_routine(fastq_files, output, dryrun, fields, group_size):
    user_spec = DEFAULT_SPECIFICATION
    if fields is not None:
        user_spec = {field: DEFAULT_SPECIFICATION[field] for field in fields}

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
                specification=user_spec, group_size=group_size
            )
        )
