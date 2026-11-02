# Лабораторная работа № 2

### 1. Классификация VR / AR / MR

**Вопрос:** Напишите функцию `classify(immersion, sees_real)`, которая определяет тип технологии: «полное» погружение и реальный мир не виден → VR; частичное погружение и мир виден → AR; иначе → MR. Проверьте на трёх наборах.

**Ответ:**

```python
def classify(immersion, sees_real):
    if immersion == "полное" and not sees_real:
        return "VR"
    elif immersion == "частичное" and sees_real:
        return "AR"
    return "MR"


print(classify("полное", False))     # VR
print(classify("частичное", True))    # AR
print(classify("полное", True))       # MR
```

### 2. Поле зрения FOV

**Вопрос:** Угол обзора (FOV) гарнитуры задаёт, какие объекты видны. Напишите функцию `in_fov(angle, fov)`: объект виден, если его угол не выходит за половину FOV в каждую сторону. Проверьте углы 10, 45, 60 при FOV = 110.

**Ответ:**

```python
def in_fov(angle, fov):
    return abs(angle) <= fov / 2


for angle in (10, 45, 60):
    print(f"угол {angle}° при FOV 110° -> {in_fov(angle, 110)}")
```

### 3. Расстояние в 3D-пространстве

**Вопрос:** Позиции контроллеров и объектов задаются координатами (x, y, z). Напишите функцию `distance(p1, p2)`, вычисляющую евклидово расстояние между двумя точками, и найдите расстояние от (0, 0, 0) до (1, 2, 2).

**Ответ:**

```python
import math


def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


print("Расстояние:", distance((0, 0, 0), (1, 2, 2)))  # 3.0
```

### 4. Задержка motion-to-photon

**Вопрос:** Задержка между движением головы и обновлением картинки (motion-to-photon) должна быть не выше 20 мс, иначе возможно укачивание. Напишите функцию `latency_ok(ms)` и проверьте значения 12, 20, 35 мс.

**Ответ:**

```python
def latency_ok(ms):
    return ms <= 20


for ms in (12, 20, 35):
    result = "комфортно" if latency_ok(ms) else "риск укачивания"
    print(f"{ms} мс -> {result}")
```

### 5. Градусы и радианы

**Вопрос:** Повороты головы часто задают в градусах, а математические функции работают с радианами. Напишите функцию `to_radians(deg)` и переведите 0, 90, 180 градусов.

**Ответ:**

```python
import math


def to_radians(deg):
    return deg * math.pi / 180


for deg in (0, 90, 180):
    print(f"{deg}° = {round(to_radians(deg), 3)} рад")
```

### 6. Нормализация вектора

**Вопрос:** Направление взгляда задаётся вектором, который нужно привести к единичной длине (нормализовать). Напишите функцию `normalize(v)` для 3D-вектора и нормализуйте (0, 3, 4).

**Ответ:**

```python
import math


def normalize(v):
    length = math.sqrt(sum(component ** 2 for component in v))
    if length == 0:
        raise ValueError("Нельзя нормализовать нулевой вектор")
    return tuple(component / length for component in v)


print(normalize((0, 3, 4)))  # (0.0, 0.6, 0.8)
```

### 7. Частота кадров FPS

**Вопрос:** Для комфортного VR желательно не менее 90 кадров в секунду. Напишите функцию `fps_ok(frames, seconds, target=90)`, возвращающую FPS и признак, достаточно ли его. Проверьте: 540 кадров за 6 секунд.

**Ответ:**

```python
def fps_ok(frames, seconds, target=90):
    if seconds <= 0:
        raise ValueError("Время должно быть больше нуля")
    fps = frames / seconds
    return fps, fps >= target


fps, comfortable = fps_ok(540, 6)
print(f"FPS = {fps}, комфортно для VR: {comfortable}")
```

### 8. Подбор устройства по бюджету

**Вопрос:** Дан прайс VR-устройств (словарь «модель → цена»). Напишите функцию `affordable(budget)`, которая вернёт список моделей не дороже бюджета. Проверьте для бюджета 35000 ₽.

**Ответ:**

