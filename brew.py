import click

from libbuilder import main_routine


class FileTableParam(click.File):
    FNAME_TABLE_SEPARATOR = "@"

    def convert(self, value, param, ctx):
        file_name, table_name = value.split(self.FNAME_TABLE_SEPARATOR)
        convertion_result = super().convert(file_name, param, ctx)
        convertion_result.table_name = table_name
        return convertion_result


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    '-o', '--output', required=True,
    help='Output database file', type=click.Path()
)
@click.option('-d', '--dryrun', default=False, is_flag=True)
@click.argument('fastq_files', type=FileTableParam(), nargs=-1)
def builder(**kwargs):
    main_routine(**kwargs)


if __name__ == "__main__":
    builder()
