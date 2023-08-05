# #######################################################
#                                                       #
# gtimes library and timecalc.py modules                #
# installation instructions                             #
#                                                       #
# Instructions made by bgo@vedur.is                     #
# Iceland Met Office                                    #
# 2013                                                  #
#                                                       #
# #######################################################

Introduction:
gtimes provides two sets of time modules gpstime and timefunc
-> gtimes.gpstime: A Python implementation of GPS related time conversions
            by Bud P. Bruegger
-> gtimes.timefunc: Further time modules based on utilizing gpstime

timecalc.py: A simple command line script, somewhat similar to date
             implementing gpstime and timefunc for GPS specific time conversions
             as well as none GPS specific


Instructions:

  (1) run "python setup.py install" which will install the gtimes module in the python domain
  (2) run "sh setup.sh" which will place the command line script in /opt/timecalc and 
      create a softlink /usr/bin/timecalc to make it executable.

All operations must be used with a privileged user (sudo/root)
