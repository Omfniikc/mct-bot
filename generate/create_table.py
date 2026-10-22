import os 
import json 
from string import Template 
from playwright.async_api import async_playwright 
from PIL import Image, ImageOps 
from text.htmls import *
 
def _normalize_food_json(food_json): 
    if isinstance(food_json, str): 
        try: 
            food_json = json.loads(food_json) 
        except (json.JSONDecodeError, TypeError): 
            return None 
    if not isinstance(food_json, dict): 
        return None 
    items = food_json.get('items', []) 
    total = food_json.get('total') 
    if not items or not total: 
        return None 
    return food_json
 
def _td(value): 
    return chr(60)+'td'+chr(62)+str(value)+chr(60)+'/td'+chr(62) 
 
def _tr(cells, total=False): 
    cls = ' class=\"total-row\"' if total else '' 
    return chr(60)+'tr'+cls+chr(62)+cells+chr(60)+'/tr'+chr(62)
 
def _build_rows(food_json): 
    rows = '' 
    for item in food_json['items']: 
        cells = _td(item['name']) + _td(item['weight']) + _td(item['kcal']) + _td(item['protein']) + _td(item['fat']) + _td(item['carbs']) 
        rows += _tr(cells) 
    total = food_json['total'] 
    cells = _td('Total') + _td(total['weight']) + _td(total['kcal']) + _td(total['protein']) + _td(total['fat']) + _td(total['carbs']) 
    rows += _tr(cells, total=True) 
    return rows
 
async def styling(food_json, food_img='', path='media/img/test.png'): 
    os.makedirs('notes', exist_ok=True) 
    food_json = _normalize_food_json(food_json) 
    if food_json is None: 
        return 'Error: GPT miss' 
    total = food_json['total'] 
    dishes = [item['name'] for item in food_json['items'] if item.get('name') != 'TOTAL'] 
    food_data = {'kcal': total['kcal'], 'p': total['protein'], 'f': total['fat'], 'c': total['carbs'], 'weight': total['weight']} 
    rows = _build_rows(food_json)
    if food_img != '': 
        crop_food_photo(food_img) 
        template = Template(FOOD_PHOTO_HTML) 
        html_template = template.substitute(photo_url='../'+food_img, kal=food_data['kcal'], prot=food_data['p'], fat=food_data['f'], carb=food_data['c'], row=rows) 
    else: 
        template = Template(FOOD_HTML) 
        html_template = template.substitute(kal=food_data['kcal'], prot=food_data['p'], fat=food_data['f'], carb=food_data['c'], row=rows)
    html_path = f'notes/{path}.html'
    os.makedirs(os.path.dirname(html_path), exist_ok=True) 
    img_path = f'notes/{path}.png' 
    json_path = f'notes/{path}.json' 
    with open(json_path, 'w', encoding='utf-8') as file: 
        json.dump(food_json, file, ensure_ascii=False, indent=2) 
    with open(html_path, 'w', encoding='utf-8') as f: 
        f.write(html_template)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('file://'+__file__.replace(chr(92), '/').replace('generate/create_table.py', html_path))
        # Скриншот самого контейнера, а не всей страницы: иначе по краям
        # остаются большие белые поля (viewport 1280px против контента 600px).
        await page.wait_for_selector('.container')
        element = await page.query_selector('.container')
        await element.screenshot(path=__file__.replace(chr(92), '/').replace('generate/create_table.py', img_path))
        await browser.close()
    return dishes, food_data, img_path
 
def crop_food_photo(file_name): 
    img = Image.open(file_name) 
    width, height = img.size 
    target_height = width // 1.5 
    if height <= target_height: 
        return 
    crop_amount = height - target_height 
    top = crop_amount // 2
    bottom = height - (crop_amount - top) 
    cropped_img = img.crop((0, top, width, bottom)) 
    cropped_img.save(file_name)
async def create_trainer_table(clients, user_id): 
    os.makedirs('media/img/trainers_stat', exist_ok=True) 
    os.makedirs('media/html/trainers_stat', exist_ok=True)
    file_name = f'media/img/trainers_stat/{user_id}.png' 
    html_name = f'media/html/trainers_stat/{user_id}.html' 
    rows = ''
    for client in clients: 
        cells = _td(client['name']) + _td(client['kcal']) + _td(client['p']) + _td(client['f']) + _td(client['c']) 
        rows += _tr(cells)
    template = Template(TRAINER_TABLE) 
    html_template = template.substitute(rows=rows) 
    with open(html_name, 'w', encoding='utf-8') as file: 
        file.write(html_template)
    async with async_playwright() as p: 
        browser = await p.chromium.launch(headless=True) 
        page = await browser.new_page() 
        await page.goto('file://'+__file__.replace(chr(92), '/').replace('generate/create_table.py', html_name))
        await page.screenshot(path=__file__.replace(chr(92), '/').replace('generate/create_table.py', file_name), full_page=True) 
        await browser.close() 
    return file_name
