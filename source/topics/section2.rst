


Part 2:  Client
===============

Client Protection Domain
------------------------

Make the protection domain for the client.  This should start out just like the one we did for the serial server.  The only change we will make will be to lower the priority to 253.

.. code-block:: xml

    <protection_domain name="client" priority="253">
        <program_image path="client.elf" />
    </protection_domain>

Channel
-------

Channels allow protection domains to communicate two ways:

1. Notifications and the ``notified()`` function
2. Protected procedures and the ``protected()`` function. (discussed in a later part.)

Notifications are asynchronous and bidirectional.  An **asynchronous channel** allows communication without a synchronized clock. Data can be sent at any time, and the receiver processes it upon arrival. The sender and receiver operate independently, with synchronization handled via start/stop signals, timestamps, or protocols.  A **bidirectional channel** enables data flow in both directions. It supports both sending and receiving.

Let's make the channel from the server to the client.

.. code-block:: xml

    <channel>
        <end pd="client" id="1" />
        <end pd="serial_server" id="2" />
    </channel>

The channel ID can be different for the two ends of the channel.  The client will refer to this channel as channel 1.  The serial server will refer to this channel as 2.  Of course for the serial server, we already have used ``id="1"`` for the IRQ 33 from the UART.

Notifications can go both ways.

- ``serial_server`` → ``client``
- ``client`` → ``serial_server``

We need to tell both procedures what to do when they receive a notification.

For the serial server (``serial_server.c``), we need to handle notification on channel 1 and 2.  We will define these channels with preprocessor directives.  In the ``notified()`` function, we will create a switch to handle notifications from the two channels.

1. **IRQ**:  As before, we will get and the character.  I have added a line that puts a newline so that screen formatting will be nice.  Then we notify the client on channel 2.  Finally, we handle the IRQ with the UART and acknowledge the IRQ with seL4.
2. **From the client**:  When we are notified by the client, we will simply print that we have been notified and display the channel.

.. code-block:: c

    #define UART_IRQ_CH 1
    #define CLIENT_CH 2

    #define NEWLINE 0x0A

    void notified(microkit_channel channel) {
        switch (channel) {
            case UART_IRQ_CH: {
                int character = uart_get_char();
                uart_put_char(character);
                uart_put_char(NEWLINE);
                microkit_notify(CLIENT_CH);
                uart_handle_irq();
                microkit_irq_ack(UART_IRQ_CH);
                break;
            }
            case CLIENT_CH:
                printf(" SERVER: notified on channel %d\n",channel);
                break;
        }
    }


For the client (``client.c``), we only need to handle notification in channel 1.  We will use the same switch structure since that allows us to more easily, in the future, if we need to, add other channels.

When we receive a notification on channel 1, we will simply print that we have been notified.  Then, we will send a notification back to the serial server on the same channel.  (No particular need to do this other than to show we can do it.)  Finally, we will print that we have sent a notify on the channel.

.. code-block:: c

    #define SERIAL_CHANNEL 1

    void notified(microkit_channel channel) {
        switch (channel) {
            case SERIAL_CHANNEL:
                printf("CLIENT: notified on channel %d\n", channel);
                microkit_notify(channel);
                printf("CLIENT: sent notify on channel %d\n", channel);
        }
    }

Now, ``make part2 run`` and you should get something like this when you type ``P``.

.. code-block:: 

    ERIAL SERVER: starting
    CLIENT: starting
    P
    CLIENT: notified on channel 1
    SERVER: notified on channel 2
    CLIENT: sent notify on channel 1

Notice that even though we print ``CLIENT: sent ...`` in the clients ``notified()`` function, it happens after the server has printed ``SERVER: notified ...``.  This is because the server is higher priority.  When we notify the server, seL4 gives it priority over the client.  As such, it gets the notification, handles it, which means it prints.  When the server reaches the end of its ``notified()`` function, it stops, and priority passes to the client, which then finishes its ``notified()`` function.

Shared Buffer
-------------

We want to be able to share data between the server and the client.  We want to be able to do this in both directions without writing the same place in memory.  To do this, first we need to define two the memory regions:

1. From the serial server to the client.
2. From the client to the serial server.

Of course, we do this in the ``wordle.system`` file.

.. code-block:: xml

    <memory_region name="serial_to_client" size="0x1000" />
    <memory_region name="client_to_serial" size="0x1000" />

Both regions in memory are the same size at 4 KiB (4096 B).

Next, we have to map this memory region to the two protection domains.

In the ``serial_server`` protection domain:

.. code-block:: xml

    <map mr="serial_to_client" vaddr="0x4_000_000" perms="rw" setvar_vaddr="serial_to_client_vaddr" />
    <map mr="client_to_serial" vaddr="0x4_001_000" perms="r" setvar_vaddr="client_to_serial_vaddr" />

In the ``client`` protection domain:

.. code-block:: xml

    <map mr="serial_to_client" vaddr="0x4_000_000" perms="r" setvar_vaddr="serial_to_client_vaddr" />
    <map mr="client_to_serial" vaddr="0x4_001_000" perms="rw" setvar_vaddr="client_to_serial_vaddr" />

In both cases, the serial-to-client virtual addres is ``0x4000000`` and the client-to-serial virtual address is ``0x1000`` bytes above that.  

