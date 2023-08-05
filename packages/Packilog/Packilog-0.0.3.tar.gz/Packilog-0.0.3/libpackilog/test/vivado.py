import subprocess


def check():
    ''' Returns True if test can be ran '''
    try:
        subprocess.check_output(['which', 'xvlog'])
        subprocess.check_output(['which', 'xelab'])
        subprocess.check_output(['which', 'xsim'])
    except:
        return False

    return True


def build():
    ''' Performs build step '''
    print "Building tests."
    subprocess.check_output(['xvlog --sv *.sv tests/*.sv'],
                            shell=True)


def test(test_top):
    ''' Runs the test '''
    print "Simulating test module '{0}'.".format(test_top)
    test_result = True
    subprocess.check_output(['xelab', test_top])
    try:
        results = subprocess.check_output(['xsim', '-R', test_top])
        for line in results.split('\n'):
            print line
            if line.startswith('Error: '):
                test_result = False
    except Exception as err:
        print "Exception hit when running test: {0}".format(err)
    return test_result


def cleanup():
    ''' Cleans up files from tests '''
    subprocess.check_output(['rm -r webtalk*.log webtalk*.jou xsim*.jou ' +
                             'xsim*.log xvlog.log xvlog.pb xsim.dir ' +
                             'xelab.log xelab.pb'],
                            shell=True)
