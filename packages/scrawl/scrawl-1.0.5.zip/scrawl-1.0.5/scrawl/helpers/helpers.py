import hashlib


def hashnote(note_content):
    m = hashlib.sha224(note_content).hexdigest()
    return m


def to_sync(master, child):
    data_to_sync = []
    for note in master:
        # print type(master)
        # if isinstance(master, dict):
        #     note = master.values()[-1]
        found = False
        for child_note in child:
            # print type(child_note)
            if child_note['checksum'] != note['checksum']:
                found = True
                break
        if not found:
            data_to_sync.append(note)
    return data_to_sync
