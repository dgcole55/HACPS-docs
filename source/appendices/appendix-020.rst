
.. _setup-microkit-tutorials:

==================================
Setting up seL4 Microkit Tutorials
==================================

.. 
    https://docs.sel4.systems/projects/dockerfiles/

    Install Docker
    --------------

    https://www.docker.com/


    The seL4 Microkit
    -----------------

    https://docs.sel4.systems/projects/microkit/

We want to be able to use the seL4 tutorials: `<https://docs.sel4.systems/Tutorials/>`_.  This is easiest using `Docker <https://docker.com>`_.  

These are the steps:

1. Setup Docker
2. Install the tutorials
3. Run the "Hello World" tutorial
4. Install Microkit 
5. Install the Microkit tutorial

All of the steps given below are for a Linux machine, but I got them to work on a Mac (thank you Docker!).

.. admonition:: Windows

    If you are on a Windows machine, you will have more success setting up a virtual machine running Ubuntu and then following the instructions above. There are lots of guides for this online.  Here's one: `<https://www.geeksforgeeks.org/how-to-install-ubuntu-on-virtualbox/>`_

Setup Docker Container and Test
===============================

The instructions given here `<https://docs.sel4.systems/Tutorials/setting-up>`_ ar the best reference.  In this section, we will provide commentary on that process.

Setup Docker
------------

Go to the `Docker <https://docker.com>`_ website and download docker.  The install should be straightforward.  I would recommend accepting defaults.  You will need to make a Docker account for this.  

Keep the desktop app running in the background.

Get the Docker build environment for seL4 and CAmkES
----------------------------------------------------

Decide where you want all of your seL4 stuff to live.  I made a directory ``~/seL4`` where I keep everything for running stuff on seL4.  Go to that directory.  We will download the Docker files for seL4 and CAmkES there.

To download the necessary Docker files for seL4 and CAmkES, run:

.. code-block:: bash

    git clone https://github.com/seL4/seL4-CAmkES-L4v-dockerfiles.git
    cd seL4-CAmkES-L4v-dockerfiles
    make user

When you run this, the ``git clone https://github.com/seL4/seL4-CAmkES-L4v-dockerfiles.git`` will fetch the relevant images from seL4's GitHub repository.  This makes a directory ``seL4-CAmkES-L4v-dockerfiles``.  You change to that directory.  There you run ``make user``, which does some magic Docker stuff.  The last line on the screen should be something like:

.. code-block:: bash

    Hello, welcome to the seL4/CAmkES/L4v docker build environment    

.. admonition:: Mac

    The ``make user`` step was the only hiccup I had in this process.  The instructions on those pages are for a Linux machine.  I did all of this on a Mac too, only having to make a change to a Makefile because of how it accesses "localtime."  The Makefile has a line like this.

    .. code-block:: Makefile
    
        ETC_LOCALTIME := $(realpath /etc/localtime)

    that should be changed to this
    
    .. code-block:: Makefile

        ETC_LOCALTIME := /etc/localtime
    
    A lame explanation:  on a Mac, ``/etc/localtime`` is a link that points to a file ``/usr/share/zoneinfo.default/America/New_York`` that presumably contains the local time.  When Docker tries to create the container, it tries to mount the file on the link, causing problem.  By calling out the link explicitly, the problem is solved.


Start a container
-----------------

Docker makes it easy to package and run applications without worrying about dependencies and particulars of your machine.  It uses **containers**, which are like lightweight, portable boxes that hold everything needed to run --- without needing an entire operating system or virtual machines. 

You want to be able to run the container in other directories.  To do this in bash (or zsh) it is convenient to create an alias.  To do this, put this line in your ``.bashrc`` (``.zshrc``) file.

.. code-block:: bash

    alias container='make -C /<path>/<to>/seL4-CAmkES-L4v-dockerfiles user HOST_DIR=$(pwd)'

Replace the ``/<path>/<to>/`` with the name of the directory (use the absolute path) you put the Docker files; for me, this was ``~/seL4/``.  Once you make changes to your ``.bashrc`` file, restart the bash environment with ``source ~/.bashrc``.

Now when you type 

.. code-block:: bash

    $ container

You should get a bunch of magic Docker stuff that ends with 

.. code-block:: 

    ___
     |   _      _ |_      _   _ |_ |_     
     |  |  |_| _) |_ \)/ (_) |  |_ | ) \/ 
                                       /  
     __                                   
    (_      _ |_  _  _   _                
    __) \/ _) |_ (- ||| _)                
        /                                 
    Hello, welcome to the seL4/CAmkES/L4v docker build environment
    username@in-container:/host$ 
 
You are now in an environment with a prompt where you can manage files and build seL4, but with access to the necessary dependencies.  The ``/host`` directory is the directory from whence you ran ``container``.  The files in this directory can be see from a normal bash (zsh) prompt.  You can edit them in your normal environment, and then compile in the container environment to get working seL4 applications.

Install and run seL4test
------------------------

To check the install, you can used seL4test. You can put the seL4test directory anywhere, but I put mine in ``~/seL4``.  To do that, go to ``~/seL4`` and do the following:

.. code-block:: bash

    $ mkdir seL4test
    $ cd seL4test
    $ repo init -u https://github.com/seL4/seL4test-manifest.git
    $ repo sync

Your directory ``~/seL4/seL4test`` should have a bunch of stuff in it.  Mine looks like this.

.. code-block:: bash

    (.venv) HACPS-docs % ls ~/seL4/seL4test         
    build-x86           griddle             kernel              tools
    easy-settings.cmake init-build.sh       projects

To run the test, do the following from in the ``seL4test`` directory.

.. code-block:: bash

    $ container     # this starts the container and the seL4 environment
    /host$ mkdir build-x86
    /host$ cd build-x86
    /host/build-x86$ ../init-build.sh -DPLATFORM=x86_64 -DSIMULATION=TRUE
    /host/build-x86$ ninja
    /host/build-x86$ ./simulate

The steps are this.

1. You make a build directory for the test simulation.  You will compile the seL4 kernel from there.
2. ``../init-build.sh`` is a command (actually a link to a command) in the ``/host`` directory.  This sets everything up to be able to compile.
3. ``ninja`` does the compiling and building of the test simulation.
4. ``./simulate`` runs the simulation.  

If all is right with the universe, you will see screen loads of stuff, and it should end with something like

.. code-block:: bash

    Starting test 121: Test all tests ran
    Test suite passed. 121 tests passed. 57 tests disabled.
    All is well in the universe

Congrats!  seL4 is running.  Breathe a sigh of relief.

Install the tutorials
=====================

The instructions for getting the tutorials are here:  `<https://docs.sel4.systems/Tutorials/get-the-tutorials>`_.  

To make this work, my suggestion is to create a virtual environment for python.

.. code-block:: bash

    $ python -m venv .venv

This creates a virtual environment that you activate with

.. code-block:: bash

    $ source .venv/bin/activate
    (.venv) $ 

Now you can install the CAmkES dependencies.

.. code-block:: bash

    (.venv) $ pip install camkes-deps

Note that this is slightly different from the instructions given at the seL4 site, but it should still work.

Now get the tutorials' code:

.. code-block:: bash

    (.venv) $ mkdir seL4-tutorial-manifest
    (.venv) $ cd seL4-tutorial-manifest
    (.venv) $ repo init -u https://github.com/seL4/sel4-tutorials-manifest
    (.venv) $ repo sync

Now your ``sel4-tutorial-manifest`` directory looks like something like this:

.. code-block:: bash

    (.venv) $ ls
    README-camkes.md    README.md       REMOVE_apps     init          
    kernel          projects            tools

.. note:: 

    One thing to be aware of is that sometimes the folks maintaining the seL4 repositories call some things ``seL4`` other times ``sel4``, some with an uppercase ``L``, others with a lowercase ``l``.  Be aware that this is happening. 

    Above, I gave the tutorial manifest directory an uppercase ``L`` to be consistent, even though the repository has it in lowercase.  That sort of consistency helps my sanity when searching through and changing directories.

Run the Hello World tutorial
============================

Instructions for running the "Hello World" tutorial are here: `<https://docs.sel4.systems/Tutorials/hello-world>`_.

You want to start in the ``seL4-tutorial-manifest`` directory.  Then create a container.

.. code-block:: bash

    (.venv) $ container

Now you should be in the seL4 environment at a ``/host$`` prompt.  Now run the following:

.. code-block:: bash

    /host$ ./init --tut hello-world

This automatically creates the directories ``hello-world`` and ``hello-world_build``.  It is helpful to also have solutions.  To do that

.. code-block:: bash

    /host$ mkdir hello-world-soln
    /host$ cd hello-world-soln
    /host$ ../init --tut hello-world --solution

This creates the solutions in the ``hello-world-soln`` directory and build directory in its parent directory ``/host``.

To run the ``hello-world`` tutorial,

.. code-block:: bash

    /host$ cd hello-world_build
    /host/hello-world_build$ ninja
    /host/nello-world_build$ ./simulate

Somewhere in the long printout should be

.. code-block:: 

    Booting all finished, dropped to user space
    Hello, World!    

Now, you can edit the ``hello-world/src/main.c`` file.  For example,

.. code-block:: c

    #include <stdio.h>
    
    int main(int argc, char *argv[]) {
        printf("Hello, World!\n");
        printf("Hello, sel4!\n");
        printf("What is next?\n");
    return 0;
    }

Now, somewhere in the long printout should be

.. code-block:: 

    Booting all finished, dropped to user space
    Hello, World!
    Hello, sel4!
    What is next?

Congrats again!  Take another breath.

Install the Microkit tutorial
=============================

Instructions for installing the Microkit tutorial are here:  `<https://trustworthy.systems/projects/microkit/tutorial/>`_.  

Here we will go over the instructions for installing using **Option 2 - Docker**.

You will want three things:

1. The Microkit SDK
2. The tutorials
3. The solutions

All can be downloaded as ``.tar.gz`` files.  Here is my suggestion.  Make a directory ``microkit-tutorials`` wherever you are keeping your seL4 stuff.  Then, download the three into that directory.

.. code-block:: bash

    $ mkdir microkit-tutorial
    $ cd microkit-tutorial
    $ curl -L https://github.com/seL4/microkit/releases/download/1.4.1/microkit-sdk-1.4.1-linux-x86-64.tar.gz -o sdk.tar.gz
    $ curl -L trustworthy.systems/Downloads/microkit_tutorial/tutorial.tar.gz -o tutorial.tar.gz
    $ curl -L trustworthy.systems/Downloads/microkit_tutorial/solutions.tar.gz -o solutions.tar.gz

Now you should have three files in your ``microkit-tutorial`` directory.

.. code-block:: bash

    $ ls
    sdk.tar.gz      tutorial.tar.gz         solutions.tar.gz
    
Now, expand the ``.tar.gz`` files.

.. code-block:: bash

    $ tar xf sdk.tar.gz
    $ tar xf tutorial.tar.gz
    $ tar xf solution.tar.gz

This creates three directories.

.. code-block:: bash

    $ ls 
    microkit-sdk-1.4.1 solutions          tutorial
    sdk.tar.gz         solutions.tar.gz   tutorial.tar.gz

.. warning::

    The ``Makefile`` in the tutorial and solutions has a small problem. It references the wrong SDK.  At the very top of the ``Makefile`` it has something like

    .. code-block:: make

        MICROKIT_SDK := ../microkit-sdk-1.4.0
 
    The version number for the SDK must match the version number of your directory.  For example, I changed it to

    .. code-block:: make

        MICROKIT_SDK := ../microkit-sdk-1.4.1

    and everything works.  You need to do this in the ``solutions`` directory too, if you want to run those.

At this point, you should be ready to go through the tutorials starting at `Part 1 <https://trustworthy.systems/projects/microkit/tutorial/part1.html>`_.  