[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/AMP-for-Endpoints "Gitter chat")

### AMP for Endpoints Duplicate Event Stream

Script fetches the list of existing streams and prompts the users to choose which one to duplicate. The chosen stream will be duplicated with the same event types and group GUIDs. The credentials for the new stream are printed to the console and saved to disk.

### Before using you must update the following:
- client_id 
- api_key

### Usage:
```
python duplicate_stream.py
```

### Example script output:  
```
 ID         Name
1695 - Threat Detected Events
1814 - Vulnerable Software Events
2146 - Engineering All Events
Enter the stream ID of the stream you would like to duplicate: 2146
The chosen stream has 93 event types and 1 groups
Enter a name for the event stream you would like to create: Duplicated Engineering All Events
Stream Created Sucesfully!

Stream name:... Duplicated Engineering All Events
Stream ID:..... 2220

AMQP Credentials:
User Name:..... 2220-92a4d13197b6bbeb40f0
Password:...... 4a5cd01ac514c0d3fdb923e88346baaa59f3d933
Host:.......... export-streaming.amp.cisco.com
Port:.......... 443
Queue Name:.... event_stream_2220

amqps://2220-92a4d13197b6bbeb40f0:4a5cd01ac514c0d3fdb923e88346baaa59f3d933@export-streaming.amp.cisco.com:443

NOTE: Credentials have been saved to event_stream_2220_credentials.txt
```
