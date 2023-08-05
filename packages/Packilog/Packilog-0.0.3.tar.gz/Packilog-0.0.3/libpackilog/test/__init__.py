import vivado
import sys

test_drivers = {'vivado': vivado}

def test_package(manifest):
    ''' Runs tests in the package '''
    if 'tests' not in manifest:
        print "No tests in manifest"
        return False

    if 'test_driver' in manifest:
        driver = test_drivers[mainfest['test_driver']]
    else:
        for drivername, test_driver in test_drivers.iteritems():
            if test_driver.check():
                driver = test_driver
                print "Using {0} testing driver".format(drivername)

    driver.build()

    package_passed = True
    for test in manifest['tests']:
        if not run_test(driver, test):
            package_passed = False

    if package_passed:
        driver.cleanup()

    return package_passed


def run_test(driver, test):
    print 'Running test module "{0}"'.format(test)
    if driver.test(test):
        print "Result: PASS"
        return True
    else:
        print "Result: FAIL"
        return False
