import json

settings_json = json.dumps([
    {'type': 'title',
     'title': 'Robot Settings'},
    {'type': 'numeric',
     'title': 'Robot Number',
     'desc': 'Set Robot Number',
     'section': 'robot',
     
     'key': 'robot_number'},
    {'type': 'options',
     'title': 'WiFi options',
     'desc': 'Current WiFi connections',
     'section': 'robot',
     'key': 'options_wifi',
     'options': ['insertion']},
    {'type': 'password',
     'title': 'Wi-Fi Password',
     'desc': 'Wi-Fi access point\'s password',
     'section': 'robot',
     'key': 'wifi_password'}])