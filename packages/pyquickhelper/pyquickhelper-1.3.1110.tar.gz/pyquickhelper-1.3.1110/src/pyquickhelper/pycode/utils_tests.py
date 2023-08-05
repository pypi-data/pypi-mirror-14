"""
@file
@brief  This extension contains various functionalities to help unittesting.

.. versionchanged:: 1.1
    Moved to folder ``pycode``.
"""
from __future__ import print_function

import os
import stat
import sys
import glob
import re
import unittest
import io
import warnings
import time

from ..filehelper.synchelper import remove_folder
from ..loghelper.flog import run_cmd, noLOG
from .call_setup_hook import call_setup_hook
from .code_exceptions import CoverageException, SetupHookException
from .coverage_helper import publish_coverage_on_codecov


__all__ = ["get_temp_folder", "main_wrapper_tests"]


def get_temp_folder(thisfile, name, clean=True, create=True):
    """
    return a local temporary folder to store files when unit testing

    @param      thisfile        use ``__file__``
    @param      name            name of the temporary folder
    @param      clean           if True, clean the folder first
    @param      create          if True, creates it (empty if clean is True)
    @return                     temporary folder

    .. versionadded:: 0.9
    """
    if not name.startswith("temp_"):
        raise NameError("the folder {0} must begin with temp_".format(name))

    local = os.path.join(
        os.path.normpath(os.path.abspath(os.path.dirname(thisfile))), name)
    if name == local:
        raise NameError(
            "the folder {0} must be relative, not absolute".format(name))

    if not os.path.exists(local):
        if create:
            os.mkdir(local)
            mode = os.stat(local).st_mode
            nmode = mode | stat.S_IWRITE
            if nmode != mode:
                os.chmod(local, nmode)
    else:
        if clean:
            remove_folder(local)
            time.sleep(0.1)
        if create and not os.path.exists(local):
            os.mkdir(local)
            mode = os.stat(local).st_mode
            nmode = mode | stat.S_IWRITE
            if nmode != mode:
                os.chmod(local, nmode)

    return local


def get_test_file(filter, dir=None, no_subfolder=False, fLOG=noLOG, root=None):
    """
    return the list of test files
    @param      dir             path to look (or paths to look if it is a list)
    @param      filter          only select files matching the pattern (ex: test*)
    @param      no_subfolder    the function investigates the folder *dir* and does not try any subfolder in
                                ``{"_nrt", "_unittest", "_unittests"}``
    @param      fLOG            logging function
    @param      root            root or folder which contains the project,
                                rules applyong on folder name will not apply on it
    @return                     a list of test files

    .. versionchanged:: 1.1
        Parameter *no_subfolder* was added.

    .. versionchanged:: 1.3
        Paramerer *fLOG*, *root* were added.
    """
    if no_subfolder:
        dirs = [dir]
    else:
        expected = {"_nrt", "_unittest", "_unittests"}
        if dir is None:
            path = os.path.split(__file__)[0]
            dirs = [os.path.join(path, "..", "..", d) for d in expected]
        elif isinstance(dir, str  # unicode#
                        ):
            if not os.path.exists(dir):
                raise FileNotFoundError(dir)
            last = os.path.split(dir)[-1]
            if last in expected:
                dirs = [dir]
            else:
                dirs = [os.path.join(dir, d) for d in expected]
        else:
            dirs = dir
            for d in dirs:
                if not os.path.exists(d):
                    raise FileNotFoundError(d)

    copypaths = list(sys.path)
    fLOG("[unittests], inspecting", dirs)

    li = []
    for dir in dirs:
        if "__pycache__" in dir or "site-packages" in dir:
            continue
        if not os.path.exists(dir):
            continue
        if dir not in sys.path and dir != ".":
            sys.path.append(dir)
        content = glob.glob(dir + "/" + filter)
        if filter != "temp_*":
            if root is not None:
                def remove_root(p):
                    if p.startswith(root):
                        return p[len(root):]
                    else:
                        return p
                content = [(remove_root(l), l) for l in content]
            else:
                content = [(l, l) for l in content]

            content = [fu for l, fu in content if "test_" in l and
                       ".py" in l and
                       "test_main" not in l and
                       "temp_" not in l and
                       "out.test_copyfile.py.2.txt" not in l and
                       ".pyc" not in l and
                       ".pyd" not in l and
                       ".so" not in l and
                       ".py~" not in l and
                       ".pyo" not in l]
        li.extend(content)

        lid = glob.glob(dir + "/*")
        for l in lid:
            if os.path.isdir(l):
                temp = get_test_file(
                    filter, l, no_subfolder=True, fLOG=fLOG, root=root)
                temp = [t for t in temp]
                li.extend(temp)

    # we restore sys.path
    sys.path = copypaths

    return li


