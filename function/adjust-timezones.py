import boto3
import datetime
import re
import util
import os
from pytz import timezone

#####################################################################
# let´s start by defining variables and getting everything ready
#####################################################################
# eventsToAdjust = json.loads(os.environ['EVENTS_TO_ADJUST'])
eventsToAdjust = (os.environ['EVENTS_TO_ADJUST']).split(',')
#eventsToAdjust = ('simonrule').split(',')
#accountId = '842745196201'
accountId=boto3.client('sts').get_caller_identity().get('Account')
region=os.environ['AWS_REGION']
#region = 'eu-central-1'
eventBridge = boto3.client('events')
utc = timezone('UTC')

#####################################################################
# Here comes the actual logic
#####################################################################
todayDate = datetime.datetime.now()
today = datetime.datetime(todayDate.year, todayDate.month, todayDate.day,
                          todayDate.hour, todayDate.minute, todayDate.second)

def lambda_handler(event, context):

    for event in eventsToAdjust:
        if not event:
            continue

        name = event
        arn = 'arn:aws:events:' + region + ':' + accountId + ':rule/' + name

        util.tagRule(name, arn)

        # now we can assume all rules are tagged. We can make use of this and
        # grab the localtimes in order to create the new cron expression
        # let´s start by extracting required infos
        localtimes = util.getLocalTimes(arn)
        newLocalTimes = []
        extractedScheduleInfo = util.getScheduleForRule(name)

        # now we have to determine the timezone
        # if not timezone is set, we assumes it´s europe/Berlin
        tz = util.getTimezoneTagVal(arn)
        if not tz:
            tz = 'Europe/Berlin'

        # iterate over all applied localtime tags and put the values
        # into an array. The code also does necessary timezone calculations
        for localtime in localtimes:
            extractedLocalTime = re.search('(\d+|\*):.*', localtime['value'])
            localHour = extractedLocalTime.group(1)
            diff = util.tz_diff(today, timezone(tz), utc)
            newLocalTimes.append(str(int(localHour) + diff))

        # now we have everything ready. We can use the values gathered
        # before, create a new cron expression and update the rule
        newCronExpression = 'cron({:s} {:s} {:s})'.format(
            extractedScheduleInfo['minutes'], ','.join(newLocalTimes),
            extractedScheduleInfo['appendix'])
        print('New cron expression is:' + newCronExpression)
        eventBridge.put_rule(Name=name, ScheduleExpression=newCronExpression)

    return None