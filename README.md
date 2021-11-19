# DB_mappers


This repo contains some database mapping used in some of my different projects:

- CHEBI_SQLITE_Connector is a SQLite database where you can input a ChEBI ID and get all its alternative IDs (e.g., other ChEBI IDs and/or other database IDs)
- GTDB_NCBI_SQLITE_Connector is a SQLite database where you can either input a NCBI taxonomy ID or GTDB lineage and get the corresponding ID/lineage 


How to use this?

Just import the class, create a class instance and run the corresponding methods:

### CHEBI_SQLITE_Connector

```
from CHEBI_SQLITE_Connector import CHEBI_SQLITE_Connector

chebi_connector=CHEBI_SQLITE_Connector()
alternative_ids=chebi_connector.fetch_chebi_id_info('5900')
print(alternative_ids)
```

This uses the following files:
- https://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.obo.gz
- https://ftp.ebi.ac.uk/pub/databases/chebi/Flat_file_tab_delimited/database_accession.tsv

### GTDB_NCBI_SQLITE_Connector

```
from GTDB_NCBI_SQLITE_Connector import GTDB_NCBI_SQLITE_Connector

gtdb_connector=GTDB_SQLITE_Connector()
test=gtdb_connector.fetch_ncbi_id('d__Archaea;p__Halobacteriota;c__Methanosarcinia;o__Methanosarcinales;f__Methanosarcinaceae;g__Methanolobus;s__Methanolobus psychrophilus')
print(test)
test=gtdb_connector.fetch_ncbi_id('s__Methanolobus psychrophilus')
print(test)
test=gtdb_connector.fetch_gtdb_id('1094980')
print(test)

```

This uses the following files:
- https://data.gtdb.ecogenomic.org/releases/latest/ar122_metadata.tar.gz
- https://data.gtdb.ecogenomic.org/releases/latest/bac120_metadata.tar.gz