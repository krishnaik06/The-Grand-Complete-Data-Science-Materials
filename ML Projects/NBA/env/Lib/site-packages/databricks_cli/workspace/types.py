# Databricks CLI
# Copyright 2017 Databricks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"), except
# that the use of services to which certain application programming
# interfaces (each, an "API") connect requires that the user first obtain
# a license for the use of the APIs from Databricks, Inc. ("Databricks"),
# by creating an account at www.databricks.com and agreeing to either (a)
# the Community Edition Terms of Service, (b) the Databricks Terms of
# Service, or (c) another written agreement between Licensee and Databricks
# for the use of the APIs.
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from click import ParamType


class WorkspaceLanguage(object):
    SCALA = 'SCALA'
    PYTHON = 'PYTHON'
    SQL = 'SQL'
    R = 'R'
    ALL = [SCALA, PYTHON, SQL, R]
    EXTENSIONS = ['.scala', '.py', '.sql', '.SQL', '.r', '.R', '.ipynb', '.html', '.dbc']

    @classmethod
    def to_language_and_format(cls, path):
        ext = cls.get_extension(path).lower()
        language_and_format = (None, None)
        if ext == '.scala':
            language_and_format = (cls.SCALA, WorkspaceFormat.SOURCE)
        elif ext == '.py':
            language_and_format = (cls.PYTHON, WorkspaceFormat.SOURCE)
        elif ext == '.sql':
            language_and_format = (cls.SQL, WorkspaceFormat.SOURCE)
        elif ext == '.r':
            language_and_format = (cls.R, WorkspaceFormat.SOURCE)
        elif ext == '.ipynb':
            language_and_format = (cls.PYTHON, WorkspaceFormat.JUPYTER)
        elif ext == '.html':
            language_and_format = (None, WorkspaceFormat.HTML)
        elif ext == '.dbc':
            language_and_format = (None, WorkspaceFormat.DBC)
        return language_and_format

    @classmethod
    def to_extension(cls, language):
        if language == cls.SCALA:
            return '.scala'
        elif language == cls.PYTHON:
            return '.py'
        elif language == cls.SQL:
            return '.sql'
        elif language == cls.R:
            return '.r'

    @classmethod
    def get_extension(cls, path):
        for ext in cls.EXTENSIONS:
            if path.endswith(ext):
                return ext
        return ''


class LanguageClickType(ParamType):
    name = 'Language'

    def convert(self, value, param, ctx):
        converted = value.upper()
        if converted not in WorkspaceLanguage.ALL:
            languages = ', '.join(WorkspaceLanguage.ALL)
            self.fail('Language must be one of: {}'.format(languages))
        return converted


class WorkspaceFormat(object):
    SOURCE = 'SOURCE'
    HTML = 'HTML'
    JUPYTER = 'JUPYTER'
    DBC = 'DBC'
    ALL = [SOURCE, HTML, JUPYTER, DBC]


class FormatClickType(ParamType):
    name = 'Format'

    def convert(self, value, param, ctx):
        converted = value.upper()
        if converted not in WorkspaceFormat.ALL:
            formats = ', '.join(WorkspaceFormat.ALL)
            self.fail('Format must be one of: {}'.format(formats))
        return converted
