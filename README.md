# Line Count
A library that counts the lines within a file, directory, or directory tree.

It can be run through the command line, or functions can be imported to be used in your own Python projects.

Some benefits of `linecount` over other libraries include:
- See the number of source lines of code (SLOC), commented lines, and blank lines
- Exclude files or directories whose names contain certain characters. This is useful for excluding files with certain file extensions, or certain directories like `venv` or `.git`.
- Only include files whose names contain certain characters. This is useful for counting lines of files with certain file extensions.

## Installing

You can install the project from the pypi test server:
```shell
$ pip install -i https://test.pypi.org/simple/ linecount
```
(this project is not on the main pypi yet, since account registration is closed for the main pypi server).

## Command Line Usage

### Help
You can get help on commands by performing:

```shell
$ linecount -h
$ linecount --help  # alternative way to write it
```

### Counting Lines of a File

```shell
$ linecount file_to_count.txt
```

### Counting Lines in a Directory
```shell
$ linecount . # count all files in this directory
$ linecount /path/to/dir  # or specify a directory this way
```

### Recursive
You can also count the lines of all files within a directory and all of its subdirectories. This command may take a while if you are counting the lines of a lot of files.
```shell
$ linecount . -r  # count all files in this directory + all subdirectories, recursively
$ linecount /path/to/dir -r  # another way to specify the directory
```

### Include Files
If you only want to count the lines of files containing a string in the filename, such as `.py` or `hello`, you can do:
```shell
$ linecount /path/to/dir -r --includefiles ".py,hello"
$ linecount /path/to/dir -r -if ".py,hello"  # alternative way to write it
```
This will only include files whose names contain `.py` or `hello`.  For example, the below files will be included:
```
hello.py
hello.txt
a.hello
cache.pyc
```

### Exclude Files
If you want to exclude files containing a certain string in their name, for example, `.txt`, we can do:
```shell
$ linecount /path/to/dir -r --excludefiles ".txt"
$ linecount /path/to/dir -r -ef ".txt"  # alternative way to write it
```

For example, this will exclude the following files:
```
myfile.txt
a.txt.py
```

### Exclude Dirs
You can also exclude directories that have a specific string in their name. For example, if you want to exclude the `venv` directory:
```shell
$ linecount /path/to/dir -r --excludedirs "venv"
$ linecount /path/to/dir -r -ed "venv"  # alternative way to write it
```

### Combining Include Files and Exclude Files
If you want to include files that have the string `.py`, but not `.pyc`, you can include `.py` and exclude `.pyc`:
```shell
$ linecount /path/to/dir -if ".py" -ef ".pyc"
```

## Python Usage