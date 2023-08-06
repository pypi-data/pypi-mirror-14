"""
    pyexcel_text.json
    ~~~~~~~~~~~~~~~~~~~

    Provide json output

    :copyright: (c) 2014-2016 by C. W.
    :license: New BSD
"""
import json

from pyexcel.sources import params

from ._text import TextSource, WriteOnlyMemorySourceMixin


file_types = ('json',)


class JsonSheetSource(TextSource):
    """
    Write a two dimensional array into json format
    """
    text_file_formats = file_types

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.write_title = write_title
        self.keywords = keywords

    def write_data(self, sheet):
        data = self._transform_data(sheet)
        with open(self.file_name, 'w') as jsonfile:
            if self.write_title:
                data = {sheet.name: data}
            self._write_sheet(jsonfile, data)

    def _write_sheet(self, jsonfile, data):
        jsonfile.write(json.dumps(data, sort_keys=True))

    def _transform_data(self, sheet):
        table = sheet.to_array()
        if hasattr(sheet, 'colnames'):
            colnames = sheet.colnames
            rownames = sheet.rownames
            # In the following, row[0] is the name of each row
            if colnames and rownames:
                table = dict((row[0], dict(zip(colnames, row[1:])))
                             for row in table[1:])
            elif colnames:
                table = [dict(zip(colnames, row)) for row in table[1:]]
            elif rownames:
                table = dict((row[0], row[1:]) for row in table)
        else:
            table = list(table)
        return table


class JsonSheetSourceInMemory(JsonSheetSource, WriteOnlyMemorySourceMixin):
    fields = [params.FILE_TYPE]
    def __init__(self, file_type=None, file_stream=None, write_title=True,
                 **keywords):
        WriteOnlyMemorySourceMixin.__init__(
            self,
            file_type=file_type,
            file_stream=file_stream,
            write_title=write_title,
            **keywords)

    def write_data(self, sheet):
        data = self._transform_data(sheet)
        if self.write_title:
            data = {sheet.name: data}
        self._write_sheet(self.content, data)


def write_json_book(jsonfile, bookdict):
    jsonfile.write(json.dumps(bookdict, sort_keys=True))


class JsonBookSourceInMemory(JsonSheetSourceInMemory):
    targets = (params.BOOK,)
    actions = (params.WRITE_ACTION,)

    def write_data(self, book):
        write_json_book(self.content, book.to_dict())


class JsonBookSource(JsonSheetSource):
    """
    Write a dictionary of two dimensional arrays into json format
    """
    targets = (params.BOOK,)
    actions = (params.WRITE_ACTION,)

    def write_data(self, book):
        with open(self.file_name, 'w') as jsonfile:
            write_json_book(jsonfile, book.to_dict())


sources = (JsonSheetSource, JsonBookSource,
           JsonSheetSourceInMemory, JsonBookSourceInMemory)

