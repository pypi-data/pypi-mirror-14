from os.path import abspath, dirname, join

TEST_DIR = dirname(abspath(__file__))
TEST_DATA_DIR = join(TEST_DIR, 'data')


def get_data_path(name):
    return join(TEST_DATA_DIR, name)


def get_data_string(name):
    with open(get_data_path(name), 'r') as data_file:
        return data_file.read()
