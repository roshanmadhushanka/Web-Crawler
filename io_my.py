# -*- coding: utf-8 -*-
import os.path


class FileHandler:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        '''
        Read from a specific file
        :return:
        '''
        _file = None
        _lines = None
        try:
            _file = open(self.file_name, 'r', encoding='utf-8')
            _lines = _file.readlines()
            _lines = [a.rstrip() for a in _lines if a != '\n']
        except IOError:
            print("IO Error")
            pass
        finally:
            if _file is not None:
                _file.close()
        return _lines

    def append(self, content):
        '''
        Append lines to a specific file
        :param content: String
        :return: None
        '''
        _file = None
        try:
            _file = open(self.file_name, 'a', encoding='utf-8')
            if isinstance(content, str):
                _file.write(content + '\n')
            elif isinstance(content, list):
                for line in content:
                    _file.write(line.encode('utf-8') + '\n')
        except IOError:
            print('IO Error')
            return
        finally:
            if _file is not None:
                _file.close()

    def write(self, content):
        '''
        Write contents to a specific file
        :param content: can be a string or list of strings
        :return: None
        '''
        _file = None
        try:
            _file = open(self.file_name, 'w', encoding='utf-8')
            if isinstance(content, str):
                _file.write(content)
            elif isinstance(content, list):
                content = [a + '\n' for a in content]
                _file.writelines(content)
        except IOError:
            pass
        finally:
            if _file is not None:
                _file.close()


class CSVWriter:

    def __init__(self, file_name):
        self._file_name = file_name
        self._headers = ['Internationale Vorwahl', 'Telefon', 'Telefax', 'Email', 'Internet', 'Bankverbindung', 'Straße-Adresse', 'Hausnummer', 'PLZ', 'Ort', 'Regierungsbezirk', 'Bundesland', 'Land', 'Zusätzl. Informationen', 'Rechtsform (kurz)', 'Hauptbranche WZ 2008', 'Top-Management']
        if not os.path.exists(file_name):
            self.setHeaders()

    def setHeaders(self):
        _file = None
        try:
            _file = open(self._file_name, 'w', encoding='utf-8')
            _file.write("'Company Name', 'Internationale Vorwahl', 'Telefon', 'Telefax', 'Email', 'Internet', 'Bankverbindung', 'Straße-Adresse', 'Hausnummer', 'PLZ', 'Ort', 'Regierungsbezirk', 'Bundesland', 'Land', 'Zusätzl. Informationen', 'Rechtsform (kurz)', 'Hauptbranche WZ 2008', 'Top-Management'\n")
        except IOError:
            pass
        finally:
            if _file is not None:
                _file.close()

    def append(self, content):
        '''
        Append lines to a specific file
        :param content: String
        :return: None
        '''

        if not isinstance(content, dict):
            return

        data = {'Company Name': 'N/A', 'Internationale Vorwahl': 'N/A', 'Telefon': 'N/A', 'Telefax': 'N/A', 'Email': ' N/A',
                'Internet': 'N/A', 'Bankverbindung': 'N/A', 'Straße-Adresse': 'N/A', 'Hausnummer': 'N/A',
                'PLZ': 'N/A', 'Ort': 'N/A', 'Regierungsbezirk': 'N/A', 'Bundesland': 'N/A', 'Land': 'N/A',
                'Zusätzl. Informationen': 'N/A', 'Rechtsform (kurz)': 'N/A', 'Hauptbranche WZ 2008': 'N/A',
                'Top-Management': 'N/A'}

        for key in content.keys():
            data[key] = content[key]

        str_row = data[list(data.keys())[0]]
        for key in list(data.keys())[1:]:
            str_row += ',' + data[key]

        str_row = str_row.strip()
        str_row = str_row.replace("\n", "")
        print(str_row)

        _file = None
        try:
            _file = open(self._file_name, 'a', encoding='utf-8')
            _file.write(str_row + '\n')
        except IOError:
            print('IO Error')
            return
        finally:
            if _file is not None:
                _file.close()





