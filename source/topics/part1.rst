

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

    1. ``>`` --- Standard Opening Tag (Requires a Closing Tag)
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

    2. ``/>`` --- Self-Closing Tag (Empty Element)
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
        printf("Hello World!\n");
    }

Now, compile and run.

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

The UART is part of the hardware of our system.  As such, there is no other protection domain that needs to be defined by us.  But, we do need to do three things to get this to work.

1.  We need to initialize the UART.
2.  We need to setup some a way to send data (characters) to/from the UART
3.  We need to be able to handle interrupts that happen when we type on the keyboard.

Initializing the UART
^^^^^^^^^^^^^^^^^^^^^

First, you want to fix the ``init()`` function.

.. code-block:: c

    void init(void) {
        uart_init();
        uart_put_str("SERIAL SERVER: starting\n");
    }

What does ``uart_init()`` do?  The key parts its definition are

.. code-block:: c

    #define UARTIMSC 0x038

    #define REG_PTR(base, offset) ((volatile uint32_t *)((base) + (offset)))

    void uart_init() {
        *REG_PTR(uart_base_vaddr, UARTIMSC) = 0x50;
    }

This code is configuring a UART (Universal Asynchronous Receiver-Transmitter) module, specifically setting the Interrupt Mask Set/Clear Register (IMSC) to 0x50. 

Let's break this down.

.. code-block:: c

    #define UARTIMSC 0x038

- This defines ``UARTIMSC`` as the offset 0x038, which corresponds to the Interrupt Mask Set/Clear Register in a typical ARM PL011 UART.
- This register is used to enable or disable specific UART interrupts.

.. code-block:: c

    #define REG_PTR(base, offset) ((volatile uint32_t *)((base) + (offset)))

- This macro computes a pointer to a hardware register.
- ``(base) + (offset)``: Computes the address of a specific register within a memory-mapped device.
- ``(volatile uint32_t *)``: Casts it to a volatile 32-bit pointer.
- ``volatile`` ensures that the compiler does not optimize away reads/writes.
- ``uint32_t *`` treats it as a pointer to a 32-bit register.

.. code-block:: c

    void uart_init() {
        *REG_PTR(uart_base_vaddr, UARTIMSC) = 0x50;
    }

This computes the address of the register and writes 0x50 to that address.

What Does 0x50 (Binary 0101 0000) Do?

- In ARM PL011 UART, ``UARTIMSC`` is used to enable/disable interrupts.
- Bits of ``UARTIMSC``:

    - Bit 4 (0x10 → 0001 0000): RXIM → Enable Receive Interrupt.
    - Bit 6 (0x40 → 0100 0000): RTIM → Enable Receive Timeout Interrupt.

- Setting ``UARTIMSC = 0x50`` (binary 0101 0000):
    
    - Enables Receive Timeout Interrupt (RTIM)
    - Enables Receive Interrupt (RXIM)

Final Explanation

1.	``REG_PTR()`` computes a pointer to a register at a given offset.
2.	``uart_init()`` writes 0x50 to ``UARTIMSC``, enabling RX and Timeout interrupts.
3.	This ensures the UART generates interrupts when data is received or if there is a timeout waiting for data.

Interrupt Requests (IRQ)
^^^^^^^^^^^^^^^^^^^^^^^^

Now we need let the protection domain know about the IRQ and write code to handle them.

We add this to the serial server protection domain:

.. code-block:: xml

    <irq irq="33" id="1" />

- ``irq = "33"`` is the interrupt number.  For QEMU, the IRQ number is 33.

When an IRQ occurs, for example after we type something in the keyboard, we need to handle the IRQ.  This happens with the ``notified()`` entry point.  When this function is called we are going to do four things:

1. Get the character that was typed from the UART.
2. Put the character back to the UART to show on the screen.
3. We need to have the UART handle the interrupt on its end.
4. We let seL4 know we have handled the IRQ and are ready for more interrupts.

The code to do these things might look like this.

.. code-block:: c

    void notified(microkit_channel channel) {
        int character = uart_get_char();
        uart_put_char(character)
        uart_handle_irq();
        microkit_irq_ack(1);    
    }

These do the following:

- ``uart_get_char()`` get the character that was just typed.  The output of this function is an integer, which we store in the ``character`` variable.  
- ``uart_put_char()`` this puts the character to the screen.  You could have also used ``printf("%d",character)``, which does the same thing.
- ``uart_handle_irq()`` tells the driver to handle the request.
- ``microkit_irq_ack()`` tells seL4 that are finished handling the IRQ and are ready for another one.  Without this, seL4 would not send another IRQ.

