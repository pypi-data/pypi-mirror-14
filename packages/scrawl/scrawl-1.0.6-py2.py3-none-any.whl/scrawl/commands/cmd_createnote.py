import click
from scrawl.cli import pass_context, helpers
from datetime import datetime, date


@click.command()
@click.argument('content', type=str, default="", required=True)
@pass_context
def cli(ctx, content):
    """
    Command to create a note
    """
    if not content:
        content = click.prompt(
            'You didn"t provide any content for the note. Please provide one ', type=str)
        # return
    db = ctx.database()
    cursor = db.cursor()

    response = cursor.execute('''INSERT INTO notes
        (title, content, date_created,date_modified, checksum)
        VALUES(?,?,?,?,?)''',
                              (" ", content, datetime.now(), datetime.now(), helpers.hashnote(content)))

    db.commit()
    db.close()
    click.echo(
        'Successfuly saved note id {} to the database'.format(cursor.lastrowid))
