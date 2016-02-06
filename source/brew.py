import click

from .libbuilder import main_routine
from .libbuilder.specification import default_specification


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


@click.command(
    context_settings=dict(help_option_names=['-h', '--help']),
    help="Creates sqlite3 database from fastq files."
)
@click.option(
    '-o', '--output', required=True,
    help='Output database file', type=click.Path()
)
@click.option(
    '-d', '--dryrun', default=False, is_flag=True, help='Do a fake run.'
)
@click.option(
    '-f', '--fields', default="read_identifier,sequence",
    help=(
        'Fileds to parse, some of \n%s.' %
        ', '.join(sorted(default_specification))
    )
)
@click.argument('fastq_files', type=FileTableParam(), nargs=-1)
def brew(**kwargs):
    main_routine(**kwargs)


if __name__ == "__main__":
    brew()
