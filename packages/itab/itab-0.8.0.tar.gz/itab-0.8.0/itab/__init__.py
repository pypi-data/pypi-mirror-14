from itab.reader import TabReader, TabDictReader
from itab.writer import TabWriter, TabDictWriter

__author__ = 'Jordi Deu-Pons'
__author_email__ = 'jordi@jordeu.net'
__version__ = '0.8.0'


def has_schema(file):
    with TabReader(file, header=[]) as reader:
        return reader.schema_url is not None


def get_schema_url_from_file(file):
    with TabReader(file, header=[]) as reader:
        return reader.schema_url

reader = TabReader
DictReader = TabDictReader

writer = TabWriter
DictWriter = TabDictWriter


