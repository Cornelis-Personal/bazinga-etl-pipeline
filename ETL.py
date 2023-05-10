import json
import xml.etree.ElementTree as ET
import requests
import schedule
from flask import Flask, jsonify
import time

app = Flask(__name__)

def xml_element_to_dict(element) -> dict:
    data = {child.tag: child.text for child in element}
    return data

def main():
    base_url = 'https://api.benzinga.com/api/v2.1/'
    end_point = 'calendar/dividends'
    key = 'faf73611dba341a4af12c2f2f66e07bd'

    headers = {'accept': 'application/json'}
    params = {'token': 'faf73611dba341a4af12c2f2f66e07bd'}

    response = requests.get(base_url + end_point, params=params)

    if response.status_code == 200:
        content_bytes = response.content
        content_str = content_bytes.decode('utf-8')
        root = ET.fromstring(content_str)

        stock_list = []

        for item in root.findall('./dividends/item'):
            stock_dict = xml_element_to_dict(item)
            json_obj = json.dumps(stock_dict)
            stock_list.append(json_obj)

        return stock_list

# Schedule the main function to run once a day
schedule.every().day.at("00:00").do(main)

@app.route('/')
def stocks():
    stock_list = main()
    return '<div>SERVICE IS RUNNING...</div>'

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
        app.run()