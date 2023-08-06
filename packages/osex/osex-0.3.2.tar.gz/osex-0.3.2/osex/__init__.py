import os
import sys

def append_to_name(source_path, suffix):
    dest_path_prefix = source_path + suffix
    dest_path = dest_path_prefix
    dest_index = 0
    while os.path.lexists(dest_path):
        dest_index += 1
        dest_path = dest_path_prefix + str(dest_index)
    os.rename(source_path, dest_path)

def renames(source, destination, override = True, backup = False, backup_suffix = "~"):
    if os.path.exists(destination):
        if override:
            if backup:
                append_to_name(destination, backup_suffix)
            elif os.path.isdir(destination) and not os.path.islink(destination):
                raise OSError("may not override directory '%s'" % destination)
        else:
            raise OSError("path '%s' already exists" % destination)
    os.renames(source, destination)

def symlink(source, link_name, relative = False, override = False, backup = True, backup_suffix = "~"):
    if relative:
        source = os.path.relpath(source, os.path.dirname(link_name))
    # os.path.lexists() returns True if path refers to an existing path and 
    # True for broken symbolic links. 
    if not os.path.lexists(link_name):
        os.symlink(source, link_name)
    elif not os.path.islink(link_name) or os.readlink(link_name) != source:
        if override:
            if backup:
                append_to_name(link_name, backup_suffix)
            else:
                if os.path.isdir(link_name):
                    os.rmdir(link_name)
                else:
                    os.remove(link_name)
            os.symlink(source, link_name)
        else:
            raise OSError("link's path '%s' already exists." % link_name)
