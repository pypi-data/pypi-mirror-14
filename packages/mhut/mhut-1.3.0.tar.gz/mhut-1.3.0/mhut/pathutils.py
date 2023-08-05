#!/usr/bin/env python
"""Author : Mahmud Hassan
   Purpose: Automates common shell functions for env variables
   Usage  : path_utils.py <cmd> [args]
            where <cmd> is one of: 'add', 'remove', 'clean', or 'list'
            and [args] specify the paths, or optionally the
            environment variable as follows: 

               path_utils.py add    [env var] <path 1> <path 2> ... <path N> 
               path_utils.py remove [env var] <path 1> <path 2> ... <path N> 
               path_utils.py clean  [env var] 
               path_utils.py list   [env var] 

            if 'env var' is not specified the commands apply to
            PATH by default. 'env var' may be upper case or lower case.

"""

import sys
import os





# **********************************************************
# Begin class definition for Env
# **********************************************************

class Env:
    """Object for environment variable. Can perform operations such as
    add, clean, remove or list paths for that object"""

    def __init__(self, name):
        """Creates & initiliazes env var object along with path list"""
        self.name = name
        self.val = os.getenv(name)
        if self.val != None:
            self.path_list = self.val.split(':')
        else:
            os.environ[name] = name  # create a new env variable 
            self.path_list = []


    def padd(self, path, pos=0):
        """Inserts path into current variable - into beginning(0) by default
        but could be at end (-1) or any other position"""
        path = os.path.normpath(path)           # remove double slashes and stuff
        if path in self.path_list:
            print path, "already exists. Not appending to ", self.name
        elif os.path.exists(path):
            self.path_list.insert(pos, path)
        else:
            print path, "does not exist! Not appending to ", self.name
            return
        self.pupdate()


    def plist(self):
        """Just lists out paths in env variable, one per line"""
        if self.val == None:
            print "No such env variable ", self.val, " exists!"
        else:
            print "Listing for ", self.name
            for p in self.path_list: print "  ", p


    def pclean(self):
        """Cleans up path to remove dead directories, duplicates, etc."""
        path_list_pruned = []
        for p in self.path_list:
            if not os.path.exists(p):
                print "Does not exist! ", p
            elif p in path_list_pruned:
                print "Duplicate found ", p
            else:
                p = os.path.normpath(p)       # remove double slashes and stuff
                path_list_pruned.append(p)

        self.path_list = path_list_pruned
        self.pupdate()


    def premove(self, path):
        """Removes all occurences of path from env variable"""
        path = os.path.normpath(path)       # remove double slashes and stuff
        if path not in self.path_list:
            print "Not found in path list! ", path
        else:
            print "Removing ", path, " from env var ", self.name 
            while path in self.path_list:    # needed just in case path is not cleaned first
                self.path_list.remove(path)
            self.pupdate()


    def pupdate(self):
        """Updates the internal env val to ensure path_list & val are insync"""
        try:
            tmp = self.path_list[0]
        except IndexError:
            print "Empty value for env variable ", self.name
            return

        for p in self.path_list[1:]:
            tmp = tmp + ':' + p
        self.val = tmp


    def pwrite(self):
        """Writes out sanitized or new path list to file for sourcing"""
        shell = os.getenv('SHELL') 
        if shell == None:   # assume bash or ksh
            shell = 'bash'
        else:
            shell = os.path.basename(shell)

        fname = '/tmp/source_' +  os.environ['USER']   # get login id of current user
        try:
            fid = open(fname, 'w')
        except:
            print "ERROR. Could not open ", fname, " for writing! Exiting..."
            exit(1)

        if self.val == None:
            self.val = ""

        if 'csh' in shell:
            wstr = "setenv " + self.name + " " + self.val
        else:
            wstr = "export " + self.name + "=" + self.val

        fid.write(wstr)
        fid.close()
        print "Source ", fname, " for new path to take effect"

# **********************************************************
# End of class definition for Env
# **********************************************************



def usage(s=None):
    if s != None:
        print s
    print __doc__
    exit()



