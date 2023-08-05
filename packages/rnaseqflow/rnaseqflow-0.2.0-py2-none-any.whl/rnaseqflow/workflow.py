"""
Created on Dec 12, 2015

@author: justinpalpant

Copyright 2015 Justin Palpant

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
"""

import logging
import subprocess
import os
import fnmatch
import re
import shutil
from abc import ABCMeta, abstractmethod, abstractproperty

from cliutils import all_subclasses, firstline
from cliutils import ArgFiller


class Workflow(object):
    """
    Execute a simple series of steps used to preprocess RNAseq files
    """
    logger = logging.getLogger('rnaseqflow.Workflow')

    def __init__(self):
        """
        Initialize a workflow by checking for necessary shell programs
        """

        self.items = []

    def append(self, item):
        """Add a WorkflowStage to the workflow

        Arguments:
            item - a WorkflowStage to execute
        """

        self.items.append(item)

    def insert(self, idx, item):
        """Insert a WorkflowStage into the workflow

        Arguments:
            item - a WorkflowStage to execute
        """

        self.items.insert(idx, item)

    def run(self):
        """Allows the user to select a directory and processes all files within
        that directory

        This function is the primary function of the Workflow class.  All other
        functions are written as support for this function, at the moment
        """

        current_input = None
        for item in self.items:
            next_input = item.run(current_input)
            current_input = next_input


class WorkflowStage(object):
    """Interfaces for a stage of a Workflow

    Subclasses must override the run method, which takes and verifies arbitrary
    input, processes it, and returns some output
    """
    __metaclass__ = ABCMeta

    logger = logging.getLogger('rnaseqflow.WorkflowStage')

    @abstractmethod
    def run(self, stage_input):
        """Attempt to process the provided input according to the rules of the
        subclass

        Arguments:
            stage_input - an arbitrary input to be processed, usually a list of
                file names or file-like objects.  The subclass must typecheck
                the input as necessary, and define what input it takes

        Returns:
            output - the results of the processing of this workflow item
        """
        pass

    @abstractproperty
    def spec(self):
        """Abstract class property, override with @classmethod

        Used by the help method to specify available WorkflowItems
        """

        pass

    @classmethod
    def shorthelp(cls):
        helpstrings = []

        helpstrings.append('The following WorkflowStages are available:\n')

        for sub in all_subclasses(cls):
            helpstrings.append(
                '{0}: {1} - {2}\n'.format(
                    sub.spec, sub.__name__, firstline(sub.__doc__)))

        helpstrings.append('Use "--help stages" for more details\n')
        return ''.join(helpstrings)

    @classmethod
    def longhelp(cls):
        helpstrings = []

        helpstrings.append('The following WorkflowStages are available:\n')

        for sub in all_subclasses(cls):
            helpstrings.append(
                '{0}: {1}\n    {2}\n'.format(
                    sub.spec, sub.__name__, sub.__doc__))

        return ''.join(helpstrings)


