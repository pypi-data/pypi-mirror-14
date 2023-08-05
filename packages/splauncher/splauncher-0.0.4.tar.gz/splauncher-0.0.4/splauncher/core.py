from __future__ import print_function

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$May 18, 2015 16:52:18 EDT$"


import datetime
import os
import logging


drmaa_logger = logging.getLogger(__name__)

try:
    import drmaa
except ImportError:
    # python-drmaa is not installed.
    drmaa_logger.error(
        "Was not able to import drmaa. " +
        "If this is meant to be run using the OpenGrid submission " +
        "system, then drmaa needs to be installed via pip or " +
        "easy_install."
    )
    raise
except RuntimeError:
    # The drmaa library was not specified, but python-drmaa is installed.
    drmaa_logger.error(
        "Was able to import drmaa. " +
        "However, the drmaa library could not be found. Please " +
        "either specify the location of libdrmaa.so using the " +
        "DRMAA_LIBRARY_PATH environment variable or disable/remove " +
        "use_drmaa from the config file."
    )
    raise


def main(*argv):
    job_time = datetime.datetime.utcnow()
    job_time_str = job_time.isoformat().replace(":", ".")
    job_name = "splaunch_" + argv[1].replace("/", "-") + "_" + job_time_str

    s = drmaa.Session()
    s.initialize()

    session_name = s.contact

    job_template = s.createJobTemplate()
    job_template.jobName = job_name
    job_template.remoteCommand = argv[1]
    job_template.args = argv[2:]
    job_template.jobEnvironment = os.environ
    job_template.inputPath = "localhost:" + os.devnull
    job_template.outputPath = "localhost:" + job_name + ".out"
    job_template.errorPath = "localhost:" + job_name + ".err"
    job_template.workingDirectory = os.getcwd()
    job_template.nativeSpecification = "-pe batch " + str(1)

    process_id = s.runJob(job_template)
    s.deleteJobTemplate(job_template)

    s.exit()

    print(
        "From context \"%s\" launched job \"%s\" with process ID \"%s\"." % (
            session_name, job_name, process_id
        )
    )

    return(0)
