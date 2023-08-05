#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /examples/beakerlib/Sanity/apache
#   Description: Apache example test
#   Author: Petr Splichal <psplicha@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2009 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#@ Sums up phase asserts and reports the overall phase result

# Include the BeakerLib environment
. /usr/share/beakerlib/beakerlib.sh

# Set the full test name
#@@key apache
TEST="/examples/beakerlib/Sanity/apache"

# Package being tested
PACKAGE="httpd"

HttpdPages="/var/www/html"
HttpdLogs="/var/log/httpd"

rlJournalStart
    #@ Sums up phase asserts and reports the overall phase result
    rlPhaseStartSetup "Setup"
        #@ Make sure the httpd package is installed
        rlAssertRpm "httpd"

        # Use rlRun to check the exit status of a command (0 expected here)
        rlRun 'TmpDir=$(mktemp -d)' 0
        pushd $TmpDir

        # Add a comment to make the final report more readable
        rlRun "rlFileBackup --clean $HttpdPages $HttpdLogs" 0 "Backing up"
        rlRun "echo 'Welcome to Test Page!' > $HttpdPages/index.html" 0 \
                "Creating a simple welcome page"

        # Both comment & and exit status can be omitted (expecting success)
        rlRun "rm -f $HttpdLogs/*"

        #@ Make sure the httpd service is running with fresh configuration
        # (restarts if necessary, remembers the original state)
        rlRun "rlServiceStart httpd"
    rlPhaseEnd # Sums up phase asserts and reports the overall phase result
    HttpdPages="/var/www/"

    #@Check if the file is correct
    rlPhaseStartTest "Test Existing Page"
        # @Get the page
        rlRun "wget http://localhost/" 0 "Fetching the welcome page"
        # Check whether the page has been successfully fetched
        rlAssertExists "index.html"
        # Log page content
        rlLog "index.html contains: $(<index.html)"
        #@ Make sure the content is OK
        rlAssertGrep "Welcome to Test Page" "index.html"
        #@ Check the access log for the corresponding record
        rlAssertGrep "GET / HTTP.*200" "$HttpdLogs/access_log"
    rlPhaseEnd
    # FIREFOX_PATH=$( rpm -ql firefox | grep "/usr/lib\(64\)\?/firefox-[^/]\+/firefox" ) #Testing

    #@ Trying to access a nonexistent page
    rlPhaseStartTest "Test Missing Page"
        # Expecting exit code 1 or 8, capture the stderr
        rlRun "wget http://localhost/missing.html 2>stderr" 1,8 \
                "Trying to access a nonexistent page"
        # The file should not be created
        rlAssertNotExists "missing.html"
        #@ An error message should be reported to stderr
        rlAssertGrep "Not Found" "stderr"
        #@ The access log should contain a 404 record
        rlAssertGrep "GET /missing.html HTTP.*404" "$HttpdLogs/access_log"
        # And the error log should describe the problem
        rlAssertGrep "does not exist.*missing.html" "$HttpdLogs/error_log"
    rlPhaseEnd

    #@ Cleanup after test
    rlPhaseStartCleanup "Cleanup"
        popd
        #& Let's clean up all the mess we've made
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"

        #@ Restore the www and log directories to their original state
        rlRun "rlFileRestore"

        #@ Restore httpd service to it's original state
        rlRun "rlServiceRestore httpd"
    rlPhaseEnd
rlJournalEnd

# Print the test report
rlJournalPrintText


