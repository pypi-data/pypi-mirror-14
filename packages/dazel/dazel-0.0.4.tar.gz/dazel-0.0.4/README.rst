dazel
=====

Run Google's bazel inside a docker container via a seamless proxy.

bazel is awesome at creating fast and reproducible builds on your own
development environemnt. The problem is that it works in an imperfect
and non-portable environment. Enter dazel.

dazel allows you to create your build environment as a Docker image,
either via a Dockerfile or a prebuilt repository. The tool itself is a
simple python script that sends the command line arguments directly to
bazel inside the container, and mapping all of the necessary volumes to
make it seamless to you. It uses the 'docker exec' command to achieve
this, and maps the current directory and the bazel-WORKDIR link
directory so that the results appear on the host seamlessly.

It is run the same way you would bazel:

.. code:: bash

    dazel build //my/cool/package/...
    dazel run //my/cool/package:target

This was a simple build and run. The command line arguments were sent as
is into the docker container, and the output was run again inside the
container.

Running the command for the first time will start the container on it's
own, and it will automatically detect if there is need to rebuild or
restart the container. You can configure anything you need through the
".dazelrc" file in the same directory. Take a look at the configuration
section for information on how to write one.

Installation
------------

Dependencies
~~~~~~~~~~~~

.. code:: bash

    apt-get install python python-pip
    apt-get install docker

Install dazel
~~~~~~~~~~~~~

.. code:: bash

    pip install dazel

That's all there is to it. Even bazel is not required!

Configuration
-------------

You can configure dazel in two ways (or combine): \* A .dazelrc file in
the current directory. \* Environment variables with the configuration
parameters mentioned below.

Note that specific environment variables supercede the values in the
.dazelrc file.

The possible parameters to set are: \* DAZEL\_INSTANCE\_NAME="name of
the docker container to run" [Default: "dazel"] \*
DAZEL\_IMAGE\_NAME="name of the dazel image to build or pull" [Default:
"dazel"] \* DAZEL\_DOCKERFILE="path to the Dockerfile to use to build
the dazel image" [Default: "Dockerfile.dazel"] \* DAZEL\_REPOSITORY="the
repository to pull the dazel image from" [Default: "dazel"] \*
DAZEL\_DIRECTORY="the directory to build the dazel image in" [Default:
$PWD] \* DAZEL\_COMMAND="the command to run when building: [Default:
"/bazel/output/bazel"] \* DAZEL\_VOLUMES=[":", ...] or ":,..." [Default:
""] \* DAZEL\_RUN\_DEPS=["run\_dependency/image\_to\_load:tag",...] or
"another/image:tag,..." [Default: ""] \* DAZEL\_NETWORK="the name of the
network on which to load all run dependencies and dazel container"
[Default: "dazel"]