Importantly, the variables ``serial_to_client_vaddr`` and ``client_to_serial_vaddr`` have been defined.  

Sharing Data from the Server to the Client
------------------------------------------

When we implement the above architecture, we have two variables ``serial_to_client_vaddr`` and ``client_to_serial_vaddr`` that need to be defined.  In both ``serial-server.c`` and ``client.c`` we add the following:

.. code-block:: c

    uintptr_t serial_to_client_vaddr;
    uintptr_t client_to_serial_vaddr;

- ``uintptr_t`` is an unsigned integer type capable of holding a pointer's value.
- It is defined in ``<stdint.h>`` and guarantees to be large enough to store memory addresses.
- It is often use dwhen you need to star a pointer but operate on it as an integer.

The two variables are 

- ``serial_to_client_vaddr`` holds the virtual address used to communicate from the serial server to the client.
- ``client_to_serial_vaddr`` holds the virtual address used to communicate from the client to the serial server.

Now, we need to think more about how we want Wordle to work.  As before, we have two channels that notifications come from.

1. **IRQ**:  When we get an IRQ from the UART, we do what we did before.
    - Get the character.  Now though, instead of putting that in an integer, we store it in the first byte of ``serial_to_client``.  That way, it will be available for the client to do something with.
    - We handle the IRQ with the UART.
    - We acknowledge the IRQ with seL4.
    - We notify the client that there is a new character.
2. **From the client**:  Presumably the client has done something with the data we have given it.  That is stored in ``client_to_serial``.  We pass this (as ``char *``) to ``uart_put_str``.

Code to do all of this might look like this:

.. code-block:: c

    #define UART_IRQ_CH 1
    #define CLIENT_CH 2

    uintptr_t serial_to_client_vaddr;
    uintptr_t client_to_serial_vaddr;

    void notified(microkit_channel channel) {
        switch (channel) {
            case UART_IRQ_CH:
                ((char *)serial_to_client_vaddr)[0] = uart_get_char();
                uart_handle_irq();
                microkit_irq_ack(channel);
                microkit_notify(CLIENT_CH);
                break;
            case CLIENT_CH:
                uart_put_str((char *)client_to_serial_vaddr);
                break;
        }
    }

There is one significant change here.  When we get the character from the UART, we store it in ``((char *)serial_to_client_vaddr)[0]``.  Here's a breakdown.

- The address of the ``serial_to_client`` memory region is stored in ``serial_to_client_vaddr``.  This is type ``uintptr_t``, which is type unsigned integer but is long enough to ensure you can store an address.
- They cast this address as a character pointer using ``(char *)``.  That is, they make a character pointer.  This charater pointer has the address identified by ``serial_to_client_vaddr``.  Recall that was the virtual address ``0x4000000``, which we defined in ``wordle.system``.
- This is useful because we can access the character pointer byte by byte.  By casting ``serial_to_client_vaddr`` as a ``char *`` you can write to anyone of the 4 bytes.  ``((char *)serial_to_client)[0]`` puts that in the first byte.

On the client end, we need to do something when the serial server notifies us.  This happens in the ``notified()`` function of ``client.c``.  There are three things that need to do

1. Put the character stored at ``serial_to_client_vaddr`` in a ``char`` variable.
2. Add that character to the table of characters we are collecting.  There is already a function to do this.
3. Print the table.

.. code-block:: c

    char ch = ((char *)serial_to_client_vaddr)[0];
    add_char_to_table(ch);
    print_table(true);

The input to the ``print_table()`` function is a ``bool``.  If it is ``true`` then the "screen is cleared".  We do this if a wordle table has already been printed.  If it is ``false``, then the screen is not cleared. 

Incidentially, if you look at the solution, you will see that they wrap the above code in a ``switch``, but there is only one ``case``.  This is presumably to be able to handle other channels if the system ever needed it.  

We still need to send the table we have made back to the serial server.  This is done inside the ``print_table()`` function using the ``serial_send()`` function.  We have to write this function.

.. code-block:: c

    void serial_send(char *str) {
        // Implement this function to get the serial server to print the string.
        int i = 0;
        while (str[i] != '\0') {
            ((char *)client_to_serial_vaddr)[i] = str[i];
            i++;
        }
        ((char *)client_to_serial_vaddr)[i] = '\0';
        microkit_notify(SERIAL_CHANNEL);
    }

Here is what this does.  The input to the function is a string.  We step along the string, byte by byte and put those characters in a corresponding location of a ``char *`` at the location defined in ``client_to_serial_vaddr``.  That is we write the values of the string to the client to serial server buffer.  When we get to the end of the string, we put one more character, ``\0``, the null character, which marks the end of string.  Finally, we notify the serial server we have done writing.

Doing all of this, you should be able to get an output that looks like this.

.. code-block:: 

    SERIAL SERVER: starting
    CLIENT: starting
    Welcome to the Wordle client!
    [a] [b] [c] [d] [e] 
    [f] [g] [h] [i] [j] 
    [ ] [ ] [ ] [ ] [ ] 
    [ ] [ ] [ ] [ ] [ ] 
    [ ] [ ] [ ] [ ] [ ] 

You can backspace if necessary, and need to press ``Enter`` to go to a new line.