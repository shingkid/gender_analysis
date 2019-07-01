import gzip
import os
import pickle
import urllib.request

from pathlib import Path
import codecs

import seaborn as sns

DEBUG = False

BASE_PATH = Path(os.path.abspath(os.path.dirname(__file__)))

METADATA_LIST = ['author', 'date', 'title', 'country_publication', 'author_gender',
                 'subject', 'notes']

INITIAL_BOOK_STORE = r'corpora/test_books_30'
#TODO: change to actual directory when generating corpus

# plus some extras
AUTHOR_NAME_REGEX = r"(?P<last_name>(\w+ )*\w*)\, (?P<first_name>(\w+\.* )*(\w\.*)*)(?P<suffix>\, \w+\.)*(\((?P<real_name>(\w+ )*\w*)\))*"
outputDir = 'converted'

# TODO(elsa): Investigate doctest errors in this file, may be a result of
# my own system, not actual code errors


class FileLoaderMixin:
    """ The FileLoaderMixin loads files either locally or
    remotely from Github (if run from an ipython notebook)

    Currently supported filetypes are: .csv, .txt
    """

    def load_file(self, file_path):
        """
        Loads csv and txt files either locally or remotely from Github.
        file_path can be string or Path object.

        When loading a txt file, load_file returns the text as a string

        >>> from pathlib import Path
        >>> from gender_analysis import common

        >>> f = common.FileLoaderMixin()
        >>> novel_path = Path('testing', 'corpora', 'sample_novels',
        ...                   'texts', 'austen_persuasion.txt')
        >>> novel_text = f.load_file(novel_path)
        >>> type(novel_text), len(novel_text)
        (<class 'str'>, 486253)

        csv files are returned as a list of strings, which can be
        further processed with Python's csv module

        >>> corpus_metadata_path = Path('testing', 'corpora', 'sample_novels',
        ...                             'sample_novels.csv')
        >>> corpus_metadata = f.load_file(corpus_metadata_path)
        >>> type(corpus_metadata)
        <class 'list'>

        file_path can be a string or Path object

        >>> import os
        >>> novel_path_str = os.sep.join(['testing', 'corpora', 'sample_novels',
        ...                               'texts', 'austen_persuasion.txt'])
        >>> novel_text_str = f.load_file(novel_path_str)
        >>> novel_text == novel_text_str
        True
        >>> novel_path2 = Path(r"testing/corpora/test_books_30/20-0.txt")
        >>> paradise_lost = f.load_file(novel_path2)
        >>> paradise_lost[1:61]
        'The Project Gutenberg EBook of Paradise Lost, by John Milton'

        Returns a str (txt file) or list of strs (csv file)
        """
        # if the file_path is a string, turn to Path object.
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # make sure that we only try to load supported file types
        supported_file_types = {'.csv', '.txt'}
        current_file_type = file_path.parts[-1][file_path.parts[-1].rfind('.'):]
        if current_file_type not in supported_file_types:
            err = "The FileLoaderMixin currently supports "
            err += "{supported_file_types} but not {current_file_type}."
            raise ValueError(err)

        # check if we are working locally and in the correct directory
        # __file__ is only available if executed from a file but
        # not from an ipython shell or notebook
        # in those cases, the file has to be loaded remotely from github.
        try:
            local_path = os.path.abspath(os.path.dirname(__file__))
            is_local = True
            if not local_path.endswith('gender_analysis'):
                is_local = False
                warning = "WARNING: The FileLoaderMixin should be placed "
                warning += "in the main path of the gender_analysis project."
                warning += f"It's currently in {local_path}. Until the Mixin "
                warning += "is in the correct path, files are loaded "
                warning += "from Github."
                print(warning)
        except NameError:
            is_local = False

        if is_local:
            if DEBUG:
                print(f'loading {file_path} locally.')
            return self.load_file_locally(file_path, current_file_type)
        else:
            if DEBUG:
                print(f'loading {file_path} remotely')
            return self.load_file_remotely(file_path, current_file_type)

    @staticmethod
    def load_file_locally(file_path, current_file_type):
        # I need a way of getting the local path to the base of the repo.
        # This file is currently in the base of the
        # repo so it returns the correct path. But it will change once
        # this function gets moved.
        local_base_path = Path(os.path.abspath(os.path.dirname(__file__)))
        file = open(local_base_path.joinpath(file_path), encoding='utf-8')

        if current_file_type == '.csv':
            result = file.readlines()
        elif current_file_type == '.txt':
            try:
                result = file.read()
            except UnicodeDecodeError as err:
                print(f'File loading error with {file_path}.')
                raise err

        else:
            raise Exception(
                'Cannot load if current_file_type is not .csv or .txt')

        file.close()
        return result


class MissingMetadataError(Exception):
    """Raised when a function that assumes certain metadata is called on a corpus without that
    metadata"""
    pass


def store_pickle(obj, filename):
    """
    Store a compressed "pickle" of the object in the "pickle_data" directory
    and return the full path to it.

    The filename should not contain a directory or suffix.

    Example in lieu of Doctest to avoid writing out a file.

        my_object = {'a': 4, 'b': 5, 'c': [1, 2, 3]}
        gender_analysis.common.store_pickle(my_object, 'example_pickle')

    :param obj: Any Python object to be pickled
    :param filename: str | Path
    :return: Path
    """
    filename = BASE_PATH / 'pickle_data' / (str(filename) + '.pgz')
    with gzip.GzipFile(filename, 'w') as fileout:
        pickle.dump(obj, fileout)
    return filename


