import click
import sqlite3
import json
import csv
from datetime import datetime, date
from collections import namedtuple, OrderedDict
from firebase import firebase


@click.group()
def scrawl():
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


@scrawl.command()
@click.argument('content', type=str, default="")
def createnote(content):
    if not content:
        content = click.prompt(
            'You didn"t provide any content for the note. Please provide one \n', type=str)
        # return
    db = dbase()
    cursor = db.cursor()

    response = cursor.execute('''INSERT INTO notes
        (title, content, date_created,date_modified)
        VALUES(?,?,?,?)''',
                              (" ", content, datetime.now(), datetime.now()))

    db.commit()
    db.close()
    click.echo(
        'Successfuly saved note id {} to the database'.format(cursor.lastrowid))


@scrawl.command()
@click.argument('id', type=int, default=0)
def viewnote(id):
    if not id:
        id = click.prompt(
            'You didn"t provide the id of the note to view. Please provide one \n', type=int)
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
        title_str = "Viewing note id : {} , created on {} , last modified on {}".format( \
            notes[0]['id'], notes[0]['date_created'], notes[0]['date_modified'])
        click.secho(title_str, bold=True)
        click.echo("." * len(title_str))
        click.echo(notes[0]['content'])
        return
    click.echo("No note found with id {}".format(id))


@scrawl.command()
@click.argument('id', type=int, default=0)
def deletenote(id):
    if not id:
        id = click.prompt(
            'You didn"t provide the id of the note to view. Please provide one \n', type=int)
    db = dbase()
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


@scrawl.command()
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
            "Number of notes found : '{}".format(all_notes_count), bold=True)
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
        click.secho(
            "Number of notes found : '{}".format(all_notes_count), bold=True)
        return
    click.echo("No notes found")


@scrawl.command()
@click.argument('query_str', default="", type=str)
@click.option('--limit', '-l', default=None, type=int)
def searchnotes(query_str, limit):
    if not query_str:
        query_str = click.prompt('Please specify search string \n', type=str)

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
            "Number of notes matching the search '{}': {}".format(query_str, all_notes_count))
        offset = 0
        for i in range(1, page_count + 1):
            query = "SELECT * from `notes` WHERE content like '%{}%' LIMIT {} OFFSET {}".format(
                query_str, limit, offset)
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
                click.echo(display_next)
                if display_next != 'next':
                    break

                # click.echo('Continue? [yn] ', nl=False)
                # c = click.getchar()
                # click.echo(c)

        return
    click.echo("No notes found")


@scrawl.command()
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


@scrawl.command()
# @click.argument('filename', default='import.json', type=click.File('r'))
@click.argument('path', default='import.json', type=click.Path(exists=True, file_okay=True, dir_okay=True, writable=True, readable=True, resolve_path=True))
@click.option('--format', default='json')
def _import(path, format):
    click.echo(path)
    click.pause()
    file = click.open_file(path, 'r')

    if not file:
        click.echo('file doestnt exist')
        return

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
    else:
        click.echo('No data ')


@scrawl.command()
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
        result = firebase_instance.put(url, 'notes', all_notes)
        if not result:
            click.echo('Could not sync notes')
    else:
        click.echo('Invalid url provided')
