import click

from .libbuilder import main_routine
from .libbuilder.specification import DEFAULT_SPECIFICATION, PRIMARI_KEY


class FileTableParam(click.File):
    FNAME_TABLE_SEPARATOR = "@"

    def convert(self, value, param, ctx):
        if self.FNAME_TABLE_SEPARATOR not in value:
            self.fail(
                "fastq params should have structure like "
                "filename%stablename" % self.FNAME_TABLE_SEPARATOR,
                param, ctx
            )

        file_name, table_name = value.split(self.FNAME_TABLE_SEPARATOR)
        convertion_result = super().convert(file_name, param, ctx)
        convertion_result.table_name = table_name
        return convertion_result


class FieldsToUse(click.ParamType):
    name = 'filed-list'

    def convert(self, value, param, ctx):
        fields = value.split(",")

        for field in fields:
            if field not in DEFAULT_SPECIFICATION:
                self.fail("unknown field %s." % field, param, ctx)

        if PRIMARI_KEY not in fields:
            self.fail(
                "field list should contain field %s." % PRIMARI_KEY,
                param, ctx
            )
        return fields


@click.command(
    context_settings=dict(help_option_names=['-h', '--help']),
    help=(
        "Creates sqlite3 database from fastq files. "
        "sample usage: brew -o output.db file1@table1 ... "
        "filen@tablen -f field1,filed2"
    )
)
@click.option(
    '-o', '--output', required=True,
    help='Output database file', type=click.Path()
)
@click.option(
    '-d', '--dryrun', default=False, is_flag=True, help='Do a fake run.'
)
@click.option(
    '-f', '--fields', default="read_identifier,sequence", type=FieldsToUse(),
    help=(
        'Comma separated field list to parse, some of %s.' %
        ','.join(sorted(DEFAULT_SPECIFICATION))
    )
)
@click.option(
    '-g', '--group_size', default=20000, type=int,
    help='How many records write to db at ones.'
)
@click.argument('fastq_files', type=FileTableParam(), nargs=-1)
def brew(**kwargs):
    main_routine(**kwargs)


if __name__ == "__main__":
    brew()
