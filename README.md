# riiid_auto_translator
Automatic translation module for Riiid files and documents

`riiid_auto_translator` is a module that uses Google Cloud Translation to automatically translate certain types of files.

The module currently supports the following types of file: `json`.




    # to do:

    # add capability for xls (just a matter of switching MIME type)

    # clean up the current code

    # separate a main.py and create a class that handles function usage based on file extensions

    # try converting txts into docxs, translate, and turn them back into txt (for speed)
    
    # if I pick a folder with multiple folders inside, the structure should be replicated inside /output so I don't have to do this manually

    # multiprocessing / progress bar

    # test (make sure input json # and output json # are the same)write unit test but also write in-functionv validation

    # if there are files of same name, those files should be taken out of the queue

    # make a temporary dictionary (or permanently stored in a excel in the root folder) so that already-translated words don't have to invoke API

    # make a report at the end (look into logger), display 1) times API called 2) number of charts sent 3) number of new words added to the glossary excel

    # make argparse (be able to set file paths and output paths and excel glossary path)

    # make a GUI

    # if a file stops in middle due to error, remember the last position and start over from there next time

    # create a debug=true mode so that api calls aren't made during development when not necessary

    # when sending a list of strings to google API, change the number of strings so that the combined characters do not exceed 5000 and as many as possible strings can be sent to API at one time OR test converting the json file into docx so that whole file can be sent at once (compare this with the previously completed file and see if translations are identical or close enough) 
