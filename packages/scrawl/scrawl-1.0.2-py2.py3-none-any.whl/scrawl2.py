import click
import sqlite3
import json
import csv
from datetime import datetime, date
from collections import namedtuple, OrderedDict
from firebase import firebase


@click.group()
def scrawl2():
    """Scrawl - Python note-taking console app


    """


def dbase():
    db = sqlite3.connect('data.db')
    # prefer
    # db.row_factory = sqlite3.Row
    db.row_factory = dict_factory

    return db


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@scrawl2.command()
@click.option('--title', type=str, prompt="Must proivde a title")
# will have no impact if content is explicitly passed
@click.option('--no_editor', is_flag=True)
@click.argument('content', type=str, default="")
def createnote(title, content, no_editor):
    if not content:
        if not no_editor:
            content = click.edit('\n\n', require_save=True)
            if content is None:
                click.secho(
                    'You didn"t provide any content for the note. Createnote aborted.',fg='white',bg="red")
                return
        else:
            content = click.prompt(
                click.style('You didn"t provide any content for the note. Please provide one \n',fg='white',bg="red"), type=str)
        # return
    db = dbase()
    cursor = db.cursor()

    response = cursor.execute('''INSERT INTO notes
        (title, content, date_created,date_modified)
        VALUES(?,?,?,?)''',
                              (title, content, datetime.now(), datetime.now()))

    db.commit()
    db.close()
    click.secho(
        'Successfuly saved note id {} to the database'.format(cursor.lastrowid),bg="green",fg="white")


@scrawl2.command()
@click.argument('id', type=int, default=0)
def viewnote(id):
    if not id:
        id = click.prompt(
            click.style('You didn"t provide the id of the note to view. Please provide one \n',fg="white",bg="red"), type=int)
    db = dbase()
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
        title_str = "{} - created on {} , last modified on {}".format(
            notes[0]['title'], notes[0]['date_created'], notes[0]['date_modified'])
        click.secho(title_str, bold=True,fg="white")
        # click.echo("." * len(title_str))
        click.secho(notes[0]['content'],fg="cyan")
        return
    click.secho("No note found with id {}".format(id),fg="white",bg="red")


@scrawl2.command()
@click.argument('id', type=int, default=0)
def deletenote(id):
    if not id:
        id = click.prompt(
            click.style('You didn"t provide the id of the note to delete. Please provide one \n',fg="white",bg="red"), type=int)
    db = dbase()
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


@scrawl2.command()
@click.option('--limit', '-l', default=None, type=int)
def listnotes(limit):
    db = dbase()
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

        click.secho(
            "\n Number of notes found : {} \n".format(all_notes_count) , bold=True, fg="green")
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
                title_str = "{} - created on {} , last modified on {}".format(
                    note['title'], note['date_created'], note['date_modified'])
                click.secho(title_str, bold=True,fg="white")
                # click.echo("." * len(title_str))
                click.secho(note['content'],fg="cyan")
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
    click.echo("No notes found")


@scrawl2.command()
@click.argument('query_str', default="", type=str)
@click.option('--limit', '-l', default=None, type=int)
def searchnotes(query_str, limit):
    if not query_str:
        query_str = click.prompt(click.style('Please specify search string',fg="white",bg="red")+'\n', type=str)

    db = dbase()
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
                click.secho(note['content'],fg="cyan")
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


@scrawl2.command()
@click.option('--format', default='json')
# dont provide file ext to avoid eg .json but --format=csv
# @click.argument('filename', default='backup', type=click.File('wb'))
@click.argument('filename', default='backup', type=str)
def export(format, filename):
    export_format = format
    # click.echo(export_format)
    # click.pause()
    if export_format == 'json':
        filename += '.json'
        file = click.open_file(filename, 'w')
    else:
        filename += '.csv'
        file = open(filename, 'w')

    db = dbase()
    cursor = db.cursor()

    query_all = "SELECT * from `notes_copy`"
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
        click.echo(
                click.style("Exported ",fg="green") + \
                click.style("{}".format(len(all_rows)),fg="cyan") + \
                click.style(" notes to the file ",fg="green") + \
                click.style("{}".format(filename),fg="cyan")
                )
    else:
        click.secho('No data to export',fg="green")


@scrawl2.command()
# @click.argument('filename', default='import.json', type=click.File('r'))
@click.argument('path', default='import.json', type=click.Path(exists=True, file_okay=True, dir_okay=True, writable=True, readable=True, resolve_path=True))
@click.option('--format', default='json')
def _import(path, format):
    # click.echo(path)
    # click.pause()
    file = click.open_file(path, 'r')

    # if not file:
    #     click.echo('file doestnt exist')
    #     return

    new_data = ""
    # click.echo((file.readlines.__doc__))
    while True:
        string_from_file = file.readline()
        new_data += string_from_file
        # click.echo(type(string_from_file))
        if not string_from_file:
            break

    # new_data = file.read()

    if new_data:
        defaults = {
            'title': None,
            'content': " ",
            'date_created': datetime.now(),
            'date_modified': datetime.now()
        }
        # notes = json.loads(new_data, object_pairs_hook=namedtuple)
        # notes = json.loads(new_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        # notes = json.loads(new_data, object_hook=lambda d: tuple(d.values()))

        notes = json.loads(new_data)
        notes = [{k: note.get(k, defaults[k])
                  for k in defaults} for note in notes]
        # click.echo(notes)
        # click.pause()
        db = dbase()
        cursor = db.cursor()

        # books = [(title4, author4, price4, year4),(title5, author5, price5, year5)]
        cursor.executemany(
            # '''INSERT INTO notes(title, content, date_created, date_modified) VALUES(?,?,?,?)''', [notes])
            '''INSERT INTO notes(title, content, date_created, date_modified) VALUES(:title, :content, :date_created, :date_modified)''',
            notes)
        db.commit()
        click.echo(
                click.style("Imported ",fg="green") + \
                click.style("{}".format(len(notes)),fg="cyan") + \
                click.style(" notes from to the file ",fg="green") + \
                click.style("{}".format(file),fg="cyan")
                )
    else:
        click.secho('No data to import',fg="white",bg="red")


@scrawl2.command()
@click.option('--url', default='https://bc-6-scrawl.firebaseio.com')
def syncnotes(url):
    firebase_instance = firebase.FirebaseApplication(url, None)
    if firebase_instance:
        db = dbase()
        cursor = db.cursor()

        query_all = "SELECT * from `notes`"
        cursor.execute(query_all)
        all_notes = cursor.fetchall()

        # result = firebase_instance.post('/notes', json.dumps(all_notes))
        # result = firebase_instance.post('/notes', all_notes)
        # Every time we send a POST request, the Firebase client generates a unique ID,
        # Thus use put


        # result = firebase_instance.put(url, 'notes', all_notes)

        with click.progressbar(all_notes,length=len(all_notes),
                       label='Syncing ...', color=True,width=0,item_show_func=lambda item: 'uploading id {}'.format(item)) as bar:
            for note in bar:
                result = firebase_instance.patch(url+'/notes', note)
                # if not result:
                #     click.secho('Could not sync notes',fg="white",bg="red")
                # else:
                #     click.secho('{} notes successfully synced'.format(len(all_notes)),fg="green")
    else:
        click.secho('Invalid url provided',fg="white",bg="red")
