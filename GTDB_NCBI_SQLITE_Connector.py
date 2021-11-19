import os

SPLITTER='/'

from util import RESOURCES_FOLDER,download_file,uncompress_archive,file_exists


class GTDB_SQLITE_Connector():
    '''
    this just creates an sql database from two gtdb files to convert gtdb to ncbi. first we download them and create the db
    then anytime we need to fetch info we just open the db, fetch the info, and close the connection
    '''
    def __init__(self):
        self.insert_step=50000
        self.db_file = f'{RESOURCES_FOLDER}gtdb_to_ncbi.db'
        if os.path.exists(self.db_file):
            self.start_sqlite_cursor()
        else:
            self.create_sql_table()


    def start_sqlite_cursor(self):
        self.sqlite_connection = sqlite3.connect(self.db_file)
        self.cursor = self.sqlite_connection.cursor()

    def commit_and_close_sqlite_cursor(self):
        self.sqlite_connection.commit()
        self.sqlite_connection.close()

    def close_sql_connection(self):
        self.sqlite_connection.close()

    def check_all_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = self.cursor.fetchall()
        print(all_tables)

    def process_gtdb_taxonomy(self,gtdb_lineage):
        res = None
        temp=gtdb_lineage.split(';')
        temp = ['_'.join(i.split('_')[2:]) for i in temp]
        while temp and not res:
            res = temp.pop(-1).strip()
        return res

    def read_gtdb_tsv(self,gtdb_tsv):
        res=[]
        with open(gtdb_tsv) as file:
            file.readline()
            for line in file:
                line = line.strip('\n')
                line = line.split('\t')
                gtdb_taxonomy = line[16]
                most_resolved = self.process_gtdb_taxonomy(gtdb_taxonomy)
                ncbi_id = line[77]
                res.append([most_resolved, ncbi_id])
        return res

    def download_data(self):
        url = 'https://data.gtdb.ecogenomic.org/releases/latest/'
        ar_url = f'{url}ar122_metadata.tar.gz'
        bac_url = f'{url}bac120_metadata.tar.gz'

        ar_file = f'{RESOURCES_FOLDER}ar122_metadata.tar.gz'
        bac_file = f'{RESOURCES_FOLDER}bac120_metadata.tar.gz'

        try:
            ar_file_unc = [i for i in os.listdir(RESOURCES_FOLDER) if i.startswith('ar122') and i.endswith('.tsv')][0]
            ar_file_unc = f'{RESOURCES_FOLDER}{ar_file_unc}'
        except:
            ar_file_unc = None
        try:
            bac_file_unc = [i for i in os.listdir(RESOURCES_FOLDER) if i.startswith('bac120') and i.endswith('.tsv')][0]
            bac_file_unc = f'{RESOURCES_FOLDER}{bac_file_unc}'
        except:
            bac_file_unc = None

        if file_exists(ar_file) or file_exists(ar_file_unc):
            pass
        else:
            download_file(ar_url, output_folder=RESOURCES_FOLDER)

        if file_exists(bac_file) or file_exists(bac_file_unc):
            pass
        else:
            download_file(bac_url, output_folder=RESOURCES_FOLDER)

        if file_exists(ar_file):         uncompress_archive(ar_file, remove_source=True)
        if file_exists(bac_file):        uncompress_archive(bac_file, remove_source=True)
        self.bac_file = [i for i in os.listdir(RESOURCES_FOLDER) if i.startswith('bac120') and i.endswith('.tsv')][0]
        self.ar_file = [i for i in os.listdir(RESOURCES_FOLDER) if i.startswith('ar122') and i.endswith('.tsv')][0]
        self.bac_file=f'{RESOURCES_FOLDER}{self.bac_file}'
        self.ar_file=f'{RESOURCES_FOLDER}{self.ar_file}'

    def create_sql_table(self):
        self.download_data()
        #this will probably need to be changed to an output_folder provided by the user
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        self.sqlite_connection = sqlite3.connect(self.db_file)
        self.cursor = self.sqlite_connection.cursor()

        create_table_command = f'CREATE TABLE GTDB2NCBI (' \
                            f'GTDB TEXT,' \
                            f'NCBI  INTEGER )'
        self.cursor.execute(create_table_command)
        self.sqlite_connection.commit()
        self.store_gtdb2ncbi()


    def generate_inserts(self, chebi2others):
        step=self.insert_step
        for i in range(0, len(chebi2others), step):
            yield chebi2others[i:i + step]


    def store_gtdb2ncbi(self):

        gtdb2ncbi=self.read_gtdb_tsv(self.bac_file)+self.read_gtdb_tsv(self.ar_file)
        generator_insert = self.generate_inserts(gtdb2ncbi)
        for table_chunk in generator_insert:
            insert_command = f'INSERT INTO GTDB2NCBI (GTDB, NCBI) values (?,?)'
            self.cursor.executemany(insert_command, table_chunk)
        self.sqlite_connection.commit()

    def fetch_ncbi_id(self,gtdb_lineage):
        res=set()
        gtdb_id=self.process_gtdb_taxonomy(gtdb_lineage)
        fetch_command = f'SELECT GTDB,NCBI FROM GTDB2NCBI WHERE GTDB = "{gtdb_id}"'
        res_fetch=self.cursor.execute(fetch_command).fetchall()
        for i in res_fetch:
            res.add(i[1])
        return res

    def fetch_gtdb_id(self,ncbi_id):
        res=set()
        fetch_command = f"SELECT GTDB,NCBI FROM GTDB2NCBI WHERE NCBI = {ncbi_id}"
        res_fetch=self.cursor.execute(fetch_command).fetchall()
        for i in res_fetch:
            res.add(i[0])
        return res




if __name__ == '__main__':
    gtdb_connector=GTDB_SQLITE_Connector()
    a=gtdb_connector.fetch_ncbi_id('d__Archaea;p__Halobacteriota;c__Methanosarcinia;o__Methanosarcinales;f__Methanosarcinaceae;g__Methanolobus;s__Methanolobus psychrophilus')
    print(a)
    a=gtdb_connector.fetch_ncbi_id('s__Methanolobus psychrophilus')
    print(a)
    a=gtdb_connector.fetch_gtdb_id('1094980')
    print(a)