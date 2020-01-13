import json
import re
import numpy as np
import os
import time

log_filename = 'output.log'

users = [750, 1000, 1250, 1500, 1750, 2000]
messages = [1, 2]
waits = [30, 60]

totalMsgs = failedMsgs = succeededMsgs = receivedMsgs = 0
msgSentDurations = []
msgReceivedDurations = []

for wait_time in waits:
  for message_count in messages:
    for user_count in users:
      nodejs_command = 'node message_listener/app.js 0 -n {0} -j 300 -i 300 -u {1} -w {2} -s https://stagingchannels.cloudfactory.com/ > {3}'.format(message_count, user_count, wait_time, log_filename)
      print(nodejs_command)
      os.system(nodejs_command)
      with open(log_filename) as output:
        for line in output:
          content = '{' + re.search(r'\{(.*)\}', line).group(1) + '}'
          try:
            obj = json.loads(content)
            if obj['type'] == 'receiver':
              receivedMsgs += obj['msgTotal']
              msgReceivedDurations += obj['msgDurations']
            elif obj['type'] == 'sender':
              totalMsgs += obj['msgTotal']
              succeededMsgs += obj['msgSuccess']
              failedMsgs += obj['msgFail']
              msgSentDurations += obj['msgDurations']
          except Exception as ex:
            print(ex)

        with open('report.txt', 'a') as report:
          report.write('User: {}\n'.format(str(user_count)))
          report.write('Message: {}\n'.format(str(message_count)))
          report.write('Wait: {}\n'.format(str(wait_time)))
          report.write('Total messages: {}\n'.format(str(totalMsgs)))
          report.write('Received messages: {}\n'.format(str(receivedMsgs)))
          report.write('Average sent: {}\n'.format(str(np.mean(msgSentDurations))))
          report.write('Min sent: {}\n'.format(str(np.min(msgSentDurations))))
          report.write('Max sent: {}\n'.format(str(np.max(msgSentDurations)))) 
          report.write('Average received: {}\n'.format(str(np.mean(msgReceivedDurations))))
          report.write('Min received: {}\n'.format(str(np.min(msgReceivedDurations))))
          report.write('Max received: {}\n'.format(str(np.max(msgReceivedDurations))))
          report.write('\n\n\n')


