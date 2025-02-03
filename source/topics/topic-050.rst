
*************************
Building Systems for seL4
*************************

In this chapter, we are going to work through how to build systems in seL4.  To do this, we are going to use the seL4 Microkit tutorial.  See :ref:`setup-microkit-tutorials` for instructions on how to setup the environment.

The tutorial steps through the process of building a Wordle game.  It proceeds in four parts:

1. A serial server that gets I/O from a UART (universal asynchronous receiver transmitter).  This will let us input letters from the keyboard.
2. A client that manages the letters input from the serial server and prints them to the screen in Wordle format.
3. A Wordle server that interacts with the client to determine which letters are correct, incorrect, or in the wrong position.
4. A virtual machine that communicates via ethernet to get new five-letter words for the game.

In what follows, we give some more insight on the solutions to the tutorial's sub-parts.

Part 1:  Serial Server
======================

.. admonition:: References
 
    - `<https://trustworthy.systems/projects/microkit/tutorial/part1.html>`_
    - You should have a copy of the Microkit manual in the Microkit SDK directory.

System Architecture File
------------------------

The architecture of the system is described in a system-description file.  In this project, it is called ``wordle.system``.  This file is in XML formal.  An example for an imaginary "hello world!" example might look like this.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <system>
        <protection_domain name="hello_world">
            <program_image path="hello_world.elf" />
        </protection_domain>
    </system>

In this system, it creates a protection domain named ``hello_world`` that runs a program called ``hello_world.elf``.  

An **ELF (Executable and Linkable Format)** file is a standard binary format widely used in microkernels and embedded systems for executables, firmware, and dynamic libraries. It efficiently organizes code, data, and metadata into structured sections. ELF supports dynamic and static linking, enabling modularity in microkernel architectures, where components like device drivers and system services run in separate address spaces.  ELF is a preferred format for real-time operating systems (RTOS), embedded firmware, and microcontroller-based applications.

.. note::

    In XML, the difference between > and /> at the end of an element is about whether the element has a closing tag or is self-closing.

    1. > - Standard Opening Tag (Requires a Closing Tag)
	    - Used when the element contains data or child elements.
	    - Requires a separate closing tag (</tag>).

    Example:

    .. code-block:: xml

        <name>John Doe</name>
        <person>
            <age>
                30
            </age>
        </person>

    2. /> - Self-Closing Tag (Empty Element)
	    - Used when the element has no content or children.
	    - Combines the opening and closing tag into one.

    Example:

    .. code-block:: xml

        <image src="photo.jpg" />
        
	When to Use Each?
	    - Use > if the element contains text or children.
	    - Use /> for empty elements.

Protection Domain 
-----------------

Process that run in our system each run in a protection domain.  There is not much a protection domain can do by default --- this is intentional.  We have to explicitly give it capabilities, via seL4's capability system, to access other things.  If a protection domain does not have the capability to access some resource, then seL4 will not allow it to.

For our serial server, this might look like this:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <system>
        <protection_domain name="serial_server" priority="254">
            <program_image path="serial_server.elf" />
        </protection_domain>
    </system>

This will compile the source code in ``serial_server.c`` and make ``serial_server.elf``.  It has problems though.  It wants to start up the UART, but we have not given the serial server the capability to communicate with the UART.

First, let's edit ``serial_server.c`` to make a simple "Hello World!".  In ``serial_server.c`` modify the ``init()`` function as follows.

.. code-block:: c

    void init(void) {
        // First we initialise the UART device, which will write to the
        // device's hardware registers. Which means we need access to
        // the UART device.
        // uart_init();
        // After initialising the UART, print a message to the terminal
        // saying that the serial server has started.
        // uart_put_str("SERIAL SERVER: starting\n");
        printf("Hello World!\n");
    }

Notice that we have commented out the two ``uart_`` functions.  Now, compile and run.

.. code-block:: bash

    /host/tutorial$ make part1
    /host/tutorial$ make run

You should get an output that looks something like this.

.. code-block:: 

    MON|INFO: completed bootstrap invocations
    MON|INFO: completed system invocations
    Hello World!

The microkernel is waiting for more instructions, but none are coming.

Accessing the UART
------------------

By itself, the serial server could do lots of processing, and even output things to the screen using ``printf()``, like we just did.  But, there is no way yet to have in interact with other processes.

The UART is part of the hardware of our system.  As such, there is no other protection domain that needs to be defined by us.  But, we do need to make a memory region to a specific physical address so that we can have access to it.

First we define the memory region 

.. code-block:: xml

    <memory_region name="uart" phys_addr="0x9_000_000" size="0x1000" />

The physical address of the UART is ``0x9000000``.  