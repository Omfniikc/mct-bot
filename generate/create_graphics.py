import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates

from jinja2 import Template
from playwright.async_api import async_playwright
from text.htmls import WEIGHT_WEEKLY_HTML, WEIGHT_MONTHLY_HTML, WEIGHT_QUARTER_HTML


async def gen_weight_weekly_graphic(data={'date':["16/03", "17/03", "18/03", "19/03", "20/03", "21/03", "22/03"], 'weight':[80.0, 79.3, 78.85, 79.85, 76.6, 75.1, 77.95]}, path="media/img/test.png"):
    dates = data['date']
    weights = data["weight"]
    
    html_template = Template(WEIGHT_WEEKLY_HTML)
    html = html_template.render(dates=dates, weights=weights, last_index=len(dates)-1)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 390, "height": 390})
        await page.set_content(html)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=path)
        await browser.close()
    
    return path


async def gen_weight_monthly_graphic(data={'date':["16/03", "17/03", "18/03", "19/03", "20/03", "21/03", "22/03"], 'weight':[80.0, 79.3, 78.85, 79.85, 76.6, 75.1, 77.95]}, path="media/img/test.png"):
    dates = data['date']
    weights = data["weight"]
    
    html_template = Template(WEIGHT_MONTHLY_HTML)
    html = html_template.render(dates=dates, weights=weights, last_index=len(dates)-1)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 690, "height": 400})
        await page.set_content(html)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=path)
        await browser.close()
    
    return path


async def gen_weight_quarter_graphic(data={'date':["16/03", "17/03", "18/03", "19/03", "20/03", "21/03", "22/03"], 'weight':[80.0, 79.3, 78.85, 79.85, 76.6, 75.1, 77.95]}, path="media/img/test.png"):
    dates = data['date']
    weights = data["weight"]
    
    html_template = Template(WEIGHT_QUARTER_HTML)
    html = html_template.render(dates=dates, weights=weights, last_index=len(dates)-1)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 900, "height": 400})
        await page.set_content(html)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=path)
        await browser.close()
    
    return path
