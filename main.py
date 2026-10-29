from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TowerBit Analyzer</title>
    <style>
        body {
            background-color: #121019;
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .container {
            width: 90%;
            max-width: 360px;
            background: #1c1829;
            padding: 15px;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 20px;
        }
        .cell {
            background: #28223c;
            height: 45px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            color: #5c537c;
            transition: all 0.3s ease;
        }
        .cell.safe {
            background: #2563eb;
            color: white;
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.6);
        }
        .cell.danger {
            background: #dc2626;
            color: white;
        }
        .btn {
            width: 100%;
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: white;
            border: none;
            padding: 14px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
        }
        .btn:active {
            transform: scale(0.98);
        }
        .status {
            text-align: center;
            margin-bottom: 12px;
            font-size: 14px;
            color: #9ca3af;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="status" id="statusText">Нажмите для анализа</div>
    <div class="grid" id="grid">
        <!-- Генерируем сетку 8 рядов по 4 ячейки -->
    </div>
    <button class="btn" onclick="startAnalysis()">СДЕЛАТЬ АНАЛИЗ</button>
</div>

<script>
    const rows = 8;
    const cols = 4;
    const gridEl = document.getElementById('grid');
    const statusText = document.getElementById('statusText');

    // Создаем ячейки сетки
    function createGrid() {
        gridEl.innerHTML = '';
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = r;
                cell.innerText = 'B';
                gridEl.appendChild(cell);
            }
        }
    }

    function startAnalysis() {
        statusText.innerText = "Сканирование алгоритмов...";
        const cells = document.querySelectorAll('.cell');
        
        // Сброс цветов
        cells.forEach(c => {
            c.className = 'cell';
        });

        let step = 0;
        // Эффект анимации сканирования снизу вверх
        const interval = setInterval(() => {
            if (step < rows) {
                // Подсвечиваем случайную ячейку в каждом ряду как "проверенную"
                for (let c = 0; c < cols; c++) {
                    const index = (rows - 1 - step) * cols + c;
                    cells[index].style.background = '#3b3556';
                }
                step++;
            } else {
                clearInterval(interval);
                showResult(cells);
            }
        }, 150);
    }

    function showResult(cells) {
        statusText.innerText = "Анализ завершен!";
        
        // Для каждого ряда выбираем по одной безопасной ячейке (или условно безопасной)
        for (let r = 0; r < rows; r++) {
            const randomCol = Math.floor(Math.random() * cols);
            for (let c = 0; c < cols; c++) {
                const index = r * cols + c;
                if (c === randomCol) {
                    cells[index].className = 'cell safe';
                    cells[index].innerText = '✓';
                } else {
                    cells[index].className = 'cell';
                    cells[index].innerText = '•';
                }
            }
        }
    }

    createGrid();
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_PAGE
