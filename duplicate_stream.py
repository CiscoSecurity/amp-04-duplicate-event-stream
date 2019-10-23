import sys
import json
import requests

def ask_for_stream_id(valid_ids):
    while True:
        reply = str(input('Enter the stream ID of the stream you would like to duplicate: ')).strip()
        if reply in valid_ids:
            return reply
        else:
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
            sys.stdout.write('{} is not a valid stream ID try again.\n'.format(reply))

def get_streams():
    url = 'https://api.amp.cisco.com/v1/event_streams'
    request = amp_session.get(url)
    request_json = request.json()
    data = request_json['data']
    return data

def creat_new_stream(name, events_ids, group_guids):
    url = 'https://api.amp.cisco.com/v1/event_streams'
    headers = {'accept': 'application/json',
               'content-type': 'application/json',
               'Accept-Encoding': 'gzip, deflate'}

    # Build the payload
    if not events_ids:
        payload = {"name":name, "group_guid":group_guids}
    else:
        payload = {"name":name, "event_type":events_ids, "group_guid":group_guids}

    # POST to API to create new event stream
    post_req = amp_session.post(url, headers=headers, data=json.dumps(payload))

    return post_req


def output_credentials(response):
    # Name the values in the JSON
    data = response['data']
    stream_id = data['id']
    name = data['name']
    user_name = data['amqp_credentials']['user_name']
    password = data['amqp_credentials']['password']
    queue_name = data['amqp_credentials']['queue_name']
    host = data['amqp_credentials']['host']
    port = data['amqp_credentials']['port']
    proto = data['amqp_credentials']['proto']

    # Construct the stream URL
    stream_url = 'amqps://{}:{}@{}:{}'.format(user_name, password, host, port)

    # Write credentials to disk
    with open('{}_credentials.txt'.format(queue_name), 'w') as file:
        file.write('User Name: {}\n'
                   'Password: {}\n'
                   'Queue Name: {}\n'
                   'URL: {}\n'.format(user_name, password, queue_name, stream_url))

    # Print the values for the new stream
    print('Stream Created Sucesfully!\n')
    print('{:.<15} {}'.format('Stream name:', name))
    print('{:.<15} {}'.format('Stream ID:', stream_id))
    print('\nAMQP Credentials:')
    print('{:.<15} {}'.format('User Name:', user_name))
    print('{:.<15} {}'.format('Password:', password))
    print('{:.<15} {}'.format('Host:', host))
    print('{:.<15} {}'.format('Port:', port))
    print('{:.<15} {}'.format('Queue Name:', queue_name))


    print('\n{}'.format(stream_url))
    print('\nNOTE: Credentials have been saved to {}_credentials.txt'.format(queue_name))


# 3rd Party API Client ID
client_id = 'a1b2c3d4e5f6g7h8i9j0'

# API Key
api_key = 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'

amp_session = requests.Session()
amp_session.auth = (client_id, api_key)

url = 'https://api.amp.cisco.com/v1/event_streams'

stream_data = get_streams()

streams = {str(stream['id']):stream['name'] for stream in stream_data}

print('{:>3} {:>12}'.format('ID', 'Name'))
for stream_id, stream_name in streams.items():
    print('{} - {}'.format(stream_id, stream_name))

if len(streams) is 5:
    sys.exit('\nAlready have 5 streams\nDelete one and try again')

to_duplicate = ask_for_stream_id(streams)

for stream in stream_data:
    if stream['id'] == int(to_duplicate):
        event_types = stream.get('event_types', [])
        group_guids = stream.get('group_guids', [])

if not event_types and not group_guids:
    print('The chosen stream has all event types and all groups')
elif not event_types and group_guids:
    print('The chosen stream has all event types and {} groups'.format(len(group_guids)))
elif event_types and not group_guids:
    print('The chosen stream has {} event types and all groups'.format(len(event_types)))
else:
    print('The chosen stream has {} event types and {} groups'.format(len(event_types), len(group_guids)))

name = input('Enter a name for the event stream you would like to create: ')

new_stream_response = creat_new_stream(name, event_types, group_guids)

# Check if errors were returned
if new_stream_response.status_code // 100 != 2:
    reason = new_stream_response.json()['errors'][0]['details'][0]
    sys.exit('\nFailed to create stream: {}'.format(reason))

output_credentials(new_stream_response.json())
