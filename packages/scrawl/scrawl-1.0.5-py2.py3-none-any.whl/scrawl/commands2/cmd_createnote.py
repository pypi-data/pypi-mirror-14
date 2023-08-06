import click
from scrawl.cli import pass_context, helpers
from datetime import datetime, date

@click.command()
@click.option('--title', type=str, prompt="Must proivde a title", help="The title for the note")
# will have no impact if content is explicitly passed
@click.option('--no_editor', is_flag=True, help="Flag to disable using the system editor")
@click.argument('content', type=str, default="", required=True)
@pass_context
def cli(ctx, title, content, no_editor):
    """
    Command to create a note
    """
    if not content:
        if not no_editor:
            content = click.edit('\n\n', require_save=True)
            if content is None:
                click.secho(
                    'You didn"t provide any content for the note. Createnote aborted.', fg='white', bg="red")
                return
        else:
            content = click.prompt(
                click.style('You didn"t provide any content for the note. Please provide one \n', fg='white', bg="red"), type=str)
        # return
    db = ctx.database()
    cursor = db.cursor()

    response = cursor.execute('''INSERT INTO notes
        (title, content, date_created,date_modified, checksum)
        VALUES(?,?,?,?,?)''',
                              (" ", content, datetime.now(), datetime.now(), helpers.hashnote(content)))

    db.commit()
    db.close()
    click.secho(
        'Successfuly saved note id {} to the database'.format(cursor.lastrowid), bg="green", fg="white")
