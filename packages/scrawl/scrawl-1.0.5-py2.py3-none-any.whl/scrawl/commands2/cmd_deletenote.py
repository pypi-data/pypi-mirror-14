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
            click.style('You didn"t provide the id of the note to delete. Please provide one',fg="white",bg="red"), type=int)
    db = ctx.database()
    cursor = db.cursor()
    query = "SELECT * from `notes` where id = {}".format(id)
    cursor.execute(query)
    notes = cursor.fetchall()

    if notes:
        if click.confirm(click.style('Are you sure?',fg="magenta")):
            query = "DELETE from `notes` where id = {}".format(id)
            cursor.execute(query)
            db.commit()
            click.secho("Note with id {} has been deleted".format(id),fg="white",bg="green")
        else:
            click.secho("Nothing deleted. Delete action aborted.",fg="white",bg="green")
        return
    click.secho("No note found with id {}. Delete action aborted.".format(id),fg="white",bg="red")
