# encoding: utf-8, division
from __future__ import print_function, division

import functools
import itertools
import multiprocessing
import os
import sys
import warnings
import subprocess

from exceptions import SettingsError


def cmdline_for_msconvert(path_to_msconvert, input_file, output_file, extract_levels, pick_levels,
                          intensity_threshold):

    # the order of arguments is crucial for the final result  !!!
    if pick_levels is not None:
        pp_args = ["--filter", "peakPicking true %d-%d" % pick_levels]
    else:
        pp_args = []

    target_ext = os.path.splitext(output_file)[1]

    # the order of arguments is crucial for the final result  !!!
    filter_args = ["--filter", "zeroSamples removeExtra",
                   "--filter", "msLevel %d-%d" % extract_levels]
    if intensity_threshold is not None:
        filter_args += ["--filter", "threshold absolute %s most-intense" % intensity_threshold]
    if target_ext == ".mzXML":
        output_fmt = "--mzXML"
        pp_args += ["--32"]   # 32 bit mz values
    else:
        output_fmt = "--mzML"

    cmdline = [path_to_msconvert, input_file, output_fmt, "--zlib"] + \
        pp_args + filter_args + ["--outfile", output_file]
    return cmdline


def convert_single_file(input_file, output_file, extract_levels, pick_levels, intensity_threshold,
                        path_to_msconvert=None, overwrite=False):
    """
    input_file:          path to a single .raw file
    output_file:         path to write result mzML or mzXML file, the file extension matters
    extract_levels:      tuple of integer numbers telling which ms spectra levels should appear in
                         the final file
    pick_levels   :      tuple of integer numbers which of the levels provided in 'extract_levels'
                         should be centroided. So 'pick_levels' must be a sub set of
                         'extract_levels'
    intensity_threshold: number to cut noise peaks, reduces final file size.
    path_to_msconvert:   if this is None raw2mzml tries to guess the path to msconvert.exe on the
                         local machine. If it is not found an exception will be thrown.
                         In this case you can provide the path to msconvert.exe on your machine
                         by setting this parameter.
    overwrite:           if this is True the 'output_file' will be overwritten if it already
                         exists. Else 'convert_single_file' throws an exception.
    """

    if os.path.exists(output_file) and not overwrite:
        raise ValueError("file %s exists. use --ovewrite if this is your intention" % output_file)

    target_folder = os.path.dirname(os.path.abspath(output_file))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    if path_to_msconvert is None:
        from helpers import guess_path_to_msconvert
        path_to_msconvert = guess_path_to_msconvert()
        if path_to_msconvert is None:
            raise SettingsError("could not guess path to msconvert.exe you have to "
                                "specify this argument explicitly")

    cmdline = cmdline_for_msconvert(path_to_msconvert, input_file, output_file, extract_levels,
                                    pick_levels, intensity_threshold)

    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        shell = True
    else:
        startupinfo = None
        shell = False

    proc = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            startupinfo=startupinfo, shell=shell)

    out_open = err_open = True
    while out_open or err_open:
        if out_open:
            line_out = proc.stdout.readline()
            out_open = line_out != ""
            if line_out:
                print("out: " + line_out.rstrip())
        if err_open:
            line_err = proc.stderr.readline()
            err_open = line_err != ""
            if line_err:
                print("err: " + line_err.rstrip())

    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError("calling msconvert failed !")
    return proc.returncode


def _convert_single_file(args_as_tuple, **kw):
    """multiprocessing.Pool.map passes one tuple with all args, so we need this intermediate
    step to get the arguments right"""
    return convert_single_file(*args_as_tuple, **kw)


def check(input_files, target_folder, extract_levels, pick_levels, format_, intensity_threshold,
          path_to_msconvert, num_workers, overwrite):

    if not set(pick_levels) <= set(extract_levels):
        raise ValueError("you want to pick from ms levels which you did not specify to "
                         " extract.")

    if os.path.isfile(target_folder):
        raise ValueError("target_folder %s is an exisiting file" % target_folder)

    n_cores = multiprocessing.cpu_count()
    if num_workers > n_cores:
        warnings.warn("you've chosen more workers than cpu cores, you will not benefit from this "
                      "setting. use the default setting instead.")

    if num_workers == n_cores:
        warnings.warn("you've chosen as many workers as you have cpu cores, this might freeze "
                      "your machine. it is recommended to use the default settings instead.")


def prepare(input_files, target_folder, extract_levels, pick_levels, format_, intensity_threshold,
            path_to_msconvert, num_workers, overwrite):

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)


def convert_batch(input_files, target_folder, extract_levels, pick_levels, format_,
                  intensity_threshold, path_to_msconvert, num_workers, overwrite):
    """
    input_files:         list of paths to .raw files
    target_folder:       path to folder to write final results. The names of the generated files
                         will be in sync to the file names of the input files except the file
                         extensions. if target_folder does not exist yet this function tries
                         to create it unless needed access rights are missing.
    extract_levels:      tuple of integer numbers telling which ms spectra levels should appear in
                         the final file
    pick_levels:         tuple of integer numbers which of the levels provided in 'extract_levels'
                         should be centroided. So 'pick_levels' must be a sub set of
                         'extract_levels'
    format_:             either "mzML" or "mzXML"
    intensity_threshold: number to cut noise peaks, reduces final file size.
    path_to_msconvert:   if this is None raw2mzml tries to guess the path to msconvert.exe on the
                         local machine. If it is not found an exception will be thrown.
                         In this case you can provide the path to msconvert.exe on your machine
                         by setting this parameter.
    num_workers:         number of cores to be used for parallel processing, it is recommended 
                         not use more than n - 1 workers if n is the total count of cores of your
                         machine. If you use more than one worker the output from msconvert.exe
                         on your console will look disrupted.
    overwrite:           if this is True output files will be overwritten if it already
                         exists. Else 'convert_batch' throws an exception.
    """

    check(input_files, target_folder, extract_levels, pick_levels, format_, intensity_threshold,
          path_to_msconvert, num_workers, overwrite)
    prepare(input_files, target_folder, extract_levels, pick_levels, format_, intensity_threshold,
            path_to_msconvert, num_workers, overwrite)

    file_ext = "." + format_

    output_files = []
    for input_file in input_files:
        stem = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(target_folder, stem + file_ext)
        output_files.append(output_file)

    if len(input_files) == 1:
        return convert_single_file(input_files[0], output_files[0], extract_levels, pick_levels,
                                   intensity_threshold, path_to_msconvert, overwrite)
    else:
        pool = multiprocessing.Pool(num_workers)

        target_function = functools.partial(_convert_single_file,
                                            extract_levels=extract_levels,
                                            pick_levels=pick_levels,
                                            intensity_threshold=intensity_threshold,
                                            path_to_msconvert=path_to_msconvert,
                                            overwrite=overwrite)

        args = itertools.izip(input_files, output_files)

        pool.map(target_function, args)
