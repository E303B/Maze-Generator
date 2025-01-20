# Maze Generator
Базовая программа для генерации лабиринта, использующая библиотеку pygame. Я использовал алгоритм генерации лабиринта с [geekforgeeks](https://www.geeksforgeeks.org/random-acyclic-maze-generator-with-given-entry-and-exit-point/) с небольшими модификациями. Программа предназначена для базового освоения рабочих программ новичками.
 
## Настройки программы

Настройки программы хранятся в конфиге, написанном на [JSON](https://ru.wikipedia.org/wiki/JSON). Ниже я приведу все необходимые вам поля в конфиге("config.json"):

- **"tileColor"** - Цвет пустых клеток. Принимает кортежи формата "r,g,b"(без скобок!!!), или базовые цвета на английском (смотрите соотвествующую главу), регистронезависимо
- **"wallColor"** - Цвет стен. Принимает кортежи формата "r,g,b"(без скобок!!!), или базовые цвета на английском (смотрите соотвествующую главу), регистронезависимо
- **"startColor"** - Цвет начальной точки. Принимает кортежи формата "r,g,b"(без скобок!!!), или базовые цвета на английском (смотрите соотвествующую главу), регистронезависимо
- **"endColor"** - Цвет финиша. Принимает кортежи, формата "r,g,b"(без скобок!!!), или базовые цвета на английском (смотрите соотвествующую главу), регистронезависимо
- **"playerColor"** - Цвет игрока. Принимает кортежи формата "r,g,b"(без скобок!!!), или базовые цвета на английском (смотрите соотвествующую главу), регистронезависимо
-  **"hiddenColor"** - Цвет скрытых клеток. Принимает кортежи формата "r,g,b"(без скобок!!!), или базовые цвета на английском (смотрите соотвествующую главу), регистронезависимо
-  **"width"** - Количество столбцов, число. Не может быть меньше 10, программа не будет давать такое сделать(хотя, никто не мешает вам изменить код, отвечающий за это)
-  **"height"** - Количество рядов, число. Не может быть меньше 10, программа не будет давать такое сделать(хотя, никто не мешает вам изменить код, отвечающий за это)
-  **"generator"** - Объект, отвечающий за свойства генератор. На текущий момент, имеет только параметр **"randomSeed"** - строк или число, позволяющий форсировать сид генерации карты
-  **"playerSpeed"** - Число, влияющее на задержку движения игрока по формуле 1/x
-  **"lightMode"** - строка, влияющая на режим света и имеющая три позиции: "on" - клетки будут навсегда становится видимыми, "partial" - клетки будут видны только когда игрок видит их напрямую, "off" - клетки видны всегда

## Устройство кода

Расскажу немного об устройстве кода. Главным классом является ```main.py```, который запускает главный runner кода. У раннера есть поля для классов ```game.tilesystem.Tileset```, ```game.entitysystem.Entitysystem``` и ```game.lightsystem.Lightsystem```. Также, есть файл ```configloader.py```, который превращает конфиг в словарь, файл ```game/generator.py```, ответстенный за создание лабиринта, а также файл ```defines/colors.py```, который содержит несколько определений и функций для цвета

## Перечень поддерживаемых цветов

- **"red"** - RGB(255,0,0)
- **"black"** - RGB(0,0,0)
- **"white"** - RGB(255,255,255)
- **"green"** - RGB(0,255,0)
- **"blue"** - RGB(0,0,255)
- **"yellow"** - RGB(255,255,0)
- **"cyan"** - RGB(0,224,255)
- **"dark_gray"** - RGB(42,42,42)

## Полезные ссылки

- https://metanit.com/web/javascript/11.1.php - почитать про JSON
- https://ru.wikipedia.org/wiki/RGB - почитать про RGB
- https://www.geeksforgeeks.org/pygame-tutorial/ - почитать про PyGame
- https://ru.wikipedia.org/wiki/Стек - почитать про стек
- https://en.wikipedia.org/wiki/Maze_generation_algorithm - почитать про алгоритмы генерации лабиринтов(АНГ)

## Примеры генерации

![1](https://github.com/E303B/Maze-Generator/blob/main/img/example1.png)

![2](https://github.com/E303B/Maze-Generator/blob/main/img/example2.png)

![3](https://github.com/E303B/Maze-Generator/blob/main/img/example3.png)
