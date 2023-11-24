from privat import TOKEN
from comand import checking
from ocr import ts 
from translate import translate_text
import requests
import os
import shutil
url = f'https://api.telegram.org/bot{TOKEN}/'


def send_message(chat_id: int, text: str):#отпрака сообщения
    config = {'chat_id': chat_id, 'text': text}
    response = requests.post(f'{url}sendMessage', data = config)
    return response.json()

def process_message(message):#обработка сообщения
    chat_id = message['chat']['id']
    try:
        mess = message['text']
        message_output = checking(mess)
        send_message(chat_id=chat_id,  text=message_output)
    except:
        pass

def process_photo(message):
    chat_id = message['chat']['id']
    if 'photo' in message:
        photo = message['photo'][-1]
        file_id = photo['file_id']
        file_path = get_file_path(file_id)
        text = download_photo(file_path=file_path, chat_id=chat_id)
        text = translate_text(text=text, target_language='ru')
        send_message(chat_id=chat_id, text=f'Русский:\n{text}')
        text = translate_text(text=text)
        send_message(chat_id=chat_id, text=f'Английский:\n{text}')

def download_photo(file_path, chat_id):
    save_path = f'src/{chat_id}/{file_path}'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_path}')
    with open(save_path, 'wb') as file:
        file.write(response.content)

    text = ts(save_path)
    try:
        shutil.rmtree('src')
    except OSError as e:
        print(f"Ошибка: {e}")
    return text

def get_file_path(file_id):
    config = {'file_id': file_id}
    response = requests.get(f'{url}getFile', params=config)
    file_path = response.json()['result']['file_path']
    return file_path


def get_updates(offset = None):#получение обновлений
    config = {'offset': offset, 'timeout': 30}
    response = requests.get(f'{url}getUpdates', params=config)
    return response.json()

def main():
    offset = None

    while True:
        updates = get_updates(offset=offset)
        if 'result' in updates and updates['result']:
            for update in updates['result']:
                offset = update['update_id'] + 1
                if 'message' in update:
                    process_message(message=update['message'])
                    process_photo(message=update['message'])


if __name__ == '__main__':
    main()















