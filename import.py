import sqlite3
import re


# this is a script to import narratives from the msdos file


def parse_file(file_path):
    data = []
    print("importing")
    id_ = None
    description = ''
    test = ''
    pass_ = ''
    fail = ''
    skip = ''
    phase = 0
    with open(file_path, 'r', errors="ignore") as file:
        for line in file:
            match = re.match(r'(\d+.\d.\d)', line)
            # print(match)
            if match:
                if id_ != match.group(1) and id_ is not None:
                    phase = 0
                    # print("id:" + id_)
                    # print("---------------------------------------------------------------")
                    # print("des" + description)
                    # print("---------------------------------------------------------------")
                    # print("pass:" + pass_)
                    # print("---------------------------------------------------------------")
                    # print("Fail: " + fail)
                    dataarray = (id_, description, pass_, fail, skip)
                    data.append(dataarray)
                    id_ = match.group(1)
                    description = ''
                    # test = []
                    pass_ = ''
                    fail = ''
                    skip = ''
                elif id_ is None:
                    id_ = match.group(1)

            if phase == 0:
                if "PASS:" in line:
                    phase = 1
                    cur = line.rfind(':')
                    pass_ += line[cur + 1:]
                else:
                    if id_ is not None:
                        if id_ in line:
                            pass
                        else:
                            description += line
            elif phase == 1:
                if "FAIL:" in line:
                    phase = 2
                    cur = line.rfind(':')
                    fail += line[cur + 1:]
                else:
                    pass_ += line
            elif phase == 2:
                if "SKIP:" in line:
                    phase = 3
                    cur = line.rfind(':')
                    skip += line[cur+1:]
                else:
                    fail += line
            elif phase == 3:
                skip += line
    return data


def insert_into_db(db_path, data):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            description TEXT,
            pass TEXT,
            fail TEXT,
            skip TEXT
        )
    ''')

    # Insert a row of data
    c.executemany('INSERT INTO entries VALUES (?, ?, ?, ?, ?)', data)

    # Save (commit) the changes
    conn.commit()

    # Close connection
    conn.close()


def main():
    file_path = 'importmsdos.txt'  # Change this to your file path
    db_path = 'sqlite.db'  # Change this to your SQLite DB path
    data = parse_file(file_path)
    insert_into_db(db_path, data)


if __name__ == '__main__':
    main()
