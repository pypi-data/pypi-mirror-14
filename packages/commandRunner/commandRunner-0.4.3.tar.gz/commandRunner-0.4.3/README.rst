commandRunner
=============

commandRunner is yet another package created to handle running commands,
scripts or programs on the command line. The simplest class lets you run
anything locally on your machine. Later classes are targeted at Analytics
and data processing platforms such as Grid Engine and HADOOP. The class
attempts to run commands in a moderately thread safe way by requiring that
you provide with sufficient information that it can build a uniquely labeled
tmp directory for all input and output files. This means that this can play
nicely with things like Celery workers.

Release 0.4.2
-------------

This release supports running commands on localhost and DRMAA compliant grid
engine installs (ogs, soge and univa). Commands are built/interpolated via
some simple rules.

Future
------

In the future we'll provide classes to run commands over RServe,
Hadoop, Octave, and SAS Server.


Usage
-----
This is the basic usage::

    from commandRunner.localRunner import *

    r = localRunner(tmp_id="ID_STRING", tmp_path=,/tmp/", out_glob=['file', ],
                    command="ls /tmp", input_data={DATA_DICT})
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

__init__ initalises all the class variables needed and performs the command
string interpolation.

Interpolation rules work the following way. The command string is split in to
tokens if you provide a list of flags or a dict of options theses are inserted
between the 0th and 1st token. So if you call with the following. If you
provide a std_out_str then an appropriate redirection will be added to the
end of your command string::

    r = localRunner(tmp_id="ID_STRING",
                    tmp_path=,/tmp/",
                    out_glob=['file', ],
                    flags=["-a","-l"]
                    options={"b", "this"}
                    command="ls /tmp",
                    input_data={DATA_DICT},
                    str_out_str="file.stdout")

You will effectively build the following command::

      ls -a -l b this /tmp > file.stdout

The command string builing supports some limited interpolation. Anything
labeled $INPUT or $OUTPUT will be replaced with the input_string and
output_string if you provide them on intialisation.

r.prepare() builds a temporary directory and makes any input file which is
needed. In the example given tmp_id="ID_STRING", specifies a path where
temporary files can be placed are used eith tmp_path to create a tempdir
called /tmp/ID_STRING/.

Next it takes input_data. This is a dict of {Filename:Data_string} values.
Iterating over, it writes the data to a file after the key in the tempdir. So
the following dict::

    { "test.file" : "THIS IS MY STRING OF DATA"}

would result in a file with the path /tmp/ID_STRING/test.file

out_glob is an array of file suffixes which we want to gather up when the
command completes.

Note that only tmp_id, tmp_path and command are required. Omitting
input_data or out_glob assumes that there are respectively no input files to
write or output files to gather.

The line r.run_cmd(success_params=[0]) runs the command string provided.

Once complete if out_globs have been provided and the files were output then
the contents of those files can be found in the dict r.output_data. which has
the same {Filename:Data_string} form as the input_data dict::

{ "output.file" : "THIS IS MY PROCESSED DATA"}

r.tidy() cleans up deleting any input and output files and the temporary
working directory. Any data in the output file is available in to r.output_data

Grid Engine Quirks
------------------

geRunner uses python DRMAA to submit jobs. A consequence of this that a command
string is not constructed in quite the same way. The first portion of the
command string is split off as a command. Subsequence portions are tokenised
and added to a params array to be passed to DRMAA

The Options dict is flattened to a key:value list. You can include or omit as
many of those as you'd like options as you like. Any instance of the string
$INPUT and $OUTPUT in final args array will be interpolated for the input_string
and output_string respectively

If std_out_string is provided it will be used as
a file where the Grid Engine thread STDOUT will be captured::

    from commandRunner.geRunner import *

    r = geRunner(tmp_id="ID_STRING", tmp_path=,/tmp/", out_glob=['file'],
                 command="ls -lah", input_data={"File.txt": "DATA"},
                 options = {"-file": "$OUTPUT"},
                 input_string="test.file", output_string="out.file"
                 std_out_string="std.out")
    r.prepare()
    exit_status = r.run_cmd(success_params=[0])
    r.tidy()
    print(r.output_data)

Although DRMAA functions differently you can think of this as effectively
run the following command (after following the interpolation rules)::

   ls -file out.file -lah > std.out

Tests
-----

Best to run these 1 suite at a time, geRunner tests will fail if you do not
have Grid Engine installed, DRMAA_LIBRARY_PATH set and SGE_ROOT set.

Run tests with::

    python setup.py test -s tests/test_commandRunner.py
    python setup.py test -s tests/test_localRunner.py
    python setup.py test -s tests/test_geRunner.py

TODO
----

1. Implement rserveRunner for running commands in r
2. Implement hadoopRunner for running command on Hadoop
3. Implement sasRunner for a SAS backend
4. Implement octaveRunner for Octave backend
5. matlab? mathematica?
