TwitFS
======

Simple Twitter filesystem based on RouteFS, written December 2010

https://blogs.oracle.com/ksplice/entry/building_filesystems_the_way_you

Exposes usernames as directories and status messages of friends as files in these directories.

=== Usage

	$ ./twitfs mnt_dir
	$ ls mnt_dir/
	$ ls mnt_dir/lordmaldy
	$ ls mnt_dir/
	$ cat mnt_dir/lordmaldy/mithileshg
	$ fusermount -u mnt_dir
