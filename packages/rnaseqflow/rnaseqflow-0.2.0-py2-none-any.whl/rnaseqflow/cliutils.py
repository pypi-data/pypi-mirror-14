'''
Created on Mar 15, 2016

@author: justinpalpant

Copyright 2016 Justin Palpant

This file is part of the Jarvis Lab RNAseq Workflow program.

RNAseq Workflow is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

RNAseq Workflow is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
RNAseq Workflow. If not, see http://www.gnu.org/licenses/.
'''

import sys
import os
import readline
import re
import logging

COMMANDS = ['']
RE_SPACE = re.compile('.*\s+$', re.M)


def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def firstline(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    return lines[0]


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


class PathCompleter(object):
    """Class courtesy of samplebias from StackOverflow
    For more information see http://stackoverflow.com/a/5638688/5370002

    Modified to reduce functionality to path completion only
    """

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
               for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()

        if not buffer:
            return (self._complete_path('.') + [None])[state]

        return (self._complete_path(buffer) + [None])[state]


class ArgFiller(object):
    """An interactive method of filling in arguments not given at runtime

    """

    logger = logging.getLogger('rnaseqflow.ArgFiller')

    def __init__(self, args):
        """Store a reference to args and prepare path completion

        Arguments:
            args - any mutable object to which attributes can be added.  At
                minimum, types.SimpleNamespace or argparse.Namespace will do,
                but object() and None will not
        """

        self.args = args

        self.comp = PathCompleter()
        # we want to treat '/' as part of a word, so override the delimiters
        readline.set_completer_delims('\t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.comp.complete)

    def fill(self, args_needed):
        """Add the needed arguments to self.args if they are not there

        Asks the user for input for each of the arguments
        """

        for arg in args_needed:
            try:
                fillmethod = getattr(self, '_fill_{0}'.format(arg))
            except AttributeError:
                self.logger.error('No method to fill arg {0}'.format(arg))
                raise
            else:
                fillmethod()

    @classmethod
    def _get_integer_input(cls, message):
        """Ask the user to enter an integer in the command line"""

        while True:
            try:
                input_value = int(raw_input(message))
            except ValueError:
                cls.logger.warning(
                    "That doesn't appear to be an integer, please try again.")
                continue
            else:
                break

        return input_value

    @classmethod
    def _get_directory_input(cls, message):
        """Ask the user to enter a directory path in the command line"""

        while True:
            input_value = raw_input(message)

            if os.path.isdir(input_value):
                break
            else:
                cls.logger.warning(
                    "That doesn't appear to be an directory, please try again.")

        return input_value

    @classmethod
    def _get_filepath_input(cls, message):
        """Ask the user to enter a file path in the command line"""

        while True:
            input_value = raw_input(message)

            if os.path.isfile(input_value):
                break
            else:
                cls.logger.warning(
                    "That doesn't appear to be an file, please try again.")

        return input_value

    def _fill_root(self):
        """Fill in the --root argument with a valid root directory"""

        if not (hasattr(self.args, 'root') and
                self.args.root and
                os.path.isdir(self.args.root)):
            print 'No root directory provided with --root'
            self.args.root = self._get_directory_input(
                'Please enter a directory to use as the root folder: ')

    def _fill_ext(self):
        """Fill in the --ext argument with a file type extension"""

        if not hasattr(self.args, 'ext') or not self.args.ext:
            print 'No file extension provided with --ext'
            self.args.ext = raw_input(
                "Please provide a file extension (e.g. .fastq, .fastq.gz): ")

    def _fill_blocksize(self):
        """Fill in the --blocksize argument with a valid integer (in kB)"""

        if not (hasattr(self.args, 'blocksize') and
                isinstance(self.args.blocksize, int) and
                self.args.blocksize):
            print 'No blocksize for file copy operations given with --blocksize'

            self.args.blocksize = self._get_integer_input(
                'Please provide a blocksize in kB (e.g. 1024): ')

    def _fill_adapters(self):
        """Fill in the --adapters argument with a valid file path"""

        if not (hasattr(self.args, 'adapters') and
                self.args.adapters and
                os.path.isfile(self.args.adapters)):
            print "fasta adapter file not yet specified with --adapters"
            self.args.adapters = self._get_filepath_input(
                "Please specify the .fasta adapter file location: ")

    def _fill_fastq_args(self):
        """Fill in the arguments to be passed to fastq"""

        if not (hasattr(self.args, 'fastq_args') and self.args.fastq_args):
            print 'No fastq arguments provided to --fastq_args'

            self.args.fastq_args = raw_input(
                'Provide an optional argument string for fastq'
                ' here (e.g. "-q 30 -x 0.5"): ')

    def _fill_fastq(self):
        """Fill in the fastq-mcf executable argument with a default"""

        if not (hasattr(self.args, 'fastq') and self.args.fastq):

            self.args.fastq = 'fastq-mcf'
