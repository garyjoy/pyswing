import logging
import os
import shutil

from utils.Logger import Logger


def ensureDirectoryExists(relativeDirectoryPath):
    if not os.path.exists(relativeDirectoryPath):
        Logger.log(logging.INFO, "Creating Directory",
                   {"scope": __name__, "relativeDirectoryPath": relativeDirectoryPath})
        try:
            os.makedirs(relativeDirectoryPath)
        except IOError as ioError:
            Logger.log(logging.ERROR, "Cannot Create Directory",
                       {"scope": __name__, "relativeDirectoryPath": relativeDirectoryPath})
            Logger.log(logging.DEBUG, "Caught Exception", {"scope": __name__, "exception": str(ioError)})


def deleteDirectory(relativeDirectoryPath):
    """
    Delete the specified directory.

    :param relativeDirectoryPath: Relative (from the working directory) path to a directory (i.e. that we want to delete).
    """

    try:
        if os.path.exists(relativeDirectoryPath):
            shutil.rmtree(relativeDirectoryPath)
    except OSError as osError:
        Logger.log(logging.ERROR, "Cannot Delete Directory", {"scope":__name__, "directory":relativeDirectoryPath})
        Logger.log(logging.DEBUG, "Caught Exception", {"scope":__name__, "exception":str(osError)})


def deleteFile(relativeFilePath):
    """
    Delete the specified file.

    :param relativeFilePath: Relative (from the working directory) path to a file (i.e. that we want to delete).
    """

    try:
        if os.path.exists(relativeFilePath):
            if ("pyswing.db" not in relativeFilePath):
                Logger.log(logging.INFO, "Delete File", {"scope":__name__, "file":relativeFilePath})
                os.remove(relativeFilePath)
            else:
                Logger.log(logging.WARN, "Do You Want To Delete This Database?", {"scope":__name__, "file":relativeFilePath})
    except OSError as osError:
        Logger.log(logging.ERROR, "Cannot Delete File", {"scope":__name__, "directory":relativeFilePath})
        Logger.log(logging.DEBUG, "Caught Exception", {"scope":__name__, "exception":str(osError)})


def forceWorkingDirectory():
    """
    forceWorkingDirectory() will ensure that the working directory is set to the project root (i.e. /Users/Gary/PycharmProjects/pyswing).

    There is a discrepancy between TeamCity (which always forces the working directory to be the project root) and IDEs
    (e.g. Eclipse, PyCharm) (which, by default, set the working directory to be the directory containing the script being run).
    """

    Logger().log(logging.DEBUG, "Log Method Call", {"scope":__name__, "arguments":""})

    workingDirectory = os.path.abspath(os.path.curdir)
    if (os.path.exists("pyswing") and os.path.exists("test")):
        Logger().log(logging.DEBUG, "Working Directory", {"scope":__name__, "workingDirectory":workingDirectory})
    else:
        newWorkingDirectory = None

        if os.path.exists("../pyswing") and os.path.exists("../test"):
            newWorkingDirectory = os.path.abspath("../")
        elif os.path.exists("../../pyswing") and os.path.exists("../../test"):
            newWorkingDirectory = os.path.abspath("../../")
        elif os.path.exists("../../../pyswing") and os.path.exists("../../../test"):
            newWorkingDirectory = os.path.abspath("../../../")
        elif os.path.exists("../../../../pyswing") and os.path.exists("../../../../test"):
            newWorkingDirectory = os.path.abspath("../../../../")
        elif os.path.exists("../../../../../pyswing") and os.path.exists("../../../../../test"):
            newWorkingDirectory = os.path.abspath("../../../../../")
        elif os.path.exists("../../../../../../pyswing") and os.path.exists("../../../../../../test"):
            newWorkingDirectory = os.path.abspath("../../../../../../")

        if newWorkingDirectory is not None:
            os.chdir(newWorkingDirectory)
            Logger().log(logging.DEBUG, "Changed Working Directory", {"scope":__name__, "old":workingDirectory,"new":newWorkingDirectory})

        else:
            Logger().log(logging.WARN, "Cannot Change Working Directory", {"scope":__name__, "workingDirectory":workingDirectory})
