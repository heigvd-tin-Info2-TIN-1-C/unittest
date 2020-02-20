#!/usr/bin/env python3

"""

"""

from subprocess import Popen, PIPE, STDOUT
import json
import sys
import getopt


##############################################################
# class cOneTest
class cOneTest:
##############################################################
# __init__ : constructor
# This function creates the test
    def __init__(self, exec, args, input, output, returnCode):
        self.exec=exec
        self.args=args
        self.stdinput=input
        self.stdoutput=output
        self.returnCode=returnCode
        return

##############################################################
# run : constructor
# This function verifies the output and return code of
# ``exec`` within the ``context``.
# inputs: 
#    exec is the name of the executable to run
#    context is the test context (stdin, stdout and error code)
# returns: 2 booleans values
#    outputCorrect (stdout state regarding context)
#    returnCodeCorrect (return code state regarding context)
    def run(self):
        # indicators of correctness
        outputCorrect = True        # for stdout check
        returnCodeCorrect = True    # for return code check

        # add args to the exec list
        for s in self.args:
            self.exec.extend([str(s)])

        # create the stdin input string for the executable 
        i = ''
        b = ''
        for s in self.stdinput:
            i = i + str(s) + '\n'
        b = str.encode(i)

        # exec and grab the stdout and return code outputs
        p = Popen(self.exec, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdoutput = p.communicate(input=b)[0]
        ret = p.returncode
        output = stdoutput.decode()
        output = output.split('\n')

        #print(output)

        # check the output
        outputCorrect = True
        for r in self.stdoutput:
            found = False
            r=r.replace(" ", "")
            for s in output:
                s=s.replace(" ", "")
                if r == s:
                    found = True
            if found == False:
                outputCorrect = False

        # check return code
        returnCodeCorrect=True if ret == self.returnCode else False

        return(outputCorrect, returnCodeCorrect)




##############################################################
# class cAppTest
# This class allow the user to create a test and to run it on
# an application, by using a JSON test file descriptor.
#
class cAppTest:

    def __init__(self,jsonFileName):
        self.jsonFileName=jsonFileName
        # manage json input file
        try:
            with open(self.jsonFileName, 'r') as f:
                self.datastore = json.load(f)
        except BaseException:
            print ('Error, json file [' + self.jsonFileName + '] not found.')
            sys.exit(1)

    def run(self):
        # statistic indicators
        nbTestToDo = 0
        nbTestFailed = 0
        nbTestSuccess = 0

        # do all tests
        execName = self.datastore['exec']
        nbTestToDo = len(self.datastore['test'])

        print('\nRunning #' + str(nbTestToDo) + ' tests...\n')
        for k in range(0, len(self.datastore['test'])):

            testContext=self.datastore['test'][k]
            testToRun=cOneTest([execName], testContext['args'], testContext['stdin'], testContext['stdout'], testContext['returnCode'])
            (outputCorrect, returnCodeCorrect)=testToRun.run()

            failed=True if not outputCorrect or not returnCodeCorrect else False

            nbTestFailed += 1 if failed else 0
            nbTestSuccess += 1 if not failed else 0

            s = 'Test #' + str(k + 1) + ' \"' + testContext['comment'] + '\" :'
            if not outputCorrect:
                s += ' \033[0;33moutput is NOT correct\033[0;37m '
            if not returnCodeCorrect:
                s += ' \033[0;33mreturn code is NOT correct\033[0;37m '
            if failed:
                s += ' => \033[0;31mTEST FAILED.\033[0;37m '
            else:
                s += ' \033[0;32mTEST SUCCESSFUL.\033[0;37m '
            print(s)

        # print the summary
        print('\nSummary:')
        print('\tTest to do: ', nbTestToDo)
        s='\tTest OK:     '
        if nbTestSuccess == nbTestToDo:
            s=s+'\033[1;32m'+str(nbTestSuccess)+'\033[0;37m'
        else:
            s=s+'\033[1;31m'+str(nbTestSuccess)+'\033[0;37m'
        print(s)

        s='\tTest failed: '
        if nbTestFailed == 0:
            s=s+'\033[1;32m'+str(nbTestFailed)+'\033[0;37m'
        else:
            s=s+'\033[1;31m'+str(nbTestFailed)+'\033[0;37m'
        print(s)
    

        if nbTestFailed == 0:
            print("\n\033[1;32m TEST SUCCESSFUL\033[0;37m\n")
        else:
            print("\n\033[1;31m TEST FAILED\033[0;37m\n")

        return



##############################################################
# main(argv):
# This function run some tests on a specified executable
# inputs: 
#   -i filename :  filename contains the tests context
#   -h : give some help regarding the usage
# returns nothing.
def main(argv):

    # statistic indicators
    nbTestToDo = 0
    nbTestFailed = 0
    nbTestSuccess = 0

    # manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Usage: ' + sys.argv[0] + ' -i <inputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ' + sys.argv[0] + ' -i <inputfile> ')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            filename = arg

    appTest=cAppTest(filename)
    appTest.run()



##############################################################
# main(argv):
# This function run some tests on a specified executable
# inputs: 
#   -i filename :  filename contains the tests context
#   -h : give some help regarding the usage
# returns nothing.
def main3(argv):

    # statistic indicators
    nbTestToDo = 0
    nbTestFailed = 0
    nbTestSuccess = 0

    # manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Usage: ' + sys.argv[0] + ' -i <inputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: ' + sys.argv[0] + ' -i <inputfile> ')
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            filename = arg
    print ('Json file for testing is [' + filename + '].')

    # manage json input file
    try:
        with open(filename, 'r') as f:
            datastore = json.load(f)
    except BaseException:
        print ('Error, json file [' + filename + '] not found.')
        sys.exit(1)


    # do all tests
    execName = datastore['exec']
    nbTestToDo = len(datastore['test'])
    print('\nRunning #' + str(nbTestToDo) + ' tests...\n')
    for k in range(0, len(datastore['test'])):


        testContext=datastore['test'][k]
        print(execName)
        print([execName])
        zz=[execName]
        zz.extend('ok')
        print(zz)
        testToRun=cOneTest([execName], testContext['args'], testContext['stdin'], testContext['stdout'], testContext['returnCode'])
        (outputCorrect, returnCodeCorrect)=testToRun.run()


        failed=True if not outputCorrect or not returnCodeCorrect else False

        nbTestFailed += 1 if failed else 0
        nbTestSuccess += 1 if not failed else 0

        s = 'Test #' + str(k + 1) + ' \"' + testContext['comment'] + '\" :'
        if not outputCorrect:
            s += ' \033[0;33moutput is NOT correct\033[0;37m '
        if not returnCodeCorrect:
            s += ' \033[0;33mreturn code is NOT correct\033[0;37m '
        if failed:
            s += ' => \033[0;31mTEST FAILED.\033[0;37m '
        else:
            s += ' \033[0;32mTEST SUCCESSFUL.\033[0;37m '
        print(s)

    # print the summary
    print('\nSummary:')
    print('\tTest to do: ', nbTestToDo)
    s='\tTest OK:     '
    if nbTestSuccess == nbTestToDo:
        s=s+'\033[1;32m'+str(nbTestSuccess)+'\033[0;37m'
    else:
        s=s+'\033[1;31m'+str(nbTestSuccess)+'\033[0;37m'
    print(s)

    s='\tTest failed: '
    if nbTestFailed == 0:
        s=s+'\033[1;32m'+str(nbTestFailed)+'\033[0;37m'
    else:
        s=s+'\033[1;31m'+str(nbTestFailed)+'\033[0;37m'
    print(s)
    

    if nbTestFailed == 0:
        print("\n\033[1;32m TEST SUCCESSFUL\033[0;37m\n")
    else:
        print("\n\033[1;31m TEST FAILED\033[0;37m\n")


if __name__ == "__main__":
    main(sys.argv[1:])
