import boto3
import datetime
import pytz
import re

eventBridge = boto3.client('events')


#####################################################################
# Ok, everything is set up. Let us declare some functions which we
# will need later
#####################################################################
def is_dst(dt=None, timezone="Europe/Berlin"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


def tz_diff(date, tz1, tz2):
    '''
    Returns the difference in hours between timezone1 and timezone2
    for a given date.
    '''
    loc=date.astimezone(tz1)
    loc2=date.astimezone(tz2)
    # print(datetime.datetime.timestamp(loc))
    # print(datetime.datetime.timestamp(loc2))
    # print(loc.timestamp-loc2.timestamp)
    return loc2.hour-loc.hour

    # return (tz1.localize(date) -
    #         tz2.localize(date).astimezone(tz1))\
    #         .seconds/3600

def getLocalTimes(arn):
    tags = eventBridge.list_tags_for_resource(ResourceARN=arn)
    tags = tags['Tags']
    retVal = []
    for tag in tags:
        if tag['Key'].startswith('local-time'):
            retVal.append({'key': tag['Key'], 'value': tag['Value']})
    return retVal


def getScheduleForRule(name):
    scheduleExpression = eventBridge.describe_rule(
        Name=name)['ScheduleExpression']
    exctractedScheduleExpr = re.search('cron\((\S+) (\S+) (.*)\)',
                                       scheduleExpression)
    exprMinutes = exctractedScheduleExpr.group(1)
    exprHour = exctractedScheduleExpr.group(2)
    exprAppendix = exctractedScheduleExpr.group(3)
    return {
        'minutes': exprMinutes,
        'hours': exprHour,
        'appendix': exprAppendix
    }

def getTimezoneTagVal(arn):
    tags = eventBridge.list_tags_for_resource(ResourceARN=arn)
    tags = tags['Tags']
    for tag in tags:
        if tag['Key'] == 'timezone':
            return tag['Value']
    return None

def tagRule(name, arn):
    localtime = getLocalTimes(arn)
    if not localtime:
        print('No local-time tag found for event ' + name)

        tags = eventBridge.list_tags_for_resource(ResourceARN=arn)
        extractedScheduleInfo = getScheduleForRule(name)
        hours = extractedScheduleInfo['hours']
        minutes = extractedScheduleInfo['minutes']

        if "," in hours:
            # if we reach here, it means we have a cron expression like cron(55 04,10,16,22 ? * 2-6 *)
            # in that case, we have to iterate over all the hours and create a tag out of these
            splitted = hours.split(',')
            for idx, hour in enumerate(splitted):
                tags['Tags'].append({
                    'Key': 'local-time' + str(idx),
                    'Value': hour + ':' + minutes
                })
        else:
            tags['Tags'].append({
                'Key': 'local-time',
                'Value': hours + ':' + minutes
            })

        eventBridge.tag_resource(ResourceARN=arn, Tags=tags['Tags'])