Memory Regions
^^^^^^^^^^^^^^

Send data to/from the UART we need to setup a channel.  The memory address is already part of the UART, so we need to tell the system where it is, and we need to tell the serial server protection domain abou it.

First we define the memory region 

.. code-block:: xml

    <memory_region name="uart" phys_addr="0x9_000_000" size="0x1000" />

The physical address of the UART is ``0x9000000``.  Finding this and other information can be done different ways, but one that is fairly easy is to inspect the Device Tree Source.  When you do that, you get an entry that looks like this:

.. code-block::  

    pl011@9000000 {
		clock-names = "uartclk", "apb_pclk";
		clocks = <0x8000 0x8000>;
		interrupts = <0x00 0x01 0x04>;
		reg = <0x00 0x9000000 0x00 0x1000>;
		compatible = "arm,pl011", "arm,primecell";
	};

This is a Device Tree (DTS) node describing a PL011 UART (ARM PrimeCell UART) hardware peripheral.  Breaking this down:

1. Node Name: ``pl011@9000000``
    - ``pl011``: Name of the hardware block (PL011 UART).
    - ``@9000000``: The base address of the UART hardware in memory (0x9000000).

2. clock-names and clocks

    - ``clock-names``: Lists the clock sources for this UART.
        - ``"uartclk"`` → The main UART clock.
        - ``"apb_pclk"`` → The APB (Advanced Peripheral Bus) clock.
    - ``clocks``: Specifies the clock source handles or identifiers.
    - ``<0x8000 0x8000>`` refers to hardware clock sources (exact interpretation depends on the system).

3. interrupts

    - Describes the interrupt settings for the UART.
    - ``<0x00 0x01 0x04>``
    
        - ``0x00``: Interrupt controller number (e.g., first interrupt controller).
        - ``0x01``: IRQ number (e.g., assigned interrupt line).
        - ``0x04``: Interrupt trigger type.
        - ``0x04`` usually means level-sensitive, active-high in GIC (ARM Generic Interrupt Controller).

4. reg (Register Address and Size)

    - Defines the memory-mapped address range for the UART registers.
    - ``<0x00 0x9000000 0x00 0x1000>``

        - Base address: ``0x9000000``
        - Size: ``0x1000`` (4 KiB)
        - This means the UART hardware registers are mapped at ``0x9000000`` to ``0x9000FFF``.

5. compatible (Device Compatibility)

    - Defines compatibility with drivers in the Linux kernel.
    - ``"arm,pl011"`` → Refers to the ARM PL011 UART.
    - ``"arm,primecell"`` → Refers to ARM PrimeCell peripherals (generic ARM devices).

This setup is typically found in ARM-based SoCs used in embedded systems (e.g., Linux on Raspberry Pi, QEMU, or ARM development boards).

Now we want to map that memory region to the serial server's protection domain. 

.. code-block:: xml

    <protection_domain name="serial_server" priority="254">
        <program_image path="serial_server.elf" />
        <map mr="uart" vaddr="0x2000000" perms="rw" cached="false" 
            setvar_vaddr="uart_base_vaddr"/>
    </protection_domain>

- ``mr`` is the memory region (defined above) that is being mapped to.
- ``vaddr`` is the virtual address forthe mapped memory region. 
- ``perms`` are the permissions for the region.  The options are ``r`` (read), ``w`` (write), and ``x`` (execute).  We have set it to ``rw`` so we can both read and write to the memory.
- ``cached`` determines if caching is enabled.  It defaults to true.  We've set it to false.
- ``setvar_vaddr`` is a symbol that gets used in the program image.

With all of this the protection domain now looks like this:

.. code-block:: xml

    <protection_domain name="serial_server" priority="254">
        <program_image path="serial_server.elf" />
        <map mr="uart" vaddr="0x2000000" perms="rw" cached="false" 
            setvar_vaddr="uart_base_vaddr"/>
        <irq irq="33" id="1" />
    </protection_domain>

and ``serial_server.c`` looks like this:

.. code-block:: c

    void init(void) {
    uart_init();
    uart_put_str("SERIAL SERVER: starting\n");
    }

    void notified(microkit_channel channel) {
        int character = uart_get_char();
        uart_put_char(character);
        uart_handle_irq();
        microkit_irq_ack(1);
    }

Now when you build and run (``make part1 run``) you should be able to type on the keyboard and see the result on the screen.