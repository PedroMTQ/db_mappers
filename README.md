# DB_mappers


This repo contains some database mapping used in some of my different projects:

- CHEBI_SQLITE_Connector is a SQLite database where you can input a ChEBI ID and get all its alternative IDs (e.g., other ChEBI IDs and/or other database IDs)
- Rhea_SQLITE_Connector is a SQLite database where you can input a Rhea ID and get all associated information
- Taxonomy_SQLITE_Connector is a SQLite database where you can either input a NCBI taxonomy ID or GTDB lineage and get the corresponding ID/lineage. Ambiguous taxa are determined through the lowest common ancestor


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


### Rhea_SQLITE_Connector

```
from Rhea_SQLITE_Connector import Rhea_SQLITE_Connector

rhea_connector=Rhea_SQLITE_Connector()
r=rhea_connector.find_reactions_chebi('16459')
print(r)
```

This uses the following files:
- https://ftp.expasy.org/databases/rhea/tsv/rhea2uniprot.tsv
- https://ftp.expasy.org/databases/rhea/tsv/rhea2xrefs.tsv
- https://ftp.expasy.org/databases/rhea/tsv/rhea-directions.tsv
- https://ftp.expasy.org/databases/rhea/txt/rhea-reactions.txt.gz



### Taxonomy_SQLITE_Connector

```
from Taxonomy_SQLITE_Connector import Taxonomy_SQLITE_Connector

gtdb_connector=Taxonomy_SQLITE_Connector()
gtdb_connector.launch_taxonomy_connector()
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
