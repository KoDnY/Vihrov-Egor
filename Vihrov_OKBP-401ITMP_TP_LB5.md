# Лабораторная работа № 5

### 1. Пропускная способность записи

**Вопрос:** Три сети обрабатывают разное число транзакций в секунду: Ethereum — 30, Binance Smart Chain — 160, Solana — 50 000. Напишите функцию, которая вычисляет, сколько транзакций обработает каждая сеть за один час, и определяет сеть-лидера.

**Ответ:**

```python
def transactions_per_hour(networks):
    hourly = {name: tps * 3600 for name, tps in networks.items()}
    leader = max(hourly, key=hourly.get)
    return hourly, leader


networks = {"Ethereum": 30, "Binance Smart Chain": 160, "Solana": 50000}
hourly, leader = transactions_per_hour(networks)

for name, count in hourly.items():
    print(f"{name}: {count:,} транзакций/час")
print("Лидер:", leader)
```

### 2. Соотношение операций чтения к записи

**Вопрос:** На каждую операцию записи приходится от 100 до 10 000 операций чтения. При 500 операциях записи в секунду вычислите минимальное и максимальное число операций чтения в секунду.

**Ответ:**

```python
def read_limits(writes):
    return writes * 100, writes * 10000


writes = 500
minimum, maximum = read_limits(writes)
print(f"Записей в секунду: {writes}")
print(f"Минимум чтений/с: {minimum:,}")
print(f"Максимум чтений/с: {maximum:,}")
```

### 3. Простейший блокчейн из блоков

**Вопрос:** Реализуйте класс Block с полями index, data, prev_hash и методом вычисления хэша (SHA-256 от строки index + data + prev_hash). Соберите цепочку из трёх блоков, где каждый хранит хэш предыдущего; у генезис-блока prev_hash = "0".

**Ответ:**

```python
import hashlib


class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        text = str(self.index) + self.data + self.prev_hash
        return hashlib.sha256(text.encode("utf-8")).hexdigest()


chain = [Block(0, "Генезис", "0")]
for index in range(1, 3):
    chain.append(Block(index, f"Данные блока {index}", chain[-1].hash))

for block in chain:
    print(f"Блок {block.index}: hash={block.hash[:16]}... "
          f"prev={block.prev_hash[:16]}...")
```

### 4. Хеширование SHA-256

**Вопрос:** Напишите функцию, возвращающую SHA-256-хэш произвольной строки, и проверьте её на строке "blockchain".

**Ответ:**

```python
import hashlib


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


print("SHA-256('blockchain') =")
print(sha256("blockchain"))
```

### 5. Proof-of-Work

**Вопрос:** Реализуйте функцию майнинга: для data = "block1" и сложности 4 найдите nonce, при котором SHA-256 от (data + nonce) начинается с четырёх нулей.

**Ответ:**

```python
import hashlib


def mine(data, difficulty):
    if not 0 <= difficulty <= 64:
        raise ValueError("Сложность должна быть от 0 до 64")
    prefix = "0" * difficulty
    nonce = 0
    while True:
        text = data + str(nonce)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest.startswith(prefix):
            return nonce, digest
        nonce += 1


difficulty = 4
nonce, digest = mine("block1", difficulty)
print(f"difficulty={difficulty}, nonce={nonce}")
print(f"hash={digest}")
```

### 6. Корень дерева Меркла

**Вопрос:** Постройте корень дерева Меркла для списка из четырёх транзакций: начните с хэшей транзакций, затем хэшируйте склеенные пары соседних хэшей, пока не останется один корневой хэш. Если число элементов нечётное, продублируйте последний.

**Ответ:**

```python
import hashlib


def merkle_root(transactions):
    def hash_text(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    if not transactions:
        raise ValueError("Список транзакций пуст")
    level = [hash_text(transaction) for transaction in transactions]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            hash_text(level[index] + level[index + 1])
            for index in range(0, len(level), 2)
        ]
    return level[0]


transactions = ["tx1", "tx2", "tx3", "tx4"]
print("Merkle root:", merkle_root(transactions))
```

### 7. Угроза атаки 51 процента

**Вопрос:** Напишите функцию, определяющую, представляет ли пул угрозу при контроле более половины вычислительной мощности сети. Проверьте её на долях 0.3, 0.51, 0.49 и 0.6.

**Ответ:**

```python
def attack_threat(share):
    return share > 0.5


for share in (0.3, 0.51, 0.49, 0.6):
    result = "УГРОЗА (атака 51%)" if attack_threat(share) else "безопасно"
    print(f"Доля мощности {share:.0%}: {result}")
```

### 8. Tangle и подтверждение транзакций

**Вопрос:** Смоделируйте Tangle из шести транзакций, где каждая, кроме двух начальных, ссылается на две случайные различные предыдущие. Зафиксируйте random.seed(42) и выведите структуру подтверждений.

**Ответ:**

```python
import random


def create_tangle(count):
    random.seed(42)
    return [
        [] if index < 2 else random.sample(range(index), 2)
        for index in range(count)
    ]


tangle = create_tangle(6)
for index, confirmations in enumerate(tangle):
    result = confirmations if confirmations else "— (начальная)"
    print(f"Транзакция {index} подтверждает: {result}")
```

### 9. Время подтверждения в IOTA

**Вопрос:** По учебной модели время подтверждения обратно пропорционально числу транзакций: t = k / n. При k = 1000 вычислите условное время подтверждения для 10, 100 и 1000 транзакций.

