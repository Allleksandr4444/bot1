import requests
import time


API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN = '7059376754:AAFXRWe0AMni9boHlm2_LFrxRt3XXm93bNY'
TEXT = 'это конечно хорошо, но как насчет фото котика?'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('


MAX_COUNTER = 1000

offset = -2
counter = 0
cat_response: requests.Response
cat_link: str


while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                chat_message = result['message']['text']
                TEXT2 = f'"{chat_message}" {TEXT}'
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT2}')
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1