```python
# Учебный пример прайса.
prices = {
    "Cardboard": 1000,
    "Quest 2": 30000,
    "Quest 3": 60000,
    "Vive Pro": 100000,
}


def affordable(budget):
    return [model for model, price in prices.items() if price <= budget]


print("До 35000 ₽:", affordable(35000))
# До 35000 ₽: ['Cardboard', 'Quest 2']
```

### 9. Подсчёт применений по областям

**Вопрос:** Дан список областей применения VR (с повторами). Постройте словарь-счётчик: сколько раз встретилась каждая область. Проверьте на списке [игры, медицина, игры, образование, медицина, игры].

**Ответ:**

```python
applications = [
    "игры", "медицина", "игры",
    "образование", "медицина", "игры",
]

counts = {}
for application in applications:
    counts[application] = counts.get(application, 0) + 1

print(counts)
# {'игры': 3, 'медицина': 2, 'образование': 1}
```

### 10. Самая популярная область

**Вопрос:** На основе того же списка напишите функцию `most_common(items)`, которая возвращает наиболее часто встречающийся элемент. Проверьте на списке применений.

**Ответ:**

```python
def most_common(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return max(counts, key=counts.get) if counts else None


applications = [
    "игры", "медицина", "игры",
    "образование", "медицина", "игры",
]

print("Чаще всего:", most_common(applications))  # игры
```

### 11. Плавная анимация

**Вопрос:** Чтобы объект плавно перемещался между кадрами, применяют линейную интерполяцию. Напишите функцию `lerp(a, b, t)`, где t от 0 до 1, и покажите позицию при t = 0, 0.5, 1 для отрезка от 0 до 10.

**Ответ:**

```python
def lerp(a, b, t):
    return a + (b - a) * t


for t in (0, 0.5, 1):
    print(f"t={t}: {lerp(0, 10, t)}")
```

### 12. Зона взаимодействия grab

**Вопрос:** Объект можно «взять», если рука ближе к нему, чем длина досягаемости. Используя функцию `distance` из задания 3, напишите `can_grab(hand, obj, reach=0.3)`. Проверьте на близком (0.1, 0.1, 0.1) и далёком (1, 1, 1) объектах.

**Ответ:**

```python
def can_grab(hand, obj, reach=0.3):
    return distance(hand, obj) <= reach


hand = (0, 0, 0)

print(can_grab(hand, (0.1, 0.1, 0.1)))  # True
print(can_grab(hand, (1, 1, 1)))        # False
```

### 13. Фильтр каталога по типу

**Вопрос:** Дан каталог устройств — список словарей с полями name и type (VR/AR). Напишите код, который отберёт названия только VR-устройств.

**Ответ:**

```python
catalog = [
    {"name": "Quest 3", "type": "VR"},
    {"name": "HoloLens 2", "type": "AR"},
    {"name": "Vive Pro", "type": "VR"},
]

vr_devices = [
    device["name"]
    for device in catalog
    if device["type"] == "VR"
]

print("VR-устройства:", vr_devices)
# VR-устройства: ['Quest 3', 'Vive Pro']
```

### 14. Суммарная задержка стриминга

**Вопрос:** При облачном VR полная задержка складывается из сетевой, задержки рендеринга и вывода на экран. Напишите функцию `total_latency(network, render, display)` и проверьте пригодность (≤ 20 мс) для значений 8, 6, 4 мс.

**Ответ:**

```python
def total_latency(network, render, display):
    return network + render + display


latency = total_latency(8, 6, 4)

print(f"Суммарная задержка: {latency} мс")  # 18 мс
print("Пригодно для VR:", latency <= 20)  # True
```

### 15. Мини-симуляция движения

**Вопрос:** Смоделируйте движение объекта: он движется со скоростью 2 единицы/сек при частоте 90 кадров/сек. За каждый кадр позиция растёт на speed·dt. Выведите позицию после первых трёх кадров.

**Ответ:**

```python
speed = 2
fps = 90
dt = 1 / fps
position = 0

for frame in range(1, 4):
    position += speed * dt
    print(f"Кадр {frame}: позиция = {position:.4f}")
```