def get_estimation_time(file):
    """
    return an estimation of the processing time, it extracts the number in ``(time=5s)`` for example

    @param      file        filename
    @return                 int
    """
    try:
        f = open(file, "r")
        li = f.readlines()
        f.close()
    except UnicodeDecodeError:
        try:
            f = open(file, "r", encoding="latin-1")
            li = f.readlines()
            f.close()
        except Exception as ee:
            raise Exception("issue with %s\n%s" % (file, str(ee)))

    s = ''.join(li)
    c = re.compile("[(]time=([0-9]+)s[)]").search(s)
    if c is None:
        return 0
    else:
        return int(c.groups()[0])


def import_files(li, additional_ut_path=None, fLOG=noLOG):
    """
    run all tests in file list li

    @param      li                      list of files (python scripts)
    @param      additional_ut_path      additional paths to add when running the unit tests
    @param      fLOG                    logging function
    @return                             list of tests [ ( testsuite, file) ]

    .. versionchanged:: 1.3
        Parameters *fLOG*, *additional_ut_path* were added.
    """
    allsuite = []
    for l in li:

        copypath = list(sys.path)

        sdir = os.path.split(l)[0]
        if sdir not in sys.path:
            sys.path.append(sdir)
        if additional_ut_path:
            for p in additional_ut_path:
                if isinstance(p, tuple):
                    if p[1]:
                        sys.path.insert(0, p[0])
                    else:
                        sys.path.append(p[0])
                else:
                    sys.path.append(p)
        tl = os.path.split(l)[1]
        fi = tl.replace(".py", "")

        try:
            mo = __import__(fi)
        except:
            fLOG("problem with ", fi)
            fLOG("additional paths")
            for p in sys.path:
                fLOG("   ", p)
            mo = __import__(fi)

        # some tests can mess up with the import path
        sys.path = copypath

        cl = dir(mo)
        for c in cl:
            if len(c) < 5 or c[:4] != "Test":
                continue
            # test class c
            testsuite = unittest.TestSuite()
            loc = locals()
            exec(
                compile("di = dir (mo." + c + ")", "", "exec"), globals(), loc)
            di = loc["di"]
            for d in di:
                if len(d) >= 6 and d[:5] == "_test":
                    raise RuntimeError(
                        "a function _test is still deactivated %s in %s" % (d, c))
                if len(d) < 5 or d[:4] != "test":
                    continue
                # method d.c
                loc = locals()
                exec(
                    compile("t = mo." + c + "(\"" + d + "\")", "", "exec"), globals(), loc)
                t = loc["t"]
                testsuite.addTest(t)

            allsuite.append((testsuite, l))

    return allsuite


def clean(dir=None, fLOG=noLOG):
    """
    do the cleaning

    @param      dir     directory
    @param      fLOG    logging function
    """
    # do not use SVN here just in case some files are not checked in.
    for log_file in ["temp_hal_log.txt", "temp_hal_log2.txt",
                     "temp_hal_log_.txt", "temp_log.txt", "temp_log2.txt", ]:
        li = get_test_file(log_file, dir=dir)
        for l in li:
            try:
                if os.path.isfile(l):
                    os.remove(l)
            except Exception as e:
                fLOG(
                    "unable to remove file", l, " --- ", str(e).replace("\n", " "))

    li = get_test_file("temp_*")
    for l in li:
        try:
            if os.path.isfile(l):
                os.remove(l)
        except Exception as e:
            fLOG("unable to remove file. ", l,
                 " --- ", str(e).replace("\n", " "))
    for l in li:
        try:
            if os.path.isdir(l):
                remove_folder(l)
        except Exception as e:
            fLOG("unable to remove dir. ", l,
                 " --- ", str(e).replace("\n", " "))


