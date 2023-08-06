# encoding: utf-8, division
from __future__ import print_function, division

import multiprocessing
import os

import click

from click.exceptions import BadOptionUsage

from . import helpers
from .convert import convert_batch

path_to_msconvert = helpers.guess_path_to_msconvert()
n_cores = multiprocessing.cpu_count()


@click.command()
@click.argument('input-files', nargs=-1)
@click.option('--target', type=click.Path(), help="target folder for the results")
@click.option('--extract-levels', type=int, multiple=True, default=(1, 2), show_default=True,
              help="which ms levels should appear in the final files")
@click.option('--pick-levels', type=int, multiple=True, default=(1, 2), show_default=True,
              help="which of the levels specified by --extract-levels should be centroided")
@click.option('--format', "format_", type=click.Choice(["mzML", "mzXML"]), default="mzML")
@click.option('--intensity-threshold', type=float, default=0)
@click.option("--path-to-msconvert", metavar="PATH",
              type=click.Path(exists=True, dir_okay=False), default=path_to_msconvert, show_default=True,
              help="manual setting of path to msconver.exe if automatic detection fails"
              )
@click.option("--num-workers", type=int, default=n_cores - 1, show_default=True,
              help="number of parallel workers")
@click.option("--overwrite", is_flag=True, help="overwrite result files if already present")
def main(input_files, target, extract_levels, pick_levels, format_, intensity_threshold,
         path_to_msconvert, num_workers, overwrite):
    """commandline interface to raw2mzml Python libarary.

This library wraps most common use cases of `msconvert.exe` command line tool.

`msconvert.exe` is part of Proteowizard (<http://proteowizard.sourceforge.net/>)
and allows conversion from Thermo Fisher .raw files to open source formats
.mzML and .mzXML. It has many options and getting them right is not always easy and wrong usage
results in wrong conversion results. Instead `raw2mzml` has only a configurable options which
cover common use cases.
    """
    if path_to_msconvert is None:
        raise BadOptionUsage("please specify path to msconvert")

    target = os.path.abspath(target)
    if os.path.exists(target) and not os.path.isdir(target):
        raise BadOptionUsage("the --target option must be a folder")

    print(overwrite)
    convert_batch(input_files, target, extract_levels, pick_levels, format_, intensity_threshold,
                  path_to_msconvert, num_workers, overwrite)
