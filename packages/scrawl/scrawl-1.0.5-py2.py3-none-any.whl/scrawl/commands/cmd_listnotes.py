import click
from scrawl.cli import pass_context


@click.command()
@click.option('--limit', '-l', default=None, type=int, help="Number of notes to display/view at a time")
@pass_context
def cli(ctx, limit):
    """
    Command to list notes \n
    e.g: \n
    scrawl2 listnotes - will list all notes \n
    scrawl2 listnotes --limit=5 - will list all notes 5 at a time
    """
    db = ctx.database()
    cursor = db.cursor()

    query_all = "SELECT * from `notes`"
    cursor.execute(query_all)
    all_notes = cursor.fetchall()
    all_notes_count = len(all_notes)

    if all_notes:
        if not limit:
            limit = len(all_notes)
        if all_notes_count % limit:
            page_count = all_notes_count // limit + 1
        else:
            page_count = all_notes_count // limit

        click.echo(
            "\n Number of notes found : {} \n".format(all_notes_count))
        click.pause()
        offset = 0
        for i in range(1, page_count + 1):
            query = "SELECT * from `notes` LIMIT {} OFFSET {}".format(
                limit, offset)

            offset += limit
            cursor.execute(query)
            notes = cursor.fetchall()
            for note in notes:
                click.echo("\n")
                title_str = "Note id : {} , created on {} , last modified on {}".format(
                    note['id'], note['date_created'], note['date_modified'])
                click.secho(title_str, bold=True)
                click.echo("." * len(title_str))
                click.echo(note['content'])
            if all_notes_count > limit and page_count != i:
                display_next = click.prompt(
                    'Type "next" to display next set of {} records. Any other key to abort'.format(all_notes_count - (limit * i)))
                # click.echo(display_next)
                if display_next != 'next':
                    break
                # click.echo('Continue? [yn] ', nl=False)
                # c = click.getchar()
                # click.echo(c)
        return
    click.echo("No notes found")
