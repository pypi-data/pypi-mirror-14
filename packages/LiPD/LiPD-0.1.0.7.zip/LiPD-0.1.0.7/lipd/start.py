from .pkg_resources.lipd.LiPD_Library import *
from .pkg_resources.timeseries.Convert import *
from .pkg_resources.timeseries.TimeSeries_Library import *

# GLOBALS
lipd_lib = LiPD_Library()
ts_lib = TimeSeries_Library()
convert = Convert()
path = set_source()


def setDir():
    """
    Set the current working directory by providing a directory path.
    (ex. /Path/to/files)
    :param path: (str) Directory path
    """
    path = set_source()


def loadLipd(filename):
    """
    Load a single LiPD file into the workspace. File must be located in the current working directory.
    (ex. loadLiPD NAm-ak000.lpd)
    :param filename: (str) LiPD filename
    """
    lipd_lib.loadLipd(filename)


def loadLipds(arg):
    """
    Load all LiPD files in the current working directory into the workspace.
    """
    self.lipd_lib.loadLipds()


# ANALYSIS - LIPD


def showCsv(filename):
    """
    Show CSV data for one LiPD
    :param filename:
    :return:
    """
    lipd_lib.showCsv(filename)


def showLipd(filename):
    """
    Display the contents of the specified LiPD file. (Must be previously loaded into the workspace)
    (ex. displayLiPD NAm-ak000.lpd)
    :param filename: (str) LiPD filename
    """
    lipd_lib.showLipd(filename)


def showLipds():
    """
    Prints the names of all LiPD files in the LiPD_Library
    """
    lipd_lib.showLipds()


def map(filename):
    """

    :param filename:
    :return:
    """
    # No input given. Map all LiPDs
    if not filename:
        lipd_lib.mapAll()
    # One or more records given. Map them.
    else:
        lipd_lib.map(filename)
    return


# ANALYSIS - TIME SERIES


def extractTimeSeries(arg):
    """
    Create a TimeSeries using the current files in LiPD_Library.
    :return: (obj) TimeSeries_Library
    """
    # Loop over the LiPD objects in the LiPD_Library
    for k, v in lipd_lib.get_master().items():
        # Get metadata from this LiPD object. Convert it. Pass TSO metadata to the TS_Library.
        ts_lib.loadTsos(v.get_name_ext(), convert.ts_extract_main(v.get_master()))


def exportTimeSeries(arg):
    """
    Export TimeSeries back to LiPD Library. Updates information in LiPD objects.
    """
    l = []
    # Get all TSOs from TS_Library, and add them to a list
    for k, v in ts_lib.get_master().items():
        l.append({'name': v.get_lpd_name(), 'data': v.get_master()})
    # Send the TSOs list through to be converted. Then let the LiPD_Library load the metadata into itself.
    lipd_lib.load_tsos(convert.lipd_extract_main(l))


def showTso(name):
    """
    Show contents of one TimeSeries object.
    :param name:
    :return:
    """
    ts_lib.showTso(name)


def showTsos(arg):
    """
    Prints the names of all TimeSeries objects in the TimeSeries_Library
    :return:
    """
    ts_lib.showTsos()

# CLOSING


def saveLipd(filename):
    """
    Saves changes made to the target LiPD file.
    (ex. saveLiPD NAm-ak000.lpd)
    :param filename: (str) LiPD filename
    """
    lipd_lib.saveLipd(filename)


def saveLipds():
    """
    Save changes made to all LiPD files in the workspace.
    """
    lipd_lib.saveLipds()


def removeLipd(filename):
    """
    Remove LiPD object from library
    :return: None
    """
    lipd_lib.removeLipd(filename)
    return


def removeLipds(arg):
    """
    Remove all LiPD objects from library.
    :return: None
    """
    lipd_lib.removeLipds()
    return


def quit():
    """
    Quit and exit the program. (Does not save changes)
    """
    # self.llib.close()
    return True


def set_source():
    """
    User sets the path to LiPD source. Local or online.
    :return: (str) Path
    """
    path = None
    invalid = True
    count = 0
    while invalid:
        print("Where are your files stored? Choose an option by number:\n1. Online URL\n2. Local Computer\n3. "
              "Downloads "
              "Folder\n")
        option = input("Option: ")
        if option == '1':
            # Retrieve data from the online URL
            path = input("Enter the URL: ")
        elif option == '2':
            # Open up the GUI browse dialog
            path = browse_dialog()
            # Set the path to the local files in CLI and lipd_lib
        elif option == '3':
            # Set the path to the system downloads folder.
            path = os.path.expanduser('~/Downloads')
        else:
            # Something went wrong. Prompt again. Give a couple tries before defaulting to downloads folder
            if count == 2:
                print("Defaulting to Downloads Folder.")
                path = os.path.expanduser('~/Downloads')
            else:
                count += 1
                print("Invalid option. Try again.")
        if path:
            invalid = False
    lipd_lib.setDir(path)

    return path