#TODO: fix this so that errors in one or paths in list of paths is 
# handled more appropriately, eg, if only one non-existent path to
# be added should not attempt to write to tmp file
def execute(cmd, var, args):
    """Executes one of only 4 real commands: add, clean, remove or list
    on an environment variable. Assume arguments have been sanitized"""
    env_obj = Env(var)

    if 'list' in cmd:
        env_obj.plist()
    elif 'clean' in cmd:
        env_obj.pclean()
        env_obj.pwrite()
    elif 'add' in cmd:
        for path in args: env_obj.padd(path)
        env_obj.pwrite()
    elif 'remove' in cmd:
        for path in args: env_obj.premove(path)
        env_obj.pwrite()
    else:
        usage("Some really weird error occured. Check program inputs & try again!")



def process_options(args):
    """Process options based on legal operations & subcommands
    Return sanitized cmds and arguments"""
    subcmds = dict()   # each key(cmd) can take on a val of 0, or 1 
    subcmds_wo_arg = [ 'clean', 'list' ]
    subcmds_with_args = [ 'add', 'remove' ]

    for cmd in subcmds_wo_arg:
        subcmds[cmd] = 0
    for cmd in subcmds_with_args:
        subcmds[cmd] = 1

    if (len(args) == 0):
        usage("ERROR. must have one sub-command available")

    cmd = args.pop(0)
    argc = len(args)

    def bad_args(cmd, argc):
        return True if argc < subcmds[cmd] else False

    env_var = '' 
    # determine what kind of cmd was given and arguments
    if cmd not in subcmds:
        usage("ERROR. Unrecognized cmd " + cmd + "! cmd must be from appropriate list")
    elif bad_args(cmd, argc):
        usage("Must enter at least one argument for " + cmd)
    elif argc > subcmds[cmd]:          # determine if it defaults to PATH or anything else
       if os.getenv(args[0]) != None: 
            env_var = args.pop(0)      
       elif os.getenv(args[0].upper()) != None: 
            env_var = args.pop(0).upper() 
       else: # first argument is NOT a known env variable 
          if (cmd == 'remove'): 
             env_var = 'PATH' 
          elif (cmd == 'add') and  ('/' not in args[0]) and (len(args) > 1):  # not like a path & has at least one other argument
               env_var = args.pop(0)      # assume new env variable to be created 
          else:
               usage("Unrecognized environment variable " + args[0])
    else:
        env_var = 'PATH'

    return (cmd, env_var, args)


def test():
    """Tests out operation of utils with sample commands and strings"""
    # usage()
    path_obj = Env('PATH')
    path_obj.pclean()
    path_obj.padd('/home/mahmud/downloads///')
    path_obj.padd('/home/mahmud/apps//', -1)
    path_obj.premove('/abcd')
    path_obj.premove('/cad/tools/platform/lsf/7.0/linux2.6-glibc2.3-x86_64/etc')
    path_obj.premove('/cad/tools/platform/lsf/7.0/linux2.6-glibc2.3-x86_64/bin')
    path_obj.plist()
    cmd = 'add /usr/bin/'
    cmd = 'clean abcd'
    cmd = 'ld_clean'
    cmd = 'lic_add /bin /tmp'
    cmd = ''
    cmd = 'env_remove CADENCE_PATH /some/arbitrary/dir'
    cmd = 'env_list CADENCE_PATH'
    cmd = 'ld_remove /cad/tools/cliosoft/sos_5.31_linux/lib    /cad/tools/cadence/soc/SOC71/tools/lib'
    (cmd, var, args) = process_options(cmd.split())
    print "Executing: ", cmd, var, args
    execute (cmd, var, args)


def main():
    """Handle argument options, create env object, and perform operations"""
    sys.argv.pop(0)
    (cmd, var, args) = process_options(sys.argv[:])
    execute(cmd, var, args)


if __name__ == '__main__':
    if (len(sys.argv) > 1) and (sys.argv[1] == "test"):  
       test()
    else:
       main()


