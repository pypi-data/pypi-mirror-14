#!/bin/bash
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   #@ does nothing at all ?
#
# this test is completely useless
#
#	there seems to be no description whatsoever :F
#	still none
#
#   no author exists
# 
# yet it is copyrighted
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

# Include the BeakerLib environment
. /usr/share/beakerlib/beakerlib.sh

# Set the full test name
#@ key sthsth # should not make a key

rlJournalStart

    rlPhaseStartSetup "Setup"
	# does nothing
    rlPhaseEnd

# some trailing puppies

    #@ Cleanup after test

    rlPhaseStartCleanup "Cleanup"
	#@ we better clean up after doing nothing
    rlPhaseEnd

rlJournalEnd





