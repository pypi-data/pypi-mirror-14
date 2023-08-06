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
import logging
import glob


def trim(docstring):
    """Trim a :pep:`0257` docstring

    Code taken directly from :pep:`0257#handling-docstring-indentation`

    :param docstring: a Python docstring
    :type docstring: str

    :returns: the first line of the docstring
    :rtype: str
    """

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
    """Extract and return only the first line of a :pep:`0257` docstring

    :param docstring: a Python docstring
    :type docstring: str

    :returns: the first line of the docstring
    :rtype: str
    """

    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    return lines[0]


def all_subclasses(cls):
    """Recursively generate all subclasses of cls

    :param cls: a python class

    :returns: all subclasses of cls
    :rtype: list(cls)
    """
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


class ArgFiller(object):
    """An interactive method of filling in arguments not given at runtime

    Code completion taken from https://gist.github.com/iamatypeofwalrus/5637895
    """

    logger = logging.getLogger('rnaseqflow.ArgFiller')

    def __init__(self, args):
        """Store a reference to args and prepare path completion

        :param args: any mutable object to which attributes can be added.  At
                minimum, types.SimpleNamespace or argparse.Namespace will do,
                but object() and None will not
        """

        self.args = args

    def set_path_complete(self, enable):
        """Enable or disable readline pathcompletion

        :param enable: enable or disable completion
        :type enable: bool
        """
        if enable:
            readline.set_completer_delims('\t')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.pathCompleter)
        else:
            readline.set_completer(None)

    def pathCompleter(self, text, state):
        """This is the tab completer for systems paths."""
        line = readline.get_line_buffer().split()

        return [x for x in glob.glob(text + '*')][state]

    def fill(self, args_needed):
        """Add the needed arguments to self.args if they are not there

        Asks the user for input for each of the missing arguments

        :param args_needed: a list of attributes to ensure self.args contains
        :type args_needed: list(str)
        """

        for arg in args_needed:
            self.set_path_complete(True)

            try:
                fillmethod = getattr(self, '_fill_{0}'.format(arg))
            except AttributeError:
                self.logger.error('No method to fill arg {0}'.format(arg))
                raise
            else:
                fillmethod()

            self.set_path_complete(False)

    @classmethod
    def _get_integer_input(cls, message):
        """Ask the user to enter an integer in the command line

        :param message: a message to display with raw_input
        :type message: str
        """

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
        """Ask the user to enter a directory path in the command line

        :param message: a message to display with raw_input
        :type message: str
        """

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
        """Ask the user to enter a file path in the command line

        :param message: a message to display with raw_input
        :type message: str
        """

        while True:
            input_value = raw_input(message)

            if os.path.isfile(input_value):
                break
            else:
                cls.logger.warning(
                    "That doesn't appear to be an file, please try again.")

        return input_value

    def _fill_root(self):
        """Fill in self.args.root with a valid root directory"""

        if not (hasattr(self.args, 'root') and
                self.args.root and
                os.path.isdir(self.args.root)):
            print 'No root directory provided with --root'
            self.args.root = self._get_directory_input(
                'Please enter a directory to use as the root folder: ')

    def _fill_ext(self):
        """Fill in self.args.ext with a file type extension"""

        if not hasattr(self.args, 'ext') or not self.args.ext:
            print 'No file extension provided with --ext'
            self.args.ext = raw_input(
                "Please provide a file extension (e.g. .fastq, .fastq.gz): ")

    def _fill_blocksize(self):
        """Fill in self.args.blocksize with a valid integer (in kB)"""

        if not (hasattr(self.args, 'blocksize') and
                isinstance(self.args.blocksize, int) and
                self.args.blocksize):
            print 'No blocksize for file copy operations given with --blocksize'

            self.args.blocksize = self._get_integer_input(
                'Please provide a blocksize in kB (e.g. 1024): ')

    def _fill_adapters(self):
        """Fill in self.args.adapters with a valid file path"""

        if not (hasattr(self.args, 'adapters') and
                self.args.adapters and
                os.path.isfile(self.args.adapters)):
            print "fasta adapter file not yet specified with --adapters"
            self.args.adapters = self._get_filepath_input(
                "Please specify the .fasta adapter file location: ")

    def _fill_fastq_args(self):
        """Fill in self.args.fastq_args"""

        if not (hasattr(self.args, 'fastq_args') and self.args.fastq_args):
            print 'No fastq arguments provided to --fastq_args'

            self.args.fastq_args = raw_input(
                'Provide an optional argument string for fastq'
                ' here (e.g. "-q 30 -x 0.5"): ')

    def _fill_fastq(self):
        """Fill in the fastq-mcf executable self.args.fastq with a default 'fastq-mcf'"""

        if not (hasattr(self.args, 'fastq') and self.args.fastq):
            self.args.fastq = 'fastq-mcf'

    def _fill_quiet(self):
        """Fill in the quiet argument self.args.quiet with default False"""

        if not (hasattr(self.args, 'quiet') and self.args.quiet):
            self.args.quiet = False
