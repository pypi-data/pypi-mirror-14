import click
from scrawl.cli import pass_context



@click.command()
@click.argument('id', type=int, default=0,required=True)
@pass_context
def cli(ctx,id):
    """
    Command to delete a specific note specified by the required ID argument passed \n
    e.g scrawl deletenote 2 - will delete note with ID=2 if found
    """
    if not id:
        id = click.prompt(
            'You didn"t provide the id of the note to view. Please provide one \n', type=int)
    db = ctx.database()
    cursor = db.cursor()
    query = "SELECT * from `notes` where id = {}".format(id)
    cursor.execute(query)
    notes = cursor.fetchall()

    if notes:
        if click.confirm('Are you sure?'):
            query = "DELETE from `notes` where id = {}".format(id)
            cursor.execute(query)
            db.commit()
            click.echo("Note with id {} has been deleted".format(id))
        else:
            click.echo("Delete action aborted.")
        return
    click.echo("No note found with id {}".format(id))
