import os
import shutil
import sqlite3


class PyPhDB:

    def __init__(self):

        self.path_pihole_dir = r'/etc/pihole'
        self.path_pihole_db = os.path.join(self.path_pihole_dir, 'gravity.db')
        self.path_output_dir = os.path.join(self.path_pihole_dir, 'PyPhDB')
        self.connection = None
        self.cursor = None

        self.set_adlists = set()
        self.set_blacklist = set()
        self.set_whitelist = set()
        self.set_bl_regexps = set()
        self.set_wl_regexps = set()
        self.set_gravity = set()

    def access_check(self):

        if os.path.exists(self.path_pihole_dir):
            print('[i] Pi-hole directory located')
            if os.access(self.path_pihole_dir, os.X_OK | os.W_OK):
                print('[i] Write access is available to Pi-hole directory')
                # Does the DB exist
                # and is the file size greater than 0 bytes
                if os.path.isfile(self.path_pihole_db) and os.path.getsize(self.path_pihole_db) > 0:
                    print('[i] Pi-hole DB located')
                    return True
                else:
                    print('[e] Write access is available but the Pi-hole DB does not exist')
                    return False
            else:
                print('[e] Write access is not available to the Pi-hole directory.')
                return False
        else:
            print('[e] Pi-hole directory was not found!')
            return False

    def make_connection(self):

        try:
            self.connection = sqlite3.connect(self.path_pihole_db)
        except sqlite3.Error as e:
            print('[e] Failed to connected to Pi-hole DB')
            return False

        print('[i] Connection established to Pi-hole DB')

        self.cursor = self.connection.cursor()

        return True

    def close_connection(self):

        print('[i] Closing connection to the Pi-hole DB')
        self.connection.close()

    def fetch_data(self):

        # adlists.list
        print('[i] Fetching adlists')
        self.cursor.execute('SELECT address FROM adlist')
        self.set_adlists.update(x[0] for x in self.cursor.fetchall())

        # whitelist.list
        print('[i] Fetching whitelist')
        self.cursor.execute('SELECT domain FROM domainlist WHERE type = 0')
        self.set_whitelist.update(x[0] for x in self.cursor.fetchall())

        # blacklist.list
        print('[i] Fetching blacklist')
        self.cursor.execute('SELECT domain FROM domainlist WHERE type = 1')
        self.set_blacklist.update(x[0] for x in self.cursor.fetchall())

        # whitelist_regex.list
        print('[i] Fetching whitelist regexps')
        self.cursor.execute('SELECT domain FROM domainlist WHERE type = 2')
        self.set_wl_regexps.update(x[0] for x in self.cursor.fetchall())

        # regex.list
        print('[i] Fetching blacklist regexps')
        self.cursor.execute('SELECT domain FROM domainlist WHERE type = 3')
        self.set_bl_regexps.update(x[0] for x in self.cursor.fetchall())

        # gravity.list
        print('[i] Fetching gravity domains')
        self.cursor.execute('SELECT distinct(domain) FROM gravity')
        self.set_gravity.update(x[0] for x in self.cursor.fetchall())

    def stage_output(self):

        # Create /etc/pihole/PyPhDB
        if not os.path.exists(self.path_output_dir):
            print('[i] Creating output directory')
            os.mkdir(self.path_output_dir)

    def dump_data(self):

        self.stage_output()

        # Create a dictionary for easier output
        dict_output = {
            'adlists.list': self.set_adlists,
            'whitelist.list': self.set_whitelist,
            'blacklist.list': self.set_blacklist,
            'whitelist_regex.list': self.set_wl_regexps,
            'regex.list': self.set_bl_regexps,
            'gravity.list': self.set_gravity
        }

        # Iterate through dictionary
        for k, v in dict_output.items():
            # If the set is not empty
            if v:
                self.output_file(k, v)

    def output_file(self, file_name, results):

        path_file = os.path.join(self.path_output_dir, file_name)

        print(f'[i] {file_name}:')
        print(f'    --> Outputting {len(results)} lines to {path_file}')

        with open(path_file, 'w') as fWrite:
            for line in sorted(results):
                fWrite.write(f'{line}\n')

    def clean_dump(self):
        if os.path.exists(self.path_output_dir):
            print('[i] Removing output directory')
            shutil.rmtree(self.path_output_dir)


# Create a new instance
PyPhDB_inst = PyPhDB()

# Access check for DB
if PyPhDB_inst.access_check():
    # If we're able to access the DB
    if PyPhDB_inst.make_connection():
        # Populate sets with data from DB
        PyPhDB_inst.fetch_data()
        # Close the connection to the DB
        PyPhDB_inst.close_connection()
        # Dump data to disk
        PyPhDB_inst.dump_data()
    else:
        exit(1)
else:
    exit(1)
