# riiid_auto_translator
Automatic translation module for Riiid files and documents

`riiid_auto_translator` is a module that uses Google Cloud Translation to automatically translate certain types of files.

The module currently supports the following types of file: `json`.




    # to do:
    
    # make a temporary dictionary (or permanently stored in a excel in the root folder) so that already-translated words don't have to invoke API (have to solve the racing condition because of the multithreading) (re.compile("[ㄱ-힣]"))

    # test (make sure input json # and output json # are the same)write unit test but also write in-functionv validation

    # make argparse (be able to set file paths and output paths and excel glossary path)

    # enable custom list sort by accepting key

    # make a GUI

    # if a file stops in middle due to error, remember the last position and start over from there next time (try / except: save a partial file. When starting again, compare the lengths of source file and found target file and if lengths are different, create a new list from the source of the dicts that dont exist in the target and translated them. Then load the existing dicts_list, add the new dicts, and sort, then overwrite the existing target file)

    # create a debug=true mode so that api calls aren't made during development when not necessary (create and use a mock data with really few chars. regressive discovery is already working one folder is enough for mock purpose)

    # when sending a list of strings to google API, change the number of strings so that the combined characters do not exceed 5000 and as many as possible strings can be sent to API at one time OR test converting the json file into docx so that whole file can be sent at once (compare this with the previously completed file and see if translations are identical or close enough) 
