

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

.. include:: part1.rst

.. include:: part2.rst

.. include:: part3.rst
    