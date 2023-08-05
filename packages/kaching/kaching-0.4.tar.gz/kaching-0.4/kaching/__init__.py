def _play_sound_file(sound_file):
    """Play specified sound file or raise error if mplayer doesn't work."""
    from subprocess import Popen, PIPE
    from sys import stderr, exit

    try:
        Popen(["mplayer", "-msglevel", "all=-1", sound_file], stdout=PIPE, stderr=PIPE)
    except OSError:
        stderr.write("Couldn't run mplayer. Do you have it installed?\n")
        exit(1)

def _print_usage():
    """Print CLI usage."""
    from sys import stderr, exit
    stderr.write("Usage: kaching [pass | fail | start]\n")
    exit(1)
    
def _play_random_file_in_dir(directory):
    """Play random file in one of the included directories."""
    from random import randint
    from os.path import join, dirname, realpath
    from os import listdir
    
    full_dir = join(dirname(realpath(__file__)), directory)
    all_files = listdir(full_dir)
    _play_sound_file(join(full_dir, all_files[randint(0, len(all_files) - 1)]))
    

def win():
    """Play a happy test passing sound."""
    _play_random_file_in_dir("pass")


def fail():
    """Play a test failing sound."""
    _play_random_file_in_dir("fail")


def start():
    """Play a test starting sound."""
    _play_random_file_in_dir("start")


def commandline():
    """Run kaching via commandline."""
    from sys import argv
    
    if len(argv) == 2:
        if argv[1] == "win":
            win()
        elif argv[1] == "pass":
            win()
        elif argv[1] == "fail":
            fail()
        elif argv[1] == "start":
            start()
        else:
            _print_usage()
    else:
        _print_usage()