def main(runner,
         path_test=None,
         limit_max=1e9,
         log=False,
         skip=-1,
         skip_list=None,
         on_stderr=False,
         flogp=noLOG,
         processes=False,
         skip_function=None,
         additional_ut_path=None,
         stdout=None,
         stderr=None,
         fLOG=noLOG):
    """
    run all unit test
    the function looks into the folder _unittest and extract from all files
    beginning by `test_` all methods starting by `test_`.
    Each files should mention an execution time.
    Tests are sorted by increasing order.

    @param      runner              unittest Runner
    @param      path_test           path to look, if None, looks for defaults path related to this project
    @param      limit_max           avoid running tests longer than limit seconds
    @param      log                 if True, enables intermediate files
    @param      skip                if skip != -1, skip the first "skip" test files
    @param      skip_list           skip unit test id in this list (by index, starting by 1)
    @param      skip_function       function(filename,content) --> boolean to skip a unit test
    @param      on_stderr           if True, publish everything on stderr at the end
    @param      flogp               logging, printing function
    @param      processes           to run the unit test in a separate process (with function @see fn run_cmd),
                                    however, to make that happen, you need to specify
                                    ``exit=False`` for each test file, see `unittest.main <https://docs.python.org/3.4/library/unittest.html#unittest.main>`_
    @param      additional_ut_path  additional paths to add when running the unit tests
    @param      stdout              if not None, use this stream instead of *sys.stdout*
    @param      stderr              if not None, use this stream instead of *sys.stderr*
    @param      fLOG                logging function
    @return                         dictionnary: ``{ "err": err, "tests":list of couple (file, test results) }``

    .. versionchanged:: 0.9
        change the result type into a dictionary, catches warning when running unit tests,
        add parameter *processes* to run the unit test in a different process through command line

    .. versionchanged:: 1.0
        parameter *skip_function* was added

    .. versionchanged:: 1.3
        Parameters *fLOG*, *stdout*, *stderr* were added.
    """
    if skip_list is None:
        skip_list = set()
    else:
        skip_list = set(skip_list)

    # checking that the module does not belong to the installed modules
    if path_test is not None:
        path_module = os.path.join(sys.executable, "Lib", "site-packages")
        paths = [os.path.join(path_module, "src"), ]
        for path in paths:
            if os.path.exists(path):
                raise FileExistsError("this path should not exist " + path)

    def short_name(l):
        cut = os.path.split(l)
        cut = os.path.split(cut[0])[-1] + "/" + cut[-1]
        return cut

    # sort the test by increasing expected time
    fLOG("path_test", path_test)
    li = get_test_file("test*", dir=path_test, fLOG=fLOG, root=path_test)
    if len(li) == 0:
        raise FileNotFoundError("no test files in " + path_test)
    est = [get_estimation_time(l) for l in li]
    co = [(e, short_name(l), l) for e, l in zip(est, li)]
    co.sort()

    # we check we do not run twice the same file
    done = {}
    duplicate = []
    for a, cut, l in co:
        if cut in done:
            duplicate.append((cut, l))
        done[cut] = True

    if len(duplicate) > 0:
        s = list(set(duplicate))
        s.sort()
        mes = "\n".join(s)
        raise Exception("duplicated test file were detected:\n" + mes)

    # check existing
    if len(co) == 0:
        raise FileNotFoundError(
            "unable to find any test files in {0}".format(path_test))

    if skip != -1:
        flogp("found ", len(co), " test files skipping", skip)
    else:
        flogp("found ", len(co), " test files")

    # extract the test classes
    cco = []
    duration = {}
    index = 0
    for e, cut, l in co:
        if e > limit_max:
            continue
        cco.append((e, l))
        cut = os.path.split(l)
        cut = os.path.split(cut[0])[-1] + "/" + cut[-1]
        duration[cut] = e
        index += 1

    exp = re.compile("Ran ([0-9]+) tests? in ([.0-9]+)s")

    # run the test
    li = [a[1] for a in cco]
    lis = [os.path.split(_)[-1] for _ in li]
    suite = import_files(li, additional_ut_path=additional_ut_path, fLOG=fLOG)
    keep = []

    # redirect standard output, error
    memo_stdout = sys.stdout
    memout = sys.stdout if stdout is None else stdout
    fail = 0
    allwarn = []

    memo_stderr = sys.stderr
    memerr = sys.stderr if stderr is None else stderr
    fullstderr = io.StringIO()

    # displays
    memout.write("---- BEGIN UNIT TEST for {0}\n".format(path_test))

    # display all tests
    for i, s in enumerate(suite):
        if skip >= 0 and i < skip:
            continue
        if i + 1 in skip_list:
            continue
        if skip_function is not None:
            with open(s[1], "r") as f:
                content = f.read()
            if skip_function(s[1], content):
                continue

        cut = os.path.split(s[1])
        cut = os.path.split(cut[0])[-1] + "/" + cut[-1]
        if cut not in duration:
            raise Exception("{0} not found in\n{1}".format(
                cut, "\n".join(sorted(duration.keys()))))
        else:
            dur = duration[cut]
        zzz = "\ntest % 3d (%04ds), %s" % (i + 1, dur, cut)
        memout.write(zzz)
    memout.write("\n")

    # displays
    memout.write("---- RUN UT\n")

    # run all tests
    for i, s in enumerate(suite):
        if skip >= 0 and i < skip:
            continue
        if i + 1 in skip_list:
            continue
        if skip_function is not None:
            with open(s[1], "r") as f:
                content = f.read()
            if skip_function(s[1], content):
                continue

        cut = os.path.split(s[1])
        cut = os.path.split(cut[0])[-1] + "/" + cut[-1]
        zzz = "running test % 3d, %s" % (i + 1, cut)
        zzz += (60 - len(zzz)) * " "
        memout.write(zzz)

        if log and fLOG is not print:
            fLOG(OutputPrint=True)
            fLOG(Lock=True)

        newstdr = io.StringIO()
        keepstdr = sys.stderr
        sys.stderr = newstdr
        list_warn = []

        if processes:
            cmd = sys.executable.replace("w.exe", ".exe") + " " + li[i]
            out, err = run_cmd(cmd, wait=True)
            if len(err) > 0:
                sys.stderr.write(err)
        else:
            if sys.version_info[0] >= 3:
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    r = runner.run(s[0])
                    for ww in w:
                        list_warn.append(ww)
                    warnings.resetwarnings()

                out = r.stream.getvalue()
            else:
                fLOG("running")
                r = runner.run(s[0])
                out = r.stream.getvalue()
                fLOG("end running")

        ti = exp.findall(out)[-1]
        # don't modify it, PyCharm does not get it right (ti is a tuple)
        add = " ran %s tests in %ss" % ti

        sys.stderr = keepstdr

        if log:
            fLOG(Lock=False)

        memout.write(add)

        if not r.wasSuccessful():
            err = out.split("===========")
            err = err[-1]
            memout.write("\n")
            try:
                memout.write(err)
            except UnicodeDecodeError:
                err_e = err.decode("ascii", errors="ignore")
                memout.write(err_e)
            except UnicodeEncodeError:
                try:
                    err_e = err.encode("ascii", errors="ignore")
                    memout.write(err_e)
                except TypeError:
                    err_e = err.encode("ascii", errors="ignore").decode(
                        'ascii', errors='ingore')
                    memout.write(err_e)

            fail += 1

            fullstderr.write("\n#-----" + lis[i] + "\n")
            fullstderr.write("OUT:\n")
            fullstderr.write(out)

            if err:
                fullstderr.write("ERRo:\n")
                try:
                    fullstderr.write(err)
                except UnicodeDecodeError:
                    err_e = err.decode("ascii", errors="ignore")
                    fullstderr.write(err_e)
                except UnicodeEncodeError:
                    err_e = err.encode("ascii", errors="ignore")
                    fullstderr.write(err_e)

            if len(list_warn) > 0:
                fullstderr.write("WARN:\n")
                for w in list_warn:
                    fullstderr.write("w{0}: {1}\n".format(i, str(w)))
            serr = newstdr.getvalue()
            if serr.strip(" \n\r\t"):
                fullstderr.write("ERRs:\n")
                fullstderr.write(serr)
        else:
            allwarn.append((lis[i], list_warn))
            val = newstdr.getvalue()
            if len(val) > 0 and is_valid_error(val):
                fullstderr.write("\n*-----" + lis[i] + "\n")
                if len(list_warn) > 0:
                    fullstderr.write("WARN:\n")
                    for w in list_warn:
                        fullstderr.write("w{0}: {1}\n".format(i, str(w)))
                if val.strip(" \n\r\t"):
                    fullstderr.write("ERRv:\n")
                    fullstderr.write(val)

        memout.write("\n")

        keep.append((s[1], r))

    # displays
    memout.write("---- END UT\n")

    # end, catch standard output and err
    sys.stderr = memo_stderr
    sys.stdout = memo_stdout
    val = fullstderr.getvalue()

    if len(val) > 0:
        flogp("-- STDERR (from unittests) on STDOUT")
        flogp(val)
        flogp("-- end STDERR on STDOUT")

        if on_stderr:
            memerr.write("##### STDERR (from unittests) #####\n")
            memerr.write(val)
            memerr.write("##### end STDERR #####\n")

    if fail == 0:
        clean()

    for fi, lw in allwarn:
        if len(lw) > 0:
            memout.write("WARN: {0}\n".format(fi))
            for i, w in enumerate(lw):
                try:
                    sw = "  w{0}: {1}\n".format(i, w)
                except UnicodeEncodeError:
                    sw = "  w{0}: Unable to convert a warnings of type {0} into a string (1)".format(
                        i, type(w))
                try:
                    memout.write(sw)
                except UnicodeEncodeError:
                    sw = "  w{0}: Unable to convert a warnings of type {0} into a string (2)".format(
                        i, type(w))
                    memout.write(sw)

    flogp("END of unit tests")

    return dict(err=val, tests=keep)


