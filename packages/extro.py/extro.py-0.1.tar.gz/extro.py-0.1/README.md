# Extro.py

Extro.py reads dependency information from a set of directories and
produces an ordered listing of this directories.

## Usage

Pass a list of directories to the `extropy` command:

    $ cd /some/place
    $ for dir in $(extropy *); do
    > (cd $dir && ./run)
    > done

## Specifying dependency information

Extro.py looks for dependency information inside the `.deps` directory of
each named directory.  Inside the `.deps` directory it will read
information from the following files:

- `requires` -- Names (basename only, not paths) of directories
  required by this directory.
- `required_by` -- This is a reverse `requires`.  If `dir1` is
  *required_by* `dir2`, that is the same as if `dir2` had listed `dir1`
  in its `requires` file.
- `provides` -- a list of aliases that can be used to refer to the
  current directory.

## Example

In this example, we'll use Extro.py to help manage the runtime
initialization of Docker containers.

A Docker container is built from a series of layers.  Each layer may
want to perform some runtime initialization when a container starts.
In this situation it is likely that there needs to be an ordering
between these initialization tasks.

One solution is for each layer to place initialization information
into a subdirectory of `/docker/config.d`.  Then have an `ENTRYPOINT`
script that looks something like this:

    #!/bin/sh

    for dir in $(extropy /docker/config.d/*); do
      (cd $dir && ./run)
    done

    exec "$@"

This will execute the `run` command inside each subdirectory, while
permitting you to define an explicit ordering between different
layers. For example, let's say you have a base image that implements
some sort of process supervision and logging.  It needs to ensure that
the target log directory has appropriate ownership (and this needs to
happen at runtime, in case the directory is a mounted volume). 

On top of that logging image, you build a new image that runs a web
application. The web application needs to perform some database
initialization tasks when it starts up, and you want to make sure that
logging is configured *before* you run the database initialization.

To solve this, you have your logging container install the directory
`/docker/config.d/logging` with the following content:

    /docker/config.d/logging/
      run

And you have your web application provide:

    /docker/config.d/webapp/
      run
      .deps/
        requires

And the `requires` file contains `logging`.  With this in place, the
`ENTRYPOINT` script will run the `run` script for both directories,
and the `logging` run script will always run before the `webapp` run
script.
## License

extro.py -- imposes an ordering on a list of directories  
Copyright (C) 2016 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
