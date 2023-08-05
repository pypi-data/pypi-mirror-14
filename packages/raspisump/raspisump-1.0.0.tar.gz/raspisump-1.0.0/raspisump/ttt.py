try:
    import ConfigParser as configparser  # Python2
except ImportError:
    import configparser  # Python3

config = configparser.RawConfigParser()
config.read('/home/pi/raspi-sump/raspisump.conf')

configs = {'pit_depth': config.getint('pit', 'pit_depth'),
           'unit': config.get('pit', 'unit'),
           'alert_when': 'high',
           'email_from': 'raspi-sump@linuxnorth.org',
           'email_to': 'alaudet@linuxnorth.org',
           'alert_interval': 5
           }

def email_content(water_depth):
    '''Build the contents of email body which will be sent as an alert'''

    unit_type = 'inches'
    email_contents = {'subject_high': 'Subject: Sump Pump Alert!',
                      'subject_low': 'Subject: Low Water Level Alert!',
                      'message_high': 'Critical! The sump pit water level is',
                      'message_low': 'Warning! The waterlevel is down to'
                      }

    if configs['alert_when'] == 'high':
        subject = email_contents['subject_high']
        message = email_contents['message_high']
    else:
        subject = email_contents['subject_low']
        message = email_contents['message_low']

    return "\r\n".join((
        "From: {}".format(configs['email_from']),
        "To: {}".format(configs['email_to']),
        "{}".format(subject),
        "",
        "{} {} {}.".format(message, str(water_depth), unit_type),
        "Next alert in {} minutes".format(configs['alert_interval']),
        )
        )


x = email_content(1)
beg, sep, end = x.partition('Subject: ')


print(beg[0:5])
print(end[0:9])
