from openai import AsyncOpenAI
import re

from config import *


client = AsyncOpenAI(api_key=GPT_TR_TOKEN)


async def generate_ration(data):
    assistant = await client.beta.assistants.retrieve('asst_MixwwgBxyDU8FD4cDDsE6t3F')
    thread = await client.beta.threads.create()
    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=
            "Составь мне рацион питания, мои данные:"
            f"1) Возраст: {data['age']}"
            f"2) Пол:  {data['sex']}"
            f"3) Рост (в см): {data['height']}"
            f"4) Вес (в кг): {data['weight']}"
            f"5) Цель: {data['goal']}"
            f"6) Ограничения в питании: {data['cancel']}"
            f"7) Физическая активность: {data['sport_lvl']}"
            f"8) Количество приёмов пищи в день: {data['eat_count']}"
            f"9) Дополнительный комментарий: {data['comment']}"
            )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=""
    )

    if run.status == 'completed':
        messages = await client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(messages)
        answer = messages.data[0].content[0].text.value
        print(answer)

        # Обработка ответа GPT
        while '*' in answer:
            answer = answer.replace('*', '')
        while '#' in answer:
            answer = answer.replace('#', '')

        # patterns = {
        #     "Цель по калориям на день": r"Цель по калориям на день:\s*(\d+)\s*ккал",
        #     "Цель по белкам на день": r"Цель по белкам на день:\s*(\d+)\s*г",
        #     "Цель по жирам на день": r"Цель по жирам на день:\s*(\d+)\s*г",
        #     "Цель по углеводам на день": r"Цель по углеводам на день:\s*(\d+)\s*г"
        # }
        patterns = {
            "Цель по калориям на день": r"Цель по калориям на день:\s*(\d+)\s*ккал",
            "Цель по белкам на день": r"Цель по белкам на день:\s*(\d+)\s*г",
            "Цель по жирам на день": r"Цель по жирам на день:\s*(\d+)\s*г",
            "Цель по углеводам на день": r"Цель по углеводам на день:\s*(\d+)\s*г"
        }

        # Извлекаем значения с помощью регулярных выражений
        goals = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, answer)
            if match:
                goals[key] = int(match.group(1))
        vls = []
        # Выводим результаты
        for goal, value in goals.items():
            vls.append(value)
            print(f"{goal}: {value}")

        print([answer, vls])
        return [answer, vls] # возвращает списиок [ответ GPT, распаршеные цели]
    else:
        print(run.status)


async def generate_tren(data):
    assistant = await client.beta.assistants.retrieve('asst_biE8HZXGS4MVYMNa4oKEk5B7')
    thread = await client.beta.threads.create()
    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=
            "Составь мне план тренировок, мои данные:\n"+
            f"1) Возраст: {data['k1']}\n"+
            f"2) Пол:  {data['k2']}\n"+
            f"3) Рост (в см): {data['k3']}\n"+
            f"4) Вес (в кг): {data['k4']}"+
            f"5) Цель: {data['k5']}\n"+
            f"6) Уровень физической подготовки:{data['k6']}\n"+
            f"7) Медицинские ограничения или травмы которые следует учитывать при составлении плана тренировок: {data['k7']}\n"+
            f"8) Желаемое количество дней в неделю для тренировок: {data['k8']}\n"+
            f"9) Комментарий к тренировкам: {data['k9']}"
            )
    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="составь план тренировок"
    )

    if run.status == 'completed':
        messages = await client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(messages)
        answer = messages.data[0].content[0].text.value
        print(answer)

        while '*' in answer:
            answer = answer.replace('*', '')
        while '#' in answer:
            answer = answer.replace('#', '')
        print(answer)
        return answer
    else:
        print(run.status)