def load_pickle(filename):
    """
    Load the pickle stored at filename where filename does not contain a
    directory or suffix.

    Example in lieu of Doctest to avoid writing out a file.

        my_object = gender_analysis.common.load_pickle('example_pickle')
        my_object
        {'a': 4, 'b': 5, 'c': [1, 2, 3]}

    :param filename: str | Path
    :return: object
    """
    raise IOError

    filename = BASE_PATH / 'pickle_data' / (str(filename) + '.pgz')
    with gzip.GzipFile(filename, 'r') as filein:
        obj = pickle.load(filein)
    return obj


def get_text_file_encoding(filepath):
    """
    For text file at filepath returns the text encoding as a string (e.g. 'utf-8')

    >>> from gender_analysis import common
    >>> from pathlib import Path
    >>> import os

    >>> path=Path(common.BASE_PATH,'testing', 'corpora','sample_novels','texts','hawthorne_scarlet.txt')
    >>> common.get_text_file_encoding(path)
    'UTF-8-SIG'

    Note: For files containing only ascii characters, this function will return 'ascii' even if
    the file was encoded with utf-8

    >>> import os
    >>> from pathlib import Path
    >>> from gender_analysis import common
    >>> text = 'here is an ascii text'
    >>> file_path = Path(common.BASE_PATH, 'example_file.txt')
    >>> with codecs.open(file_path, 'w', 'utf-8') as source:
    ...     source.write(text)
    ...     source.close()
    >>> common.get_text_file_encoding(file_path)
    'ascii'
    >>> file_path = Path(common.BASE_PATH, 'example_file.txt')
    >>> os.remove(file_path)

    :param filepath: fstr
    :return: str
    """
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()

    with open(filepath, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


def convert_text_file_to_new_encoding(source_path, target_path, target_encoding):
    """
    Converts a text file in source_path to the specified encoding in target_encoding
    Note: Currentyl only supports encodings utf-8, ascii and iso-8859-1

    :param source_path: str or Path
    :param target_path: str or Path
    :param target_encoding: str

    >>> from gender_analysis.common import BASE_PATH
    >>> text = ' ¶¶¶¶ here is a test file'
    >>> source_path = Path(BASE_PATH, 'source_file.txt')
    >>> target_path = Path(BASE_PATH, 'target_file.txt')
    >>> with codecs.open(source_path, 'w', 'iso-8859-1') as source:
    ...     source.write(text)
    >>> get_text_file_encoding(source_path)
    'ISO-8859-1'
    >>> convert_text_file_to_new_encoding(source_path, target_path, target_encoding='utf-8')
    >>> get_text_file_encoding(target_path)
    'utf-8'
    >>> import os
    >>> os.remove(source_path)
    >>> os.remove(target_path)

    :return:
    """

    valid_encodings = ['utf-8', 'utf8', 'UTF-8-SIG', 'ascii', 'iso-8859-1', 'ISO-8859-1',
                       'Windows-1252']

    # if the source_path or target_path is a string, turn to Path object.
    if isinstance(source_path, str):
        source_path = Path(source_path)
    if isinstance(target_path, str):
        target_path = Path(target_path)

    # check if source and target encodings are valid
    source_encoding = get_text_file_encoding(source_path)
    if source_encoding not in valid_encodings:
        raise ValueError('convert_text_file_to_new_encoding() only supports the following source '
                         f'encodings: {valid_encodings} but not {source_encoding}.')
    if target_encoding not in valid_encodings:
        raise ValueError('convert_text_file_to_new_encoding() only supports the following target '
                         f'encodings: {valid_encodings} but not {target_encoding}.')

    # print warning if filenames don't end in .txt
    if not source_path.parts[-1].endswith('.txt') or not target_path.parts[-1].endswith('.txt'):
        print(f"WARNING: Changing encoding to {target_encoding} on a file that does not end with "
              f".txt. Source: {source_path}. Target: {target_path}")

    with codecs.open(source_path, 'rU', encoding=source_encoding) as source_file:
        text = source_file.read()
    with codecs.open(target_path, 'w', encoding=target_encoding) as target_file:
        target_file.write(text)


def load_graph_settings(show_grid_lines=True):
    '''
    This function sets the seaborn graph settings to the defaults for our project.
    Defaults to displaying gridlines. To remove gridlines, call with False.
    :return:
    '''
    show_grid_lines_string = str(show_grid_lines)
    palette = "colorblind"
    style_name = "white"
    background_color = (252/255,245/255,233/255,0.4)
    style_list = {'axes.edgecolor': '.6', 'grid.color': '.9', 'axes.grid': show_grid_lines_string,
                  'font.family': 'serif', 'axes.facecolor':background_color,
                  'figure.facecolor':background_color}
    sns.set_color_codes(palette)
    sns.set_style(style_name, style_list)


if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test(import_plus_relative=True)  # this allows for relative calls in the import.
