import click
from scrawl.cli import pass_context
import json
import csv

@click.command()
@click.option('--format', default='json',help="Format to export data in. Default = json")
# @click.option('--csv', is_flag=True, help="Format to export data in. Default = json")
# dont provide file ext to avoid eg .json but --format=csv
# @click.argument('filename', default='backup', type=click.File('wb'))
@click.argument('filename', default='backup', type=str)

@pass_context
def cli(ctx,format, filename):
    """
    Command to export all notes
    """
    export_format = format
    # click.echo(export_format)
    # click.pause()
    if export_format == 'json':
        filename += '.json'
        file = click.open_file(filename, 'w')
    else:
        filename += '.csv'
        file = open(filename, 'w')

    db = ctx.database()
    cursor = db.cursor()

    query_all = "SELECT * from `notes`"
    cursor.execute(query_all)
    all_rows = cursor.fetchall()

    if all_rows:
        # rows_list = []
        # for row in all_rows:
        #     rows_list.append(row)
        if export_format == 'json':
            # output = json.dumps(rows_list, sort_keys=True, indent=4)
            output = json.dumps(all_rows, sort_keys=True, indent=4)
            file.write(output)
        else:
            # csv_file = open(file, 'w', newline='')
            csv_writer = csv.writer(file)
            # [lambda row: csv_writer.writerow(row.values()) for row in all_rows]
            for row in all_rows:
                # csv_writer.writerow(row.values())
                # above line sorts the keys in desc. Prefer explicit
                csv_writer.writerow(
                    [row['id'], row['title'], row['content'], row['date_created'], row['date_modified']])
            file.close()
    else:
        click.echo('No data')

