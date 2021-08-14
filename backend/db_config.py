from configparser import ConfigParser

def read_db_config(filename='config.ini',section='mysql'):

    parser = ConfigParser()
    parser.read(filename)

    db_params = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_params[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in {filename}')

    return db_params