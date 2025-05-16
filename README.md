Вот обновлённый `README.md`, включающий исходный код файлов `app.py` и `blocker.py`, готовый для размещения на GitHub:

---

```markdown
# 🛡️ Flask: Обнаружение и блокировка SQL-инъекций

Этот проект демонстрирует, как реализовать простую защиту от SQL-инъекций во Flask-приложении. Подозрительные запросы логируются и временно блокируются по IP.

## 📦 Структура проекта

```

.
├── app.py                # Основное Flask-приложение
├── blocker.py            # Логика фильтрации и блокировки
└── logs/
└── intrusions.log    # Лог-файл подозрительных запросов

````

## 🚀 Запуск

1. Установите зависимости:
   ```bash
   pip install flask
````

2. Запустите сервер:

   ```bash
   python app.py
   ```

3. Откройте [http://localhost:5000](http://localhost:5000)

---

## 📄 Исходный код

### `app.py`

```python
from flask import Flask, request
from blocker import check_request

app = Flask(__name__)

@app.before_request
def before_request():
    result = check_request()
    if result:
        return result

@app.route("/")
def home():
    return "Добро пожаловать на защищённый сайт!"

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"Поиск по запросу: {query}"

if __name__ == "__main__":
    app.run(debug=True)
```

---

### `blocker.py`

```python
import re
from flask import request
from datetime import datetime, timedelta

blocked_ips = {}
block_duration = timedelta(minutes=10)

def is_sql_injection(payload):
    pattern = r"(union|select|insert|drop|--|;|'|\"|xp_)"
    return bool(re.search(pattern, payload, re.IGNORECASE))

def log_intrusion(ip, payload):
    with open("logs/intrusions.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {ip} - Suspicious: {payload}\n")

def is_blocked(ip):
    if ip in blocked_ips:
        if datetime.now() < blocked_ips[ip]:
            return True
        else:
            del blocked_ips[ip]
    return False

def check_request():
    ip = request.remote_addr
    if is_blocked(ip):
        return "Your IP is temporarily blocked.", 403

    for key, value in request.args.items():
        if is_sql_injection(value):
            log_intrusion(ip, value)
            blocked_ips[ip] = datetime.now() + block_duration
            return "Potential intrusion detected. IP blocked.", 403

    return None
```

---

## 📂 Логирование

Все подозрительные запросы сохраняются в файл `logs/intrusions.log`. Убедитесь, что папка `logs/` существует:

```bash
mkdir logs
touch logs/intrusions.log
```

---

## 🧠 Примечания

* Используется простое регулярное выражение — его можно адаптировать под нужды проекта.
* Это базовый механизм и не заменяет полноценные средства защиты (WAF, ORM).
* Для production-режима рекомендуется использовать системное логирование и защиту от DDoS/спама.

## 📜 Лицензия

MIT License

```

Если хочешь, могу также сгенерировать `.gitignore`, `requirements.txt` или `LICENSE`.
```
