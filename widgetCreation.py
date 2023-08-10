import requests
import re


def convert_rows_to_payload(row, programId):
    widget_payload = {'program_id': programId}
    options = []

    for key, value in row.items():

        if value in ('N/A', None):
            continue

        if key == 'Widget Description/Question':
            if row['Widget Type'] == 'Alert':
                widget_payload['text'] = value
            elif row['Widget Type'] == 'Text Ask':
                widget_payload['title'] = value
            else:
                widget_payload['question'] = value
        elif re.match(r'Option \d+ Description', key):
            option_number = key.split(' ')[1]
            option_image = row.get(f'Option {option_number} Image', 'N/A')
            option = {'description': value}
            if option_image != 'N/A':
                option['image_url'] = option_image
            options.append(option)
        elif re.match(r'Option \d+ Image', key) and row['Widget Type'] == 'Emoji Slider':
            option = {'image_url': value}
            options.append(option)
        elif key == 'Interactivity Duration':
            widget_payload['timeout'] = value
        elif key == 'Video Timestamp (second)':
            widget_payload['playback_time_ms'] = int(value)
        elif key == 'Title':
            if row['Widget Type'] == 'Text Ask':
                widget_payload['prompt'] = value
            else:
                widget_payload['title'] = value
        elif key == 'Alert Image Url':
            widget_payload['image_url'] = value

    if options:
        if 'Poll' in row['Widget Type'] or 'Slider' in row['Widget Type']:
            widget_payload['options'] = options
        else:
            if row['Correct Option'] != 'N/A' and row['Correct Option'] is not None:
                correctOptionIndex = int(row['Correct Option'])
                options[correctOptionIndex - 1]['is_correct'] = True
            widget_payload['choices'] = options

    return widget_payload


def create_widget(widget_type, row, programId):
    widget_payload = convert_rows_to_payload(row, programId)
    create_function = {
        'Text Poll': create_text_poll,
        'Alert': create_alert,
        'Image Poll': create_image_poll,
        'Text Quiz': create_text_quiz,
        'Text Ask': create_text_ask,
        'Emoji Slider': create_slider,
        'Image Quiz': create_image_quiz
    }.get(widget_type)

    if create_function:
        create_function(widget_payload)
    else:
        print(f"Widget type '{widget_type}' is not supported.")


def create_text_poll(widget_payload):
    create_widget_helper('text-polls', widget_payload)


def create_image_quiz(widget_payload):
    create_widget_helper('image-quizzes', widget_payload)


def create_image_poll(widget_payload):
    create_widget_helper('image-polls', widget_payload)


def create_text_quiz(widget_payload):
    create_widget_helper('text-quizzes', widget_payload)


def create_text_ask(widget_payload):
    create_widget_helper('text-asks', widget_payload)


def create_slider(widget_payload):
    create_widget_helper('emoji-sliders', widget_payload)


def create_alert(widget_payload):
    create_widget_helper('alerts', widget_payload)


def create_widget_helper(endpoint, widget_payload):
    url = f'https://cf-blast.livelikecdn.com/api/v1/{endpoint}/'
    headers = {
        'Authorization': accessToken,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=widget_payload, headers=headers)
    if response.status_code == 201:
        widget_data = response.json()
        widgetId = widget_data['id']
        print(f'{endpoint.capitalize()} - {widgetId} created successfully.')
        publish_widget(widget_data['schedule_url'])
    else:
        print(f'{endpoint.capitalize()} creation failed.{response.text}')


def publish_widget(schedule_url):
    url = schedule_url
    headers = {
        'Authorization': accessToken,
        'Content-Type': 'application/json'
    }

    publish_payload = {'publish_delay': '00:00:10'}
    response = requests.put(url, json=publish_payload, headers=headers)

    if response.status_code == 200:
        print('Widget scheduled successfully.')
    else:
        print('Widget scheduling failed.')
