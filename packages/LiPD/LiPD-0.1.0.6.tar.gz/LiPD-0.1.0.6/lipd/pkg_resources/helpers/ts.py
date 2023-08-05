def extractTimeSeries(lipd_library, timeseries_library, convert):
    """
    Create a TimeSeries using the current files in LiPD_Library.
    :return: (obj) TimeSeries_Library
    """
    # Loop over the LiPD objects in the LiPD_Library
    for k, v in lipd_library.get_master().items():
        # Get metadata from this LiPD object. Convert it. Pass TSO metadata to the TS_Library.
        timeseries_library.loadTsos(v.get_name_ext(), convert.ts_extract_main(v.get_master()))

def exportTimeSeries(lipd_library, timeseries_library, convert):
    """
    Export TimeSeries back to LiPD Library. Updates information in LiPD objects.
    """
    l = []
    # Get all TSOs from TS_Library, and add them to a list
    for k, v in timeseries_library.get_master().items():
        l.append({'name': v.get_lpd_name(), 'data': v.get_master()})
    # Send the TSOs list through to be converted. Then let the LiPD_Library load the metadata into itself.
    lipd_library.load_tsos(convert.lipd_extract_main(l))

