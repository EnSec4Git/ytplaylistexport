#-------------------------------------------------------------------------------
# Name:        runtests
# Purpose:
#
# Author:      Yavor
#
# Created:
# Copyright:   (c) Yavor
# Licence:     GLPv3
#-------------------------------------------------------------------------------


def run_tests():
    verbosity = 1
    interactive = True
    test_runner = get_runner(settings)
    failures = test_runner([], verbosity=verbosity, interactive=interactive)
    sys.exit(failures)

if __name__ == '__main__':
    run_tests()
