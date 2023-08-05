'''
Created on Dec 13, 2015

@author: justinpalpant

This file is part of the Jarvis Lab RNAseq Workflow program.

RNAseq Workflow is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

RNAseq Workflow is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
RNAseq Workflow. If not, see http://www.gnu.org/licenses/.
'''
from workflow import Workflow, WorkflowStage
from cliutils import all_subclasses

import logging
import argparse


def opts():
    parser = argparse.ArgumentParser(
        description='Preprocess RNAseq files.',
        add_help=False, prog='rnaseqflow')

    parser.add_argument(
        '--help', choices=('all', 'stages'),
        nargs='?', const='all',
        help='display help for part of the program and exit')

    parser.add_argument(
        '--logging',
        choices=('debug', 'info', 'warning',
                 'error', 'critical'),
        default='info', help='Logging level (default: %(default)s)')

    parser.add_argument(
        '--version',
        action='version', version='%(prog)s 0.2.0')

    parser.add_argument(
        '--stages', nargs='*',
        help='Add stages')

    parser.add_argument(
        '--root',
        help='The root directory to be searched for RNAseq files')
    parser.add_argument(
        '--ext',
        help='The file extension to search for')

    parser.add_argument(
        '--blocksize',
        type=int,
        help='The size of the copy block (in kB) for merge operations')

    parser.add_argument(
        '--adapters',
        help='FastA adapters file to use')

    parser.add_argument(
        '--fastq',
        help='Location of the fastq-mcf executable',
        default='fastq-mcf')

    parser.add_argument(
        '--fastq_args',
        help='Specify arguments to be passed to fastq-mcf')

    return parser


def main():
    """This method is called when you use python -m {package}

    It requires that all the important packages be
    available in the Python path, correctly installed.
    """

    args = opts().parse_args()

    if args.help == 'all':
        opts().print_help()
        return
    elif args.help == 'stages':
        print WorkflowStage.longhelp()
        return

    logging.basicConfig(
        level=getattr(logging, args.logging.upper()),
        format='%(asctime)s in %(name)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    w = Workflow()

    if not args.stages:
        print 'Stages not given with --stages argument'
        print WorkflowStage.shorthelp()
        stages = raw_input(
            'Enter space separated stage specifiers (e.g. "1A 2 3"): ').split()
    else:
        stages = args.stages

    classmap = {cls.spec: cls for cls in all_subclasses(WorkflowStage)}

    for stage_spec in stages:
        try:
            w.append(classmap[stage_spec](args))
        except KeyError as e:
            logging.error(
                'No valid stage specifier {0} - use "--help stages" to see '
                'stage specifiers for this software'.format(stage_spec))
            raise

    w.run()

if __name__ == '__main__':
    main()
