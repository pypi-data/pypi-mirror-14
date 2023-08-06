import click
from scrawl.cli import pass_context


@click.command()
@click.argument('id', type=int, default=0, required=True)
@pass_context
def cli(ctx, id):
    """
    Command to view a specific note specified by the required ID argument passed \n
    e.g scrawl viewnote 2 - will display note with ID=2 if found
    """
    if not id:
        id = click.prompt(
            'You didn"t provide the id of the note to view. Please provide one ', type=int)

    db = ctx.database()
    cursor = db.cursor()
    query = "SELECT * from `notes` where id = {}".format(id)
    cursor.execute(query)
    notes = cursor.fetchall()

    # while True:
    #     row = cursor.fetchone()
    #     if row is None:
    #         break
    if notes:
        click.echo("\n")
        title_str = "Viewing note id : {} , created on {} , last modified on {}".format(
            notes[0]['id'], notes[0]['date_created'], notes[0]['date_modified'])
        click.secho(title_str, bold=True)
        click.echo("." * len(title_str))
        click.echo(notes[0]['content'])
        return
    click.echo("No note found with id {}".format(id))
