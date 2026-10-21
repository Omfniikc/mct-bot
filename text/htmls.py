FOOD_PHOTO_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        @font-face {
            font-family: "Actay";
            src: url("https://media.uprock.school/fonts/Actay/Actay-Regular.otf");
        }

        @font-face {
            font-family: "Actay_bold";
            src: url("https://media.uprock.school/fonts/Actay/ActayWide-Bold.otf");
        }

        * {
            font-family: "Actay";
        }

        body {
            margin: 0;
        }

        .container {
            width: 600px;
        }

        .food_image img {
            width: 600px;
            border-radius: 20px;
            margin-bottom: 15px;
        }

        .food_block {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .food_num {
            font-family: "Actay_bold";
            font-size: 30px;
        }

        .block {
            border: 2px solid black;
            width: 120px;
            height: 50px;
            border-radius: 10px;
            text-align: center;
            padding: 10px;
        }

        table {
            width: 100%;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }

        th {
            background-color: #e66363;
            color: rgb(0, 0, 0);
            font-family: "Actay_bold";
        }

        table, td, th {
            border-collapse: collapse;
            border: 2px solid #010101;
        }

        tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .total-row {
            font-weight: bold;
            background-color: #e8f8f5 !important;
        }

        .total-row td {
            font-family: "Actay_bold";
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="food_image">
            <img src="$photo_url" alt="Фото блюда" class="food-image">
        </div>
        <div class="food_block">
            <div class="block">
                <div class="food_num">$kal</div>
                Ккалории
            </div>
            <div class="block">
                <div class="food_num">$prot</div>
                Белки, г
            </div>
            <div class="block">
                <div class="food_num">$fat</div>
                Жиры, г
            </div>
            <div class="block">
                <div class="food_num">$carb</div>
                Углеводы, г
            </div>
        </div>
        <div class="food_table">
            <table>
                <thead>
                    <tr>
                        <th>Название</th>
                        <th>Вес, г</th>
                        <th>Ккал</th>
                        <th>Б, г</th>
                        <th>Ж, г</th>
                        <th>У, г</th>
                    </tr>
                </thead>
                <tbody>
                    $row
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''

FOOD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        @font-face {
            font-family: "Actay";
            src: url("https://media.uprock.school/fonts/Actay/Actay-Regular.otf");
        }

        @font-face {
            font-family: "Actay_bold";
            src: url("https://media.uprock.school/fonts/Actay/ActayWide-Bold.otf");
        }

        * {
            font-family: "Actay";
        }

        body {
            margin: 0;
        }

        .container {
            width: 600px;
        }

        .food_image img {
            width: 600px;
            border-radius: 20px;
            margin-bottom: 15px;
        }

        .food_block {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .food_num {
            font-family: "Actay_bold";
            font-size: 30px;
        }

        .block {
            border: 2px solid black;
            width: 120px;
            height: 50px;
            border-radius: 10px;
            text-align: center;
            padding: 10px;
        }

        table {
            width: 100%;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }

        th {
            background-color: #e66363;
            color: rgb(0, 0, 0);
            font-family: "Actay_bold";
        }

        table, td, th {
            border-collapse: collapse;
            border: 2px solid #010101;
        }

        tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .total-row {
            font-weight: bold;
            background-color: #e8f8f5 !important;
        }

        .total-row td {
            font-family: "Actay_bold";
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="food_block">
            <div class="block">
                <div class="food_num">$kal</div>
                Ккалории
            </div>
            <div class="block">
                <div class="food_num">$prot</div>
                Белки, г
            </div>
            <div class="block">
                <div class="food_num">$fat</div>
                Жиры, г
            </div>
            <div class="block">
                <div class="food_num">$carb</div>
                Углеводы, г
            </div>
        </div>
        <div class="food_table">
            <table>
                <thead>
                    <tr>
                        <th>Название</th>
                        <th>Вес, г</th>
                        <th>Ккал</th>
                        <th>Б, г</th>
                        <th>Ж, г</th>
                        <th>У, г</th>
                    </tr>
                </thead>
                <tbody>
                    $row
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''

TRAINER_TABLE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        @font-face {
            font-family: "Actay";
            src: url("https://media.uprock.school/fonts/Actay/Actay-Regular.otf");
        }

        @font-face {
            font-family: "Actay_bold";
            src: url("https://media.uprock.school/fonts/Actay/ActayWide-Bold.otf");
        }

        * {
            font-family: "Actay";
        }

        body {
            margin: 0;
        }

        .container {
            width: 600px;
        }

        .food_image img {
            width: 600px;
            border-radius: 20px;
            margin-bottom: 15px;
        }

        .food_block {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .food_num {
            font-family: "Actay_bold";
            font-size: 30px;
        }

        .block {
            border: 2px solid black;
            width: 120px;
            height: 50px;
            border-radius: 10px;
            text-align: center;
            padding: 10px;
        }

        table {
            width: 100%;
            margin-top: 20px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }

        th {
            background-color: #e66363;
            color: rgb(0, 0, 0);
            font-family: "Actay_bold";
        }

        table, td, th {
            border-collapse: collapse;
            border: 2px solid #010101;
        }

        tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .total-row {
            font-weight: bold;
            background-color: #e8f8f5 !important;
        }

        .total-row td {
            font-family: "Actay_bold";
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="food_table">
            <table>
                <thead>
                    <tr>
                        <th>Имя пользователя</th>
                        <th>Ккал</th>
                        <th>Б, г</th>
                        <th>Ж, г</th>
                        <th>У, г</th>
                    </tr>
                </thead>
                <tbody>
                    $rows
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''


WEIGHT_WEEKLY_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Статистика</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @font-face {
            font-family: 'Actay Wide';
            src: url( 'https://media.uprock.school/fonts/Actay/ActayWide-Bold.otf') format('opentype');
        }
        @font-face {
            font-family: 'Montserrat';
            src: url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400&display=swap') format('truetype');
        }
        * {
            font-family: 'Actay Wide', sans-serif;
        }
        body {
            margin: 0;
            background: #1e1e1e;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 400px;
            box-sizing: border-box;
        }
        h2 {
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            text-align: center;
            margin: 0 0 10px 0;
        }
        .tabs {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .tabs span {
            color: #bbb;
        }
        .tabs span.active {
            color: black;
            font-weight: bold;
        }
        canvas {
            margin-top: 10px;
        }
    </style>
</head>
<body>
<div class="card">
    <h2>Статистика</h2>
    <div class="tabs">
        <span class="active">Неделя</span>
        <span>Месяц</span>
        <span>Квартал</span>
    </div>
    <div style="font-size:14px; margin-bottom:5px;">Вес, кг / дата</div>
    <canvas id="chart" width="340" height="240"></canvas>
</div>
<script>
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{ dates | safe }},
            datasets: [{
                data: {{ weights | safe }},
                borderColor: 'red',
                backgroundColor: 'red',
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: function(context) {
                    return context.dataIndex === {{ last_index }} ? 'white' : 'red';
                },
                pointBorderColor: 'red',
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    min: Math.floor(Math.min(...{{ weights | safe }}) * 10) / 10 - 0.2,
                    max: Math.ceil(Math.max(...{{ weights | safe }}) * 10) / 10 + 0.2,
                    ticks: {
                        stepSize: 0.2
                    },
                    grid: {
                        color: '#eee'
                    }
                },
                x: {
                    ticks: {
                        color: (ctx) => ctx.index === {{ last_index }} ? 'red' : '#333'
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
</script>
</body>
</html>
"""

WEIGHT_MONTHLY_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Статистика</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @font-face {
            font-family: 'Actay Wide';
            src: url( 'https://media.uprock.school/fonts/Actay/ActayWide-Bold.otf') format('opentype');
        }
        @font-face {
            font-family: 'Montserrat';
            src: url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400&display=swap') format('truetype');
        }
        * {
            font-family: 'Actay Wide', sans-serif;
        }
        body {
            margin: 0;
            background: #1e1e1e;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Arial', sans-serif;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 700px;
            box-sizing: border-box;
        }
        h2 {
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            text-align: center;
            margin: 0 0 10px 0;
        }
        .tabs {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .tabs span {
            color: #bbb;
        }
        .tabs span.active {
            color: black;
            font-weight: bold;
        }
        canvas {
            margin-top: 10px;
        }
    </style>
</head>
<body>
<div class="card">
    <h2>Статистика</h2>
    <div class="tabs">
        <span>Неделя</span>
        <span class="active">Месяц</span>
        <span>Квартал</span>
    </div>
    <div style="font-size:14px; margin-bottom:5px;">Вес, кг / дата</div>
    <canvas id="chart" width="600" height="300"></canvas>
</div>
<script>
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{ dates | safe }},
            datasets: [{
                data: {{ weights | safe }},
                borderColor: 'red',
                backgroundColor: 'red',
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: function(context) {
                    return context.dataIndex === {{ last_index }} ? 'white' : 'red';
                },
                pointBorderColor: 'red',
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    min: Math.floor(Math.min(...{{ weights | safe }}) * 10) / 10 - 0.2,
                    max: Math.ceil(Math.max(...{{ weights | safe }}) * 10) / 10 + 0.2,
                    ticks: { stepSize: 0.4 },
                    grid: { color: '#eee' }
                },
                x: {
                    ticks: {
                        color: (ctx) => ctx.index === {{ last_index }} ? 'red' : '#333'
                    },
                    grid: { display: false }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
</script>
</body>
</html>
"""

WEIGHT_QUARTER_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Статистика</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @font-face {
            font-family: 'Actay Wide';
            src: url( 'https://media.uprock.school/fonts/Actay/ActayWide-Bold.otf') format('opentype');
        }
        @font-face {
            font-family: 'Montserrat';
            src: url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400&display=swap') format('truetype');
        }
        * {
            font-family: 'Actay Wide', sans-serif;
        }
        body {
            margin: 0;
            background: #1e1e1e;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Arial', sans-serif;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 900px;
            box-sizing: border-box;
        }
        h2 {
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            text-align: center;
            margin: 0 0 10px 0;
        }
        .tabs {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .tabs span {
            color: #bbb;
        }
        .tabs span.active {
            color: black;
            font-weight: bold;
        }
        canvas {
            margin-top: 10px;
        }
    </style>
</head>
<body>
<div class="card">
    <h2>Статистика</h2>
    <div class="tabs">
        <span>Неделя</span>
        <span>Месяц</span>
        <span class="active">Квартал</span>
    </div>
    <div style="font-size:14px; margin-bottom:5px;">Вес, кг / дата</div>
    <canvas id="chart" width="820" height="300"></canvas>
</div>
<script>
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{ dates | safe }},
            datasets: [{
                data: {{ weights | safe }},
                borderColor: 'red',
                backgroundColor: 'red',
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: function(context) {
                    return context.dataIndex === {{ last_index }} ? 'white' : 'red';
                },
                pointBorderColor: 'red',
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    min: Math.floor(Math.min(...{{ weights | safe }}) * 10) / 10 - 0.2,
                    max: Math.ceil(Math.max(...{{ weights | safe }}) * 10) / 10 + 0.2,
                    ticks: { stepSize: 0.5 },
                    grid: { color: '#eee' }
                },
                x: {
                    ticks: {
                        color: (ctx) => ctx.index === {{ last_index }} ? 'red' : '#333'
                    },
                    grid: { display: false }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
</script>
</body>
</html>
"""
