import os


def check_is_file_valid(fname):
    try:
        open(fname, 'w').close()
        os.unlink(fname)
        return True
    except OSError:
        return False
    except IOError:
        return False