class FindFiles(WorkflowStage):
    """Find files recursively in a folder

    Input:
        No input is required for this WorkflowStage
    Output:
        A flat set of file path strings
    Args used:
        --root: the folder in which to start the search
        --ext: the file extention to search for
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.FindFiles')
    spec = '1'

    def __init__(self, args):
        """Prepare the recursive file finder

        Check that a root directory is provided, or ask for one
        Make sure the search extension is valid
        """

        argfiller = ArgFiller(args)
        argfiller.fill(['root', 'ext'])

        self.root = args.root
        self.ext = args.ext

    def run(self, stage_input):
        """Run the recursive file finding stage

        Arguments:
            stage_input - not used, only for the interface

        Returns:
            A flat list of files found with the correct extension
        """

        self.logger.info('Beginning file find operations')

        outfiles = set()
        for root, _, files in os.walk(self.root):
            for basename in files:
                if fnmatch.fnmatch(basename, "*" + self.ext):
                    filename = os.path.join(root, basename)
                    outfiles.add(filename)

        self.logger.info('Found {0} files'.format(len(outfiles)))

        return outfiles


class MergeSplitFiles(WorkflowStage):
    """Merge files by the identifying sequence and direction

    Input:
        An iterable of file names to be grouped and merged
    Output:
        A flat set of merged filenames
    Args used:
        --root: the folder where merged files will be placed
        --ext: the file extention to be used for the output files
        --blocksize: number of kilobytes to use as a copy block size
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.MergeSplitFiles')
    spec = '2'

    def __init__(self, args):
        """Prepare for the merge file stage

        Check for a root directory and a blocksize
        """

        argfiller = ArgFiller(args)
        argfiller.fill(['root', 'ext', 'blocksize'])

        self.root = args.root
        self.blocksize = args.blocksize
        self.ext = args.ext

        self.outdir = os.path.join(self.root, 'merged')
        try:
            os.makedirs(self.outdir)
        except OSError:
            if not os.path.isdir(self.outdir):
                self.logger.error(
                    'Cannot make directory {0}, '
                    'permissions'.format(self.outdir))
                raise

    def run(self, stage_input):
        """Run the merge files operation

        Arguments:
            stage_input - a list of files to be organized and merged

        Returns:
            A flat list of merged files
        """
        self.logger.info('Beginning file merge operations')

        organized = self._organize_files(stage_input)

        merged_files = set()

        for i, (fileid, files) in enumerate(organized.iteritems()):
            outfile_name = 'merged_' + \
                fileid[0] + '_' + fileid[1] + self.ext
            outfile_path = os.path.join(self.outdir, outfile_name)

            self.logger.info(
                'Building file {0:d} of {1:d}: {2}'.format(
                    i + 1, len(organized), outfile_path))

            with open(outfile_path, 'wb') as outfile:
                for j, infile in enumerate(files):
                    if j + 1 != self._get_part_num(infile):
                        self.logger.error(
                            'Part {0:03d} not found, terminating construction'
                            ' of {1}'.format(j, outfile_path))
                        break

                    self.logger.debug(
                        'Merging file %d of %d: %s', j, len(files),
                        infile)

                    shutil.copyfileobj(
                        open(infile, 'rb'), outfile, 1024 * self.blocksize)

            merged_files.add(outfile_path)

        self.logger.info('Created {0} merged files'.format(len(merged_files)))

        return merged_files

    def _organize_files(self, files):
        """Organizes a list of paths by sequence_id, part number, and direction

        Arguments:
            files - a flat list of RNAseq file names

        Returns:
           A dictionary - (sequence_id, dir):list(paths in ascending order)
        """

        mapping = {}

        for path in files:
            sequence_id = self._get_sequence_id(os.path.basename(path))
            direction = self._get_direction_id(os.path.basename(path))

            if not (sequence_id and direction):
                self.logger.warning('Discarding file {0} - could not find '
                                    'sequence ID and direction using '
                                    'regular expressions'.format(
                                        os.path.basename(path)))
                continue

            try:
                mapping[(sequence_id, direction)].append(path)
            except KeyError:
                mapping[(sequence_id, direction)] = [path]

        for key, lst in mapping.iteritems():
            mapping[key] = sorted(lst, key=self._get_part_num)

        return mapping

    @staticmethod
    def _get_sequence_id(filename):
        """Gets the six-letter RNA sequence that identifies the RNAseq file

        Returns a six character string that is the ID, or an empty string if no
        identifying sequence is found."""

        p = re.compile('.*[ACTG]{6}')

        m = p.search(filename)
        if m is None:
            return ''
        else:
            return m.group()

    @staticmethod
    def _get_direction_id(filename):
        """Gets the direction identifier from an RNAseq filename

        A direction identifier is either R01 or R02, indicating a forward or a
        backwards read, respectively.
        """

        p = re.compile('R\d{1}')

        m = p.search(filename)
        if m is None:
            return ''
        else:
            return m.group()

    @staticmethod
    def _get_part_num(filename):
        """Returns an integer indicating the file part number of the selected
        RNAseq file

        RNAseq files, due to their size, are split into many smaller files,
        each of which is given a three digit file part number (e.g. 001, 010).
        This method returns that part number as an integer.

        This requires that there only be one sequence of three digits in the
        filename
        """

        p = re.compile('_\d{3}')

        m = p.search(filename)
        if m is None:
            return 0
        else:
            text = m.group()
            return int(text[1:])


class FastQMCFTrimSolo(WorkflowStage):
    """Trim adapter sequences from files using fastq-mcf one file at a time

    Input:
        A flat set of files to be passed into fastq-mcf file-by-file
    Output:
        A flat set of trimmed file names
    Args used:
        --root: the folder where trimmed files will be placed
        --adapters: the filepath of the fasta adapters file
        --fastq: the location of the fastq-mcf executable
        --fastq_args: a string of arguments to pass directly to fastq-mcf
    """

    logger = logging.getLogger('rnaseqflow.WorkflowStage.FastQMCFTrimSolo')
    spec = '3'

    def __init__(self, args):
        """Run all checks needed to create a FastQMCFTrimItem

        Check that fastq-mcf exists in the system
        Specify the fasta adapter file and any arguments
        """
        argfiller = ArgFiller(args)
        argfiller.fill(['root', 'adapters', 'fastq', 'fastq_args'])

        self.root = args.root
        self.adapters = args.adapters
        self.fastq_args = args.fastq_args
        self.executable = args.fastq

        self.outdir = os.path.join(self.root, 'trimmed')
        try:
            os.makedirs(self.outdir)
        except OSError:
            if not os.path.isdir(self.outdir):
                raise

        try:
            with open(os.devnull, "w") as fnull:
                subprocess.call([self.executable], stdout=fnull, stderr=fnull)
        except OSError:
            self.logger.error(
                'fastq-mcf not found, cannot use FastQMCFTrimSolo')
            raise
        else:
            self.logger.info('fastq-mcf found')

    def run(self, stage_input):
        """Trim files one at a time using fastq-mcf

        Arguments:
            stage_input - a flat list of file names

        Returns:
            A flat list of trimmed file names
        """

        self.logger.info('Beginning file trim operation')
        trimmed_files = set()

        for i, fname in enumerate(stage_input):
            outfile_name = 'trimmed_' + os.path.basename(fname)
            outfile_path = os.path.join(self.outdir, outfile_name)
            cmd = [self.executable, self.adapters, fname] + \
                self.fastq_args.split() + ['-o', outfile_path]

            self.logger.info(
                'Building file {0:d} of {1:d}: {2}'.format(
                    i + 1, len(stage_input), outfile_path))

            self.logger.debug('Calling %s', str(cmd))

            subprocess.call(cmd)

            trimmed_files.add(outfile_path)

        self.logger.info('Trimmed {0} files'.format(len(trimmed_files)))

        return trimmed_files
