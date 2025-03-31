=================================
Format microSD card on BeagleBone
=================================

Start the BeagleBone Black into its Linux shell (Cloud 9 or similar).

Your user name and password are
- username:  debian
- password:  temppwd

At the prompt, enter this command:

::

   $ sudo fdisk -l

You will get output that looks like this.

::

   debian@beaglebone:/var/lib/cloud9$ sudo fdisk -l
   Disk /dev/mmcblk0: 29.7 GiB, 31914983424 bytes, 62333952 sectors
   Units: sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0x00000000

   Device         Boot Start      End  Sectors  Size Id Type
   /dev/mmcblk0p1       8192 62333951 62325760 29.7G  c W95 FAT32 (LBA)


   Disk /dev/mmcblk1: 3.5 GiB, 3791650816 bytes, 7405568 sectors
   Units: sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disklabel type: dos
   Disk identifier: 0xc014b19c

   Device         Boot Start     End Sectors  Size Id Type
   /dev/mmcblk1p1 *     8192 7405567 7397376  3.5G 83 Linux

This tells you about the various file systems that exist. You don’t want
to mess with ``/dev/mmcblk1`` at all. We are interested in ``/dev/mmcblk0``.

To create Linux partition scheme on the SD card run

::

   $ sudo fdisk /dev/mmcblk0

You need to setup the partition.  You want to do two things:

1. make a new partition
2. toggle the bootable flag

Here is the output, including a listing of all commands (``m``):

::

   Changes will remain in memory only, until you decide to write them.
   Be careful before using the write command.


   Command (m for help): m

   Help:

      DOS (MBR)
         a   toggle a bootable flag
         b   edit nested BSD disklabel
         c   toggle the dos compatibility flag

      Generic
         d   delete a partition
         F   list free unpartitioned space
         l   list known partition types
         n   add a new partition
         p   print the partition table
         t   change a partition type
         v   verify the partition table
         i   print information about a partition

      Misc
         m   print this menu
         u   change display/entry units
         x   extra functionality (experts only)

      Script
         I   load disk layout from sfdisk script file
         O   dump disk layout to sfdisk script file

      Save & Exit
         w   write table to disk and exit
         q   quit without saving changes

      Create a new label
         g   create a new empty GPT partition table
         G   create a new empty SGI (IRIX) partition table
         o   create a new empty DOS partition table
         s   create a new empty Sun partition table


   Command (m for help): n
   Partition type
      p   primary (1 primary, 0 extended, 3 free)
      e   extended (container for logical partitions)
   Select (default p): p
   Partition number (2-4, default 2):
   First sector (2048-62333951, default 2048):
   Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-8191, default 8191):

   Created a new partition 2 of type 'Linux' and of size 3 MiB.

   Command (m for help): a
   Partition number (1,2, default 2):

   The bootable flag on partition 2 is enabled now.

You need to write to disk and exit (``w``).

Now that you have the partition setup, we need to make the disk.

::

   $ sudo mkfs.ext4 -O ^metadata_csum /dev/mmcblk0p1

The command ``mkfs.ext4`` formats the partition in ext4 format. The
``-O ^metadata_csum`` flag prevents it from creating the
``metadata_csum`` flag, which would cause problems later on.

Finally, we need to create a boot directory.

Create a place to mount the disk.

::

   $ sudo mkdir /media/mysdcard

Now mount the disk.

::

   $ sudo mount /dev/mmcblk0p1 /media/mysdcard

You should now be able to look at the contents of the disk.

::

   $ ls -la /media/mysdcard

.. which give this

..    Output 

Now make a directory called ``/media/mysdcard/boot``.

::

   $ sudo mkdir /media/mysdcard/boot

You can now unmount the SD card.

::

   $ sudo umount /media/mysdcard 

It's ready to roll!
