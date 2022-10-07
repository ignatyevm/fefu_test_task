import pathlib

DEFAULT_DATASET_PATH = "{}/../../dataset.csv".format(pathlib.Path(__file__).parent.resolve())

def parse(filepath = DEFAULT_DATASET_PATH):
    authors = {}
    scientometric_databases = []
    profiles = {}
    with open(filepath, mode='r', encoding='utf-8-sig') as dataset:
        for line in dataset.readlines():
            guid, full_name, scientometric_database, document_count, citation_count, h_index, url = line.strip().split(";")
            if guid not in authors:
                authors[guid] = [guid, full_name]
            if scientometric_database not in scientometric_databases:
                scientometric_databases.append(scientometric_database)
            if (guid, scientometric_database) not in profiles:
                profiles[(guid, scientometric_database)] = [guid, scientometric_database, document_count, citation_count, h_index, url]
    return list(authors.values()), list(scientometric_databases), list(profiles.values())
