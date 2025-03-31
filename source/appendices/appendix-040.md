Start the BeagleBone Black into its Linux shell (Cloud 9 or similar).

At the prompt, enter this command:
```
$ sudo fdisk -l
```
You will get output that looks like this.
```
Output output output
```
This tells you about the various file systems that exist.  You don't want to mess with `/dev/mmcblk1` at all.  We are interested in `/dev/mmcblk0`.  

To create Linux partition scheme on the SD card run
```
$ sudo fdisk /dev/mmcblk0
```
It will ask you some questions.  Important among these are
```
This one, and
This other one
```

Now that you have the partition setup, we need to make the disk.  
```
$ sudo mkfs.ext4 -O ^metadata_csum /dev/mmcblk0p1
```
The command `mkfs.ext4` formats the partition in ext4 format. 
The `-O ^metadata_csum` flag prevents it from creating the `metadata_csum` flag, which would cause problems later on.

Finally, we need to create a boot directory.  

Create a place to mount the disk.
```
$ sudo mkdir /media/mysdcard
```
Now mount the disk.
```
$ sudo mount /dev/mmcblk0p1 /media/mysdcard
```
You should now be able to look at the contents of the disk.
```
$ ls -la /media/mysdcard
```
which give this
```
Output 
```
Now make a directory called `/media/mysdcard/boot`.
```
$ sudo mkdir /media/mysdcard/boot
```
You can no unmount the SD card. 
```
$ sudo umount /media/mysdcard 
```
It's ready to roll!