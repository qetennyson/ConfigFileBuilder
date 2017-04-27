from configobj import ConfigObj
import csv
import os

# switch_config.py handles custom configuration of
# .dat (or .ini with a tweak) files.  In this case, we're
# building custom files for a series of offices that are getting
# special power switches to support broadband connectivity.

# We're using the ConfigObj module to parse the .dat file effectively.
# In this case, the .dat file was poorly formatted, and required
# modification of the base file (no big deal really) in order to
# parse with ConfigObj.  You'll see where we "unmodify" the file
# at the tail end of this program. (requires from configobj import ConfigObj)

# In this case, we're using a csv as a rudimentary database with which we'll
# populate the necessary fields.  You can use raw_input, args, or
# whatever else fits your needs. (requires import csv)

# This is an open source version, and for that reason, field names
# are somewhat sanitized, but should give a clear picture of what's
# going on.

# written by Quincy Tennyson, 4/27/2017 - github.com/qetennyson

# Here we instantiate a ConfigObj object that stores our .dat file in the config
# variable.  You can learn more about ConfigObj at http://www.voidspace.org.uk/python/configobj.html
# it's a pretty robust tool!

config = ConfigObj('configtest.dat', list_values=True, raise_errors=False)

# uses the csv module to parse the data in our file as an array.  Note the dialect setting.
with open('config.csv') as csvfile:
    configcsv = csv.reader(csvfile, dialect='excel')
    office = 'null'
    # loops through our csv file, and sets the config object key/value fields with the designated data.

    # I'm an inexperienced programmer, so there is without a doubt a better way to control the iteration.  In
    # this case, I know what my last office is.  It's not exactly scalable, but the dataset is small
    # enough that I'm using this lazily.
    while (office != 'BestOfficeNA'):
        for row in configcsv:
            config.filename = row[0] + '-powerswitch.dat'
            config['Hostname'] = row[0]
            config['Ipaddr'] = row[2]
            config['OutletName1'] = row[3]
            config['Gateway'] = row[4]
            config['DNS'] = 'DNSTEST'
            config['Account1'] = row[6]
            config['Password1'] = 'passwordtest'
            config['TimeServer1'] = '8.8.8.8'
            config['TimeZone'] = '800'
            office = row[0]
            #writes the data to our config object.
            config.write()

# now we will loop through all of our files again, and add back the lines we had to remove
# from the badly formatted .dat
with open('config.csv') as csvfile:
    configcsv = csv.reader(csvfile, dialect='excel')
    # resets our pointer so that we don't start at the last row of the csv
    csvfile.seek(0)
    office = 'null'
    # again, my rudimentary iteration method.
    while (office != 'BestOfficeNA'):
        for row in configcsv:
            filename = row[0] + '-powerswitch.dat'
            with open(filename, 'r') as cfgFile:
                almostCorrect = cfgFile.read()
            correct = "#The following line must not be removed.\nDefault\n" + almostCorrect
            with open(filename, 'w') as cfgFile:
                cfgFile.write(correct)
            # i found this useful for debugging the csv position.  remove at your pleasure.
            print row[0]
            office = row[0]
