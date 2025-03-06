

Part 4:  Virtual Machine
========================

The Wordle game you have so far has 'hello' for the word to guess.  We would like to have a new word to solve each time we plan.  To do this, we need to go to an external server.  To do that, we need an ethernet connection.  And, to realize that we will setup a Linux server in a virtual machine (VM).  The details of how to do this are not part of the tutorial.  The kind people at seL4 Microkit have already set stuff up.  We need to connect to everything in ``wordle.system`` and use the procedure calls when necessary.

Defining the VMM in the System Architecture
-------------------------------------------

The configuration to setup the Linux server and the VMM (virtual machine manager) is below.

.. code-block:: xml

    <!--
        This is what the virtual machine will use as its "RAM".
        Remember it does not know it is a VM and so  will expect a
        block of contigious memory as RAM.
    -->
    <memory_region name="guest_ram" size="0x10000000" page_size="0x200_000"
        phys_addr="0x40000000" />
    <!-- Create a memory region for the ethernet device -->
    <memory_region name="ethernet" size="0x1000" phys_addr="0xa003000" />
    <!--
        Create a memory region for the GIC vCPU, this is part of
        ARM's hardware virtualisation, I will not go into detail here,
        but it is necessary for the virtual machine to function.
    -->
    <memory_region name="gic_vcpu" size="0x1000" phys_addr="0x8040000" />

    <!-- Create a VMM protection domain -->
    <protection_domain name="vmm" priority="101">
        <program_image path="vmm.elf" />
        <!--
            Map in the virtual machine's RAM region as the VMM needs
            access to it as well for starting and setting up the VM.
        -->
        <map mr="guest_ram" vaddr="0x40000000" perms="rw"
            setvar_vaddr="guest_ram_vaddr" />
        <!--
            Create the virtual machine, the `id` is used for the
            VMM to refer to the VM. Similar to channels and IRQs
        -->
        <virtual_machine name="linux" priority="100">
            <vcpu id="0" />
            <map mr="guest_ram" vaddr="0x40000000" perms="rwx" />
            <map mr="ethernet" vaddr="0xa003000" perms="rw" cached="false" />
            <map mr="uart" vaddr="0x9000000" perms="rw" cached="false" />
            <map mr="gic_vcpu" vaddr="0x8010000" perms="rw" cached="false" />
        </virtual_machine>
        <!--
            We want the VMM to receive the ethernet interrupts, which it
            will then deliver to the VM
         -->
        <irq irq="79" id="2" trigger="edge" />
    </protection_domain>
    
    <channel>
        <!-- The VMM code expects the channel ID to be 1. -->
        <end pd="vmm" id="1" />
        <end pd="wordle_server" id="2" />
    </channel>

Let's do our best to break this down.  We will begin at the top.  First, we need to set up some RAM for the virtual machine.  

.. code-block:: xml

    <memory_region name="guest_ram" size="0x10000000" page_size="0x200_000"
        phys_addr="0x40000000" />

We need to do the same for the ethernet device.

.. code-block:: xml

     <memory_region name="ethernet" size="0x1000" phys_addr="0xa003000" />

The virtual machine will issue iterupts, and there needs to be a way to handle them.  A GIC vCPU is a virtual CPU interface within ARM's Generic Interrupt Controller (GIC), enabling efficient interrupt handling in virtualized environments. It allows guest VMs to manage their own interrupts without direct access to the physical GIC. The hypervisor maps virtual interrupts (vIRQs) to physical ones (pIRQs), ensuring proper delivery to vCPUs.  The details of all of this are not important, but we do need to give the GIC vCPU a memory region.

.. code-block:: xml

    <memory_region name="gic_vcpu" size="0x1000" phys_addr="0x8040000" />

Now we setup a protection domain for the VMM.

.. code-block:: xml

    <protection_domain name="vmm" priority="101">
        <program_image path="vmm.elf" />
        <map mr="guest_ram" vaddr="0x40000000" perms="rw"
            setvar_vaddr="guest_ram_vaddr" />
        <virtual_machine name="linux" priority="100">
            <vcpu id="0" />
            <map mr="guest_ram" vaddr="0x40000000" perms="rwx" />
            <map mr="ethernet" vaddr="0xa003000" perms="rw" cached="false" />
            <map mr="uart" vaddr="0x9000000" perms="rw" cached="false" />
            <map mr="gic_vcpu" vaddr="0x8010000" perms="rw" cached="false" />
        </virtual_machine>
        <irq irq="79" id="2" trigger="edge" />
    </protection_domain>

In that we do the following:

- Setup the ``program_image`` that points to ``vmm.elf``.
- Map the ``guest_ram`` memory region to this protection domain.
- Setup the virtual machine ``linux``.  In that they setup
    - The virtual CPU on which the Linux VM will run.
    - Map the ``guest_ram`` memory to be used by the Linux VM.
    - Map the ``ethernet`` memory to be used by the Linux VM.
    - Map the ``uart`` memory.  This gives the Linux VM access to the interrupts created at the hardware level.
    - Map the ``gic_vcpu`` memory so that the Linux VM can handle IRQ as discussed above.
- Include an IRQ in the protection domain.  I don't know what IRQ 79 does.

Finally, we need to setup a channel between the VMM and the Wordle server.

.. code-block:: xml

    <channel>
        <!-- The VMM code expects the channel ID to be 1. -->
        <end pd="vmm" id="1" />
        <end pd="wordle_server" id="2" />
    </channel>

Calling the Protected Procedure Call
------------------------------------

The VMM sets the word deep in ``vmm.c`` (line 141) using

.. code-block:: c

    microkit_msginfo msg = microkit_msginfo_new(0, WORDLE_WORD_SIZE);
    for (int i = 0; i < WORDLE_WORD_SIZE; i++) {
        microkit_mr_set(i, word[i]);
    }
    microkit_ppcall(WORDLE_SERVER_CHANNEL, msg);

Before this spot in its code, it has gotten a new word from the external server and stored it in an array ``char word[WORDLE_WORD_SIZE]``.  In the above piece of code, it creates a new Microkit message and writes each character to the memory register used as part of the protected procedure call.  Then it calls the procedure.

Then, in ``wordle_server.c`` in the ``protected()`` call the Wordle server gets each letter of the word.

.. code-block:: c

    case VMM_CHANNEL:
        for (int i = 0; i < WORD_LENGTH; i++) {
            word[i] = microkit_mr_get(i);
        }
        break;

Now, if you ``make part4`` and ``make run``, you should get a functional Wordle game.  It is missing some things, like the NY Times wordle won't let you enter a word that is not a word in English.  Also, Wordle really gives you six tries not five as in this version.  You can change that though.  You need to do two things.

1.  Change ``NUM_TRIES`` to six in ``wordle.h``. 
2.  When the client displays the table it moves the cursor up five rows.  This is defined in ``client.c`` (line 13 or so) using ``\033[5A``.  The ``5`` needs to be changed to ``6``.

Enjoy.