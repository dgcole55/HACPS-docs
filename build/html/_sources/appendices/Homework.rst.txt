

===========================================
Homework
===========================================

1. Write about a cyber-physical system failure that interests you.  You can use this list of examples or, even better, find a different example that we can learn about.  The writing should be 3--5 pages long.  Submit a PDF please.

2. Reading
    - Biggs, Simon, Damon Lee, and Gernot Heiser. "The jury is in: Monolithic os design is flawed: Microkernel-based designs improve security." *Proceedings of the 9th Asia-Pacific Workshop on Systems.* 2018. `<https://doi.org/10.1145/3265723.3265733>`_  

    -  Fisher Kathleen, John Launchbury, and Richards Raymond. 2017.  "The HACMS program: using formal methods to eliminate exploitable bugs." *Phil. Trans. R. Soc. A.* **375**:20150401 `<https://doi.org/10.1098/rsta.2015.0401>`_
    
3. Reading
    - Heiser, Gernot. "The sel4 Microkernel --- An Introduction." The seL4 Foundation (2020). `<https://sel4.systems/About/seL4-whitepaper.pdf>`_

4. We want to be able to use the seL4 tutorials: `<https://docs.sel4.systems/Tutorials/>`_.
    
    For this homework we will focus on setting up the machine and getting through the Hello World tutorial.

    - Setup Docker:  start here: `<https://docs.sel4.systems/Tutorials/setting-up>`_. This will setup Docker, start a container, and run ``seL4test``.
    - Install the tutorials: `<https://docs.sel4.systems/Tutorials/get-the-tutorials>`_
    - Run the Hello World tutorial: `<https://docs.sel4.systems/Tutorials/hello-world>`_

    .. raw:: html

        <p>&nbsp;</p>

    .. admonition:: Mac

        The instructions on those pages are really for a Linux machine.  I did all of this on a Mac too, only having to make a change to a Makefile because of how it accesses "localtime."  The Makefile has a line like this.

        Change this

        .. code-block:: Makefile
        
            ETC_LOCALTIME := $(realpath /etc/localtime)

        to this
        
        .. code-block:: Makefile

            ETC_LOCALTIME := /etc/localtime
        
        A lame explanation:  on a Mac, ``/etc/localtime`` is a link that points to a file ``/usr/share/zoneinfo.default/America/New_York`` that presumably contains the local time.  When Docker tries to create the container, it tries to mount the file on the link, causing problem.  By calling out the link explicitly, the problem is solved.

    .. admonition:: Windows

        If you are on a Windows machine, you will have more success setting up a virtual machine running Ubuntu and then following the instructions above. There are lots of guides for this online.  Here's one: `<https://www.geeksforgeeks.org/how-to-install-ubuntu-on-virtualbox/>`_

    Please let me know of problems, challenges, and **successes**.

5. Complete parts 1 and 2 of the Microkit Tutorial.  Submit a screenshot showing your name in the Wordle table.

    - `<https://trustworthy.systems/projects/microkit/tutorial/>`_

6. Complete parts 3 and 4 of the Microkit Tutorial.  Submit a screenshot showing you having played Wordle.
