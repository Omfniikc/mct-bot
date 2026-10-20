import json 
import logging 
from openai import AsyncOpenAI 
from config import TOKIFY_API_KEY, TOKIFY_BASE_URL 
 
 
client = AsyncOpenAI(api_key=TOKIFY_API_KEY, base_url=TOKIFY_BASE_URL, timeout=90.0) 
 
 
def _parse_json(content): 
    try: 
        return json.loads(content) 
    except (json.JSONDecodeError, TypeError): 
        try: 
            start = content.index('{') 
            end = content.rindex('}') 
            return json.loads(content[start:end+1]) 
        except Exception as e: 
            logging.error('Failed to parse JSON response: %s', e) 
            return None
 
 
def _build_messages(text, image_url=None): 
    prompt = 'You are a nutrition data extractor. Return ONLY valid JSON with this exact schema: ' 
    prompt += '{"items":[{"name":"string","weight":number,"kcal":number,"protein":number,"fat":number,"carbs":number}],' 
    prompt += '"total":{"name":"TOTAL","weight":number,"kcal":number,"protein":number,"fat":number,"carbs":number},' 
    prompt += '"food_detected":boolean}. ' 
    prompt += 'Weight/kcal/protein/fat/carbs are numbers for the whole portion. Use point as decimal separator. ' 
    prompt += 'If no food is detected, return {"items":[],"total":null,"food_detected":false}. ' 
    prompt += f'Analyze this food description or image: {text}' 
    content = [{"type": "text", "text": prompt}] 
    if image_url: 
        content.append({"type": "image_url", "image_url": {"url": image_url}}) 
    return [{"role": "user", "content": content}]
 
 
async def _ask_for_food(text, image_url=None): 
    response = await client.chat.completions.create( 
        model="gpt-6-astra", 
        messages=_build_messages(text, image_url), 
        response_format={"type": "json_object"}, 
        max_tokens=1000, 
    ) 
    return _parse_json(response.choices[0].message.content) 
 
 
async def text_to_food_table(text): 
    return await _ask_for_food(text) 
 
 
async def scan_food(image_url): 
    return await _ask_for_food('Analyze the food in this image.', image_url)
 
 
async def re_scan(table, changes): 
    if isinstance(table, str): 
        try: 
            table = _parse_json(table) 
        except Exception: 
            pass 
    prompt = 'Edit the food table according to the changes and recalculate nutrition values. ' 
    prompt += 'Return ONLY the same JSON schema. If changes do not affect food, set "food_detected": false and return empty items. ' 
    prompt += f'Table: {json.dumps(table, ensure_ascii=False)}. Changes: {changes}' 
    return await _ask_for_food(prompt)
 
 
async def generate_nutrition_advice(food_json): 
    if isinstance(food_json, str): 
        food_json = _parse_json(food_json) 
    if not isinstance(food_json, dict): 
        logging.error('Invalid food JSON format') 
        return 'Error: invalid data format' 
    try: 
        prompt = 'Analyze this nutrition JSON and write a short unique nutritionist tip, one or two sentences, with emojis: ' 
        prompt += json.dumps(food_json, ensure_ascii=False) 
        response = await client.chat.completions.create( 
            model="gpt-6-astra", 
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}], 
            max_tokens=300, 
        ) 
        return response.choices[0].message.content.replace('*', '') 
    except Exception as e: 
        logging.exception('Error in generate_nutrition_advice: %s', e) 
        return 'Error while generating nutrition advice'
