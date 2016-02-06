from .reader import generate_records_from_fastq
from .parser import parse_records
from .storage import write_to_sqlite


def main_routine(fastq_files, output, dryrun):
    for fastq in fastq_files:
        print(
            "Processing file '%s' into table '%s'" %
            (fastq.name, fastq.table_name)
        )

        if dryrun:
            continue

        (
            generate_records_from_fastq(fastq) |
            parse_records |
            write_to_sqlite(output=output, table_name=fastq.table_name)
        )
