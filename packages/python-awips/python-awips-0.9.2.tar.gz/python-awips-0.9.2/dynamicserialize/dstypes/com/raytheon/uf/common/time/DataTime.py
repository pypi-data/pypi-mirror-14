# #
# This software was developed and / or modified by Raytheon Company,
# pursuant to Contract DG133W-05-CQ-1067 with the US Government.
# 
# U.S. EXPORT CONTROLLED TECHNICAL DATA
# This software product contains export-restricted data whose
# export/transfer/disclosure is restricted by U.S. law. Dissemination
# to non-U.S. persons whether in the United States or abroad requires
# an export license or other authorization.
# 
# Contractor Name:        Raytheon Company
# Contractor Address:     6825 Pine Street, Suite 340
#                         Mail Stop B8
#                         Omaha, NE 68106
#                         402.291.0100
# 
# See the AWIPS II Master Rights File ("Master Rights File.pdf") for
# further licensing information.
# #

# File auto-generated against equivalent DynamicSerialize Java class
# and then modified post-generation to add additional features to better
# match Java implementation.
#    
#     SOFTWARE HISTORY
#    
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    ??/??/??                      xxxxxxxx       Initial Creation.
#    05/28/13         2023         dgilling       Implement __str__().
#    01/22/14         2667         bclement       preserved milliseconds in string representation 
#    03/03/14         2673         bsteffen       allow construction using a Date for refTime
#    06/24/14         3096         mnash          implement __cmp__
#

import calendar
import datetime
import numpy
import time
import StringIO

from dynamicserialize.dstypes.java.util import Date
from dynamicserialize.dstypes.java.util import EnumSet

from TimeRange import TimeRange

class DataTime(object):

    def __init__(self, refTime=None, fcstTime=None, validPeriod=None):
        self.fcstTime = int(fcstTime) if fcstTime is not None else 0
        self.refTime = refTime if refTime is not None else None
        if validPeriod is not None and type(validPeriod) is not TimeRange:
            ValueError("Invalid validPeriod object specified for DataTime.")
        self.validPeriod = validPeriod if validPeriod is not None else None
        self.utilityFlags = EnumSet('com.raytheon.uf.common.time.DataTime$FLAG')
        self.levelValue = numpy.float64(-1.0)
        
        if self.refTime is not None:
            if isinstance(self.refTime, datetime.datetime):
                self.refTime = long(calendar.timegm(self.refTime.utctimetuple()) * 1000) 
            elif isinstance(self.refTime, time.struct_time):
                self.refTime = long(calendar.timegm(self.refTime) * 1000)
            elif hasattr(self.refTime, 'getTime'):
                # getTime should be returning ms, there is no way to check this
                # This is expected for java Date 
                self.refTime = long(self.refTime.getTime())
            else:
                self.refTime = long(refTime)
            dateObj = Date()
            dateObj.setTime(self.refTime)
            self.refTime = dateObj
            
            if self.validPeriod is None:
                validTimeMillis = self.refTime.getTime() + long(self.fcstTime * 1000)
                self.validPeriod = TimeRange()
                self.validPeriod.setStart(validTimeMillis / 1000)
                self.validPeriod.setEnd(validTimeMillis / 1000)
                
        # figure out utility flags
        if fcstTime:
            self.utilityFlags.add("FCST_USED")
        if self.validPeriod and self.validPeriod.isValid():
            self.utilityFlags.add("PERIOD_USED") 
    
    def getRefTime(self):
        return self.refTime

    def setRefTime(self, refTime):
        self.refTime = refTime

    def getFcstTime(self):
        return self.fcstTime

    def setFcstTime(self, fcstTime):
        self.fcstTime = fcstTime

    def getValidPeriod(self):
        return self.validPeriod

    def setValidPeriod(self, validPeriod):
        self.validPeriod = validPeriod

    def getUtilityFlags(self):
        return self.utilityFlags

    def setUtilityFlags(self, utilityFlags):
        self.utilityFlags = utilityFlags

    def getLevelValue(self):
        return self.levelValue

    def setLevelValue(self, levelValue):
        self.levelValue = numpy.float64(levelValue)
    
    def __cmp__(self, other):
        if other is None :
            return 1
        
        # compare the valid times, which are the ref times + forecast times
        validTimeCmp = cmp(self.getRefTime().getTime() + self.getFcstTime(),
                           other.getRefTime().getTime() + other.getFcstTime())
        if validTimeCmp != 0 :
            return validTimeCmp
        
        # compare the forecast times
        fcstTimeCmp = cmp(self.getFcstTime(), other.getFcstTime())
        if fcstTimeCmp != 0 :
            return fcstTimeCmp
        
        # compare the level values
        levelCmp = cmp(self.getLevelValue(), other.getLevelValue())
        if levelValue != 0 :
            return levelValue
        
        # compare the valid periods
        period1 = self.getValidPeriod()
        period2 = other.getValidPerid()
        
        if period1 is None :
            return -1
        elif period2 is None :
            return 1
        
        return cmp(period1.getDuration(), period2.getDuration())
        
            
    def __str__(self):
        buffer = StringIO.StringIO()
        
        if self.refTime is not None:
            refTimeInSecs = self.refTime.getTime() / 1000
            micros = (self.refTime.getTime() % 1000) * 1000
            dtObj = datetime.datetime.utcfromtimestamp(refTimeInSecs)
            dtObj = dtObj.replace(microsecond=micros)
            buffer.write(dtObj.isoformat(' '))
        
        if "FCST_USED" in self.utilityFlags:
            hrs = int(self.fcstTime / 3600)
            mins = int((self.fcstTime - (hrs * 3600)) / 60)
            buffer.write(" (" + str(hrs))
            if mins != 0:
                buffer.write(":" + str(mins))
            buffer.write(")")
        
        if "PERIOD_USED" in self.utilityFlags:
            buffer.write("[")
            buffer.write(self.validPeriod.start.isoformat(' '))
            buffer.write("--")
            buffer.write(self.validPeriod.end.isoformat(' '))
            buffer.write("]")
        
        strVal = buffer.getvalue()
        buffer.close()
        return strVal