def is_valid_error(error):
    """
    checks if the text written on stderr is an error or not,
    a local server can push logs on this stream,

    it looks for keywords such as Exception, Error, TraceBack...

    @param      error       text
    @return                 boolean
    """
    keys = ["Exception", "Error", "TraceBack", "invalid", " line "]
    error = error.lower()
    for key in keys:
        if key.lower() in error:
            return True
    return False


def default_skip_function(name, code):
    """
    default skip function for function @see fn main_wrapper_tests.

    @param      name        name of the test file
    @param      code        code of the test file
    @return                 True if skipped, False otherwise
    """
    if "test_SKIP_" in name or "test_LONG_" in name:
        return True
    return False


def main_wrapper_tests(codefile,
                       skip_list=None,
                       processes=False,
                       add_coverage=False,
                       report_folder=None,
                       skip_function=default_skip_function,
                       setup_params=None,
                       only_setup_hook=False,
                       coverage_options=None,
                       coverage_exclude_lines=None,
                       additional_ut_path=None,
                       covtoken=None,
                       hook_print=True,
                       stdout=None,
                       stderr=None,
                       fLOG=noLOG):
    """
    calls function :func:`main <pyquickhelper.unittests.utils_tests.main>` and throw an exception if it fails

    @param      codefile                ``__file__`` or ``run_unittests.py``
    @param      skip_list               to skip a list of unit tests (by index, starting by 1)
    @param      processes               to run the unit test in a separate process (with function @see fn run_cmd),
                                        however, to make that happen, you need to specify
                                        ``exit=False`` for each test file, see `unittest.main <https://docs.python.org/3.4/library/unittest.html#unittest.main>`_
    @param      add_coverage            run the unit tests and measure the coverage at the same time
    @param      report_folder           folder where the coverage report will be stored, if None, it will be placed in:
                                        ``os.path.join(os.path.dirname(codefile), "..", "_doc","sphinxdoc","source", "coverage")``
    @param      skip_function           function(filename,content) --> boolean to skip a unit test
    @param      setup_params            parameters sent to @see fn call_setup_hook
    @param      only_setup_hook         calls only @see fn call_setup_hook, do not run the unit test
    @param      coverage_options        (dictionary) options for module coverage as a dictionary, see below, default is None
    @param      coverage_exclude_lines  (list) options for module coverage, lines to exclude from the coverage report, defaul is None
    @param      additional_ut_path      (list) additional paths to add when running the unit tests
    @param      covtoken                (str) token used when publishing coverage report to `codecov <https://codecov.io/>`_
                                        or None to not publish
    @param      hook_print              enable print display when calling *_setup_hook*
    @param      stdout                  if not None, write output on this stream instead of *sys.stdout*
    @param      stderr                  if not None, write errors on this stream instead of *sys.stderr*
    @param      fLOG                    function(*l, **p), logging function

    *covtoken* can be a string ``<token>`` or a
    tuple ``(<token>, <condition>)``. The condition is evaluated
    by the python interpreter and determines whether or not the coverage
    needs to be published.

    @FAQ(How to build pyquickhelper with Jenkins?)
    `Jenkins <http://jenkins-ci.org/>`_ is a task scheduler for continuous integration.
    You can easily schedule batch command to build and run unit tests for a specific project.
    To build pyquickhelper, you need to install `python <https://www.python.org/>`_,
    `pymyinstall <http://www.xavierdupre.fr/app/pymyinstall/helpsphinx/>`_,
    `miktex <http://miktex.org/>`_,
    `pandoc <http://johnmacfarlane.net/pandoc/>`_,
    `sphinx <http://sphinx-doc.org/>`_.

    Once Jenkins is installed, the command to schedule is::

        set PATH=%PATH%;%USERPOFILE%\AppData\Local\Pandoc
        build_setup_help_on_windows.bat

    This works if you installed Jenkins with your credentials.
    Otherwise the path to ``pandoc.exe`` needs to be changed.

    And you can also read `Schedule builds with Jenkins <http://www.xavierdupre.fr/blog/2014-12-06_nojs.html>`_.
    @endFAQ

    .. versionchanged:: 0.9
        Parameters *add_coverage* and *report_folder* were added to compute the coverage
        using the module `coverage <http://nedbatchelder.com/code/coverage/>`_.

    .. versionchanged:: 1.0
        Does something to avoid getting the following error::

            _tkinter.TclError: no display name and no $DISPLAY environment variable

        It is due to matplotlib. See `Generating matplotlib graphs without a running X server <http://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server>`_.

    .. versionchanged:: 1.1
        If the skip function is None, it will replace it by the function @see fn default_skip_function.
        Calls function @see fn _setup_hook if it is available in the unit tested module.
        Parameter *tested_module* was added, the function then checks the presence of
        function @see fn _setup_hook, it is the case, it runs it.

        Parameter *setup_params* was added. A mechanism was put in place
        to let the module to test a possibility to run some preprocessing steps
        in a separate process. They are described in @see fn _setup_hook
        which must be found in the main file ``__init__.py``.

    .. versionchanged:: 1.2
        Parameter *only_setup_hook* was added.
        Save the report in XML format, binary format, replace full paths by relative path.

    .. versionchanged:: 1.3
        Parameters *coverage_options*, *coverage_exclude_lines*,
        *additional_ut_path* were added.
        See class `Coverage <http://coverage.readthedocs.org/en/coverage-4.0b1/api_coverage.html?highlight=coverage#coverage.Coverage.__init__>`_
        and `Configuration files <http://coverage.readthedocs.org/en/coverage-4.0b1/config.html>`_
        to specify those options. If both values are left to None, this function will
        compute the code coverage for all files in this module. The function
        now exports the coverage options which were used.
        For example, to exclude files from the coverage report::

            coverage_options=dict(omit=["*exclude*.py"])

        Parameter *covtoken* as added to post the coverage report to
        `codecov <https://codecov.io/>`_.

        Parameters *hook_print*, *stdout*, *stderr* were added.
    """
    runner = unittest.TextTestRunner(verbosity=0, stream=io.StringIO())
    path = os.path.abspath(os.path.join(os.path.split(codefile)[0]))

    def run_main():
        res = main(runner, path_test=path, skip=-1, skip_list=skip_list,
                   processes=processes, skip_function=skip_function,
                   additional_ut_path=additional_ut_path, stdout=stdout, stderr=stderr,
                   fLOG=fLOG)
        return res

    if "win" not in sys.platform and "DISPLAY" not in os.environ:
        # issue detected with travis
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        #os.environ["DISPLAY"] = "localhost:0"
        pass

    # to deal with: _tkinter.TclError: no display name and no $DISPLAY
    # environment variable
    from .tkinter_helper import fix_tkinter_issues_virtualenv, _first_execution
    fLOG("MODULES (1): matplotlib already imported",
         "matplotlib" in sys.modules, _first_execution)
    r = fix_tkinter_issues_virtualenv()
    fLOG("MODULES (2): matplotlib imported",
         "matplotlib" in sys.modules, _first_execution, r)

    def tested_module(folder, project_var_name, setup_params):
        # module mod
        if setup_params is None:
            setup_params = {}
        out, err = call_setup_hook(
            folder, project_var_name, fLOG=fLOG, use_print=hook_print, **setup_params)
        if len(err) > 0 and err != "no _setup_hook":
            # fix introduced because pip 8.0 displays annoying warnings
            # RuntimeWarning: Config variable 'Py_DEBUG' is unset, Python ABI tag may be incorrect
            # RuntimeWarning: Config variable 'WITH_PYMALLOC' is unset, Python
            # ABI tag may be incorrect
            lines = err.split("\n")
            keep = []
            for line in lines:
                line = line.rstrip("\r\t ")
                if line and not line.startswith(" ") and "RuntimeWarning: Config variable" not in line:
                    keep.append(line)
            if len(keep) > 0:
                raise SetupHookException(
                    "unable to run _setup_hook\n**OUT:\n{0}\n**ERR:\n{1}\n**FOLDER:\n{2}\n**NAME:\n{3}\n**KEEP:\n{4}\n**"
                    .format(out, err, folder, project_var_name, "\n".join(keep)))
            else:
                out += "\nWARNINGS:\n" + err
                err = None
        return out, err

    # project_var_name
    folder = os.path.normpath(
        os.path.join(os.path.dirname(codefile), "..", "src"))
    content = [_ for _ in os.listdir(folder) if not _.startswith(
        "_") and not _.startswith(".") and os.path.isdir(os.path.join(folder, _))]
    if len(content) != 1:
        raise FileNotFoundError(
            "unable to guess the project name in {0}\n{1}".format(folder, "\n".join(content)))

    project_var_name = content[0]
    src_abs = os.path.normpath(os.path.abspath(
        os.path.join(os.path.dirname(codefile), "..")))

    srcp = os.path.relpath(
        os.path.join(src_abs, "src", project_var_name), os.getcwd())

    if "USERNAME" in os.environ and os.environ["USERNAME"] in srcp:
        raise Exception(
            "The location of the source should not contain USERNAME: " + srcp)

    if only_setup_hook:
        tested_module(src_abs, project_var_name, setup_params)

    else:
        # coverage
        if add_coverage:
            if report_folder is None:
                report_folder = os.path.join(
                    os.path.abspath(os.path.dirname(codefile)), "..", "_doc", "sphinxdoc", "source", "coverage")

            fLOG("call _setup_hook", src_abs, "name=", project_var_name)
            tested_module(src_abs, project_var_name, setup_params)
            fLOG("end _setup_hook")

            fLOG("current folder", os.getcwd())
            fLOG("enabling coverage", srcp)
            dfile = os.path.join(report_folder, ".coverage")

            # we clean previous report or we create an empty folder
            if os.path.exists(report_folder):
                for afile in os.listdir(report_folder):
                    full = os.path.join(report_folder, afile)
                    os.remove(full)

            # we run the coverage
            if coverage_options is None:
                coverage_options = {}
            if "source" in coverage_options:
                coverage_options["source"].append(srcp)
            else:
                coverage_options["source"] = [srcp]
            if "data_file" not in coverage_options:
                coverage_options["data_file"] = dfile

            from coverage import coverage
            cov = coverage(**coverage_options)
            if coverage_exclude_lines is not None:
                for line in coverage_exclude_lines:
                    cov.exclude(line)
            else:
                cov.exclude("raise NotImplementedError")
            cov.start()

            res = run_main()

            cov.stop()

            cov.html_report(directory=report_folder)
            outfile = os.path.join(report_folder, "coverage_report.xml")
            cov.xml_report(outfile=outfile)
            cov.save()

            # we clean absolute path from the produced files
            fLOG("replace ", srcp, ' by ', project_var_name)
            srcp_s = [os.path.abspath(os.path.normpath(srcp)),
                      os.path.normpath(srcp)]
            bsrcp = [bytes(b, encoding="utf-8") for b in srcp_s]
            bproj = bytes(project_var_name, encoding="utf-8")
            for afile in os.listdir(report_folder):
                full = os.path.join(report_folder, afile)
                with open(full, "rb") as f:
                    content = f.read()
                for b in bsrcp:
                    content = content.replace(b, bproj)
                with open(full, "wb") as f:
                    f.write(content)

            # we print debug information for the coverage
            outcov = os.path.join(report_folder, "covlog.txt")
            rows = []
            rows.append("COVERAGE OPTIONS")
            for k, v in sorted(coverage_options.items()):
                rows.append("{0}={1}".format(k, v))
            rows.append("")
            rows.append("EXCLUDE LINES")
            for k in cov.get_exclude_list():
                rows.append(k)
            rows.append("")
            rows.append("OPTIONS")
            for option_spec in sorted(cov.config.CONFIG_FILE_OPTIONS):
                attr, where = option_spec[:2]
                v = getattr(cov.config, attr)
                st = "{0}={2}".format(attr, where, v)
                rows.append(st)
            rows.append("")
            content = "\n".join(rows)

            reps = []
            for _ in srcp_s[:1]:
                __ = os.path.normpath(os.path.join(_, "..", "..", ".."))
                __ += "/"
                reps.append(__)
                reps.append(__.replace("/", "\\"))
                reps.append(__.replace("/", "\\\\"))
                reps.append(__.replace("\\", "\\\\"))

            for s in reps:
                content = content.replace(s, "")

            with open(outcov, "w", encoding="utf8") as f:
                f.write(content)

            if covtoken:
                if isinstance(covtoken, tuple):
                    if eval(covtoken[1]):
                        # publishing token
                        fLOG("publishing coverage to codecov",
                             covtoken[0], "EVAL", covtoken[1])
                        publish_coverage_on_codecov(
                            token=covtoken[0], path=outfile, fLOG=fLOG)
                    else:
                        fLOG(
                            "skip publishing coverage to codecov due to False:", covtoken[1])
                else:
                    # publishing token
                    fLOG("publishing coverage to codecov", covtoken)
                    publish_coverage_on_codecov(
                        token=covtoken, path=outfile, fLOG=fLOG)
        else:
            if covtoken and (not isinstance(covtoken, tuple) or eval(covtoken[1])):
                raise CoverageException(
                    "covtoken is not null but add_coverage is not True, coverage cannot be published")
            tested_module(src_abs, project_var_name, setup_params)
            res = run_main()

        for r in res["tests"]:
            k = str(r[1])
            if "errors=0" not in k or "failures=0" not in k:
                fLOG("*", r[1], r[0])

        err = res.get("err", "")
        if len(err) > 0:
            raise Exception(err)
