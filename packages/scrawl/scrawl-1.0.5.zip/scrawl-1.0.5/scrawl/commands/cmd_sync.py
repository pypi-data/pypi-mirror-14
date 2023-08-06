import click
from scrawl.cli import pass_context, helpers
from firebase import firebase

@click.command()
@click.option('--url', default='https://bc-6-scrawl.firebaseio.com', help="url to the firebase app. \n default = https://bc-6-scrawl.firebaseio.com")
@pass_context
def cli(ctx, url):
    """
    Command to sync notes with Firebase
    """
    firebase_instance = firebase.FirebaseApplication(url + '/notes', None)
    if firebase_instance:
        db = ctx.database()
        cursor = db.cursor()

        query_all = "SELECT * from `notes`"
        cursor.execute(query_all)
        all_notes = cursor.fetchall()
        from_firebase = firebase_instance.get('/notes',None)

        print from_firebase
        from_firebase_listed = []
        if not from_firebase:
            from_firebase = []

        for firebase_key in from_firebase:
            # print firebase_note
            from_firebase_listed.append(from_firebase[firebase_key])


        to_download = helpers.to_sync(from_firebase_listed, all_notes)

        to_upload = helpers.to_sync(all_notes, from_firebase_listed)

        print to_download

        # combined = to_download + to_upload

        # upload
        with click.progressbar(to_upload, length=len(to_upload),
                               label='Syncing ...', color=True, width=0) as bar:
            for note in bar:
                result = firebase_instance.put(url , 'notes/{}'.format(note['checksum']), note)

        # download
        with click.progressbar(to_download, length=len(to_download),
                               label='Syncing ...', color=True, width=0) as bar:
            for note in bar:
                cursor.execute('''INSERT INTO notes
        (title, content, date_created,date_modified, checksum)
        VALUES(?,?,?,?,?)''',
                               (note['title'], note['content'], note['date_created'], note['date_modified'], note['checksum']))

                db.commit()
    else:
        click.secho('Invalid url provided', fg="white", bg="red")
