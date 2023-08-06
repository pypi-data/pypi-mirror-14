import click
from scrawl.cli import pass_context


@click.command()
@click.argument('query_str', default="", type=str,required=True)
@click.option('--limit', '-l', default=None, type=int,help="Number of notes matched to display/view at a time")
@pass_context
def cli(ctx,query_str, limit):
    """
    Command to search notes and display results \n
    e.g: \n
    scrawl2 searchnotes andela - will list all notes matching 'andela' \n
    scrawl2 searchnotes andela --limit=5 - will list all notes matching 'andela' , 5 at a time
    """
    if not query_str:
        query_str = click.prompt(click.style('Please specify search string',fg="white",bg="red")+'\n', type=str)

    db = ctx.database()
    cursor = db.cursor()

    query_all = "SELECT * from `notes` WHERE content like '%{}%'".format(
        query_str)
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
            click.style("Number of notes matching the search ",bold=True, fg="green") + \
            click.style("{}:".format(query_str), bold=True, fg="cyan") + \
            click.style(" {}".format(all_notes_count), bold=True, fg="green")
            )
        click.pause()


        offset = 0
        for i in range(1, page_count + 1):
            query = "SELECT * from `notes` WHERE content like '%{}%' LIMIT {} OFFSET {}".format(
                query_str, limit, offset)
            offset += limit
            cursor.execute(query)
            notes = cursor.fetchall()
            for note in notes:
                click.echo("\n")
                title_str = "{} - created on {} , last modified on {}".format(
                    note['title'], note['date_created'], note['date_modified'])
                click.secho(title_str, bold=True,fg="white")
                # click.echo("." * len(title_str))
                highlighted = note['content'].replace(query_str, click.style(query_str, bg="cyan",fg="white"))
                click.secho(highlighted,fg="cyan")
            if all_notes_count > limit and page_count != i:
                display_next = click.prompt(
                    click.style('\n Type ', fg="magenta") + \
                    click.style("next", fg="green")+ \
                    click.style(' to display next set of', fg="magenta") + \
                    click.style(' {} '.format(all_notes_count - (limit * i)),bold=True, fg="green") + \
                    click.style('records. Any other key to abort',fg="magenta")
                    )
                if display_next != 'next':
                    break

                # click.echo('Continue? [yn] ', nl=False)
                # c = click.getchar()
                # click.echo(c)

        return
    click.echo(
            click.style("No notes found matching search string : ", fg="green") + \
            click.style("{}:".format(query_str), bold=True, fg="cyan")
            )