**Ответ:**

```python
def confirmation_time(n, k=1000):
    if n <= 0:
        raise ValueError("Число транзакций должно быть положительным")
    return k / n


for n in (10, 100, 1000):
    print(f"n={n:4} транзакций -> время подтверждения = "
          f"{confirmation_time(n):.2f} усл.ед.")
```

### 10. Индексатор транзакций и баланса

**Вопрос:** По списку транзакций с полями «откуда», «куда», «сумма» верните все транзакции заданного адреса и его итоговый баланс: входящие минус исходящие.

**Ответ:**

```python
def index_address(transactions, address):
    selected = [
        transaction for transaction in transactions
        if transaction["from"] == address or transaction["to"] == address
    ]
    incoming = sum(
        transaction["amount"] for transaction in selected
        if transaction["to"] == address
    )
    outgoing = sum(
        transaction["amount"] for transaction in selected
        if transaction["from"] == address
    )
    return selected, incoming - outgoing


transactions = [
    {"from": "Alice", "to": "Bob", "amount": 50},
    {"from": "Bob", "to": "Alice", "amount": 20},
    {"from": "Alice", "to": "Carol", "amount": 10},
    {"from": "Bob", "to": "Carol", "amount": 5},
]

address = "Alice"
selected, balance = index_address(transactions, address)
print(f"Транзакции {address} ({len(selected)}):")
for transaction in selected:
    print(f"  {transaction['from']} -> {transaction['to']}: "
          f"{transaction['amount']}")
print(f"Баланс {address}: {balance}")
```

### 11. Статистика запросов по сабграфам

**Вопрос:** По логу запросов [(сабграф, количество), …] вычислите суммарное число запросов для каждого сабграфа, найдите самый нагруженный и общее число запросов.

**Ответ:**

```python
def subgraph_stats(log):
    totals = {}
    for subgraph, count in log:
        totals[subgraph] = totals.get(subgraph, 0) + count
    busiest = max(totals, key=totals.get) if totals else None
    return totals, busiest, sum(totals.values())


log = [
    ("uniswap", 10000), ("aave", 6000), ("compound", 4500),
    ("uniswap", 2500), ("aave", 2500),
]

totals, busiest, total = subgraph_stats(log)
for subgraph, count in totals.items():
    print(f"{subgraph}: {count:,} запросов")
print("Самый нагруженный:", busiest)
print(f"Всего запросов: {total:,}")
```

### 12. Упрощённая модель цифровой подписи

**Вопрос:** Смоделируйте упрощённую подпись на основе хэширования: sign формирует SHA-256 от сообщения и ключа, а verify проверяет подпись. Покажите, что при подмене сообщения проверка не проходит.

**Ответ:**

```python
import hashlib
import hmac


# Учебная модель с общим секретом, а не реализация ECDSA.
def sign(message, private_key):
    text = message + private_key
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify(message, private_key, signature):
    expected = sign(message, private_key)
    return hmac.compare_digest(expected, signature)


message = "Alice -> Bob: 50"
private_key = "training_key"
signature = sign(message, private_key)

print("Подпись:", signature)
print("Проверка верной подписи:", verify(message, private_key, signature))
print("Проверка при подмене сообщения:",
      verify("Alice -> Bob: 500", private_key, signature))
```

### 13. Кубиты и число состояний

**Вопрос:** Напишите функцию числа состояний и сравните квантовый и классический случаи для 1, 2, 8 и 127 кубитов.

**Ответ:**

```python
def quantum_states(n):
    if n < 0:
        raise ValueError("Число кубитов не может быть отрицательным")
    return 2 ** n


# 2**n — число базисных состояний квантового регистра.
# Классические n бит тоже имеют 2**n конфигураций,
# но в каждый момент находятся в одной из них.
for n in (1, 2, 8, 127):
    states = quantum_states(n)
    print(f"{n:3} кубит(ов): {states:,} базисных состояний | "
          f"классика: {n} бит, {states:,} конфигураций, одна в данный момент")
```

### 14. Классическая факторизация числа

**Вопрос:** Реализуйте классическую факторизацию — разложение числа на простые множители — и проверьте её на числах 15, 21 и 91.

**Ответ:**

```python
def factorize(n):
    if n < 1:
        raise ValueError("Число должно быть положительным")
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    if n > 1:
        factors.append(n)
    return factors


for n in (15, 21, 91):
    print(f"{n} = " + " x ".join(map(str, factorize(n))))
```

### 15. Экстраполяция роста числа кубитов

**Вопрос:** Для последовательности процессоров на 127 → 433 → 1121 кубит вычислите коэффициенты роста между поколениями, среднее арифметическое коэффициентов и прогноз числа кубитов следующего поколения.

**Ответ:**

```python
def growth_forecast(generations):
    if len(generations) < 2 or any(value <= 0 for value in generations):
        raise ValueError("Нужны минимум два положительных значения")
    ratios = [
        current / previous
        for previous, current in zip(generations, generations[1:])
    ]
    average = sum(ratios) / len(ratios)
    forecast = round(generations[-1] * average)
    return ratios, average, forecast


generations = [127, 433, 1121]
ratios, average, forecast = growth_forecast(generations)

print("Поколения кубитов:", generations)
print("Коэффициенты роста:", [round(ratio, 2) for ratio in ratios])
print(f"Средний темп роста: x{average:.2f}")
print(f"Прогноз следующего поколения: ~{forecast} кубитов")
```
