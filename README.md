# React-like OS

Операционная система с архитектурой в стиле React. Только исходный код, собирается с помощью Node.js.

## Структура проекта

```
react-os/
├── src/
│   ├── core/           # Ядро архитектуры (компоненты, createElement)
│   ├── hooks/          # Хуки для системных операций (useProcess, useMemory)
│   ├── kernel/         # Ядро ОС (планировщик, память, системные вызовы)
│   ├── components/     # UI компоненты (Terminal, WindowManager)
│   └── index.js        # Точка входа
├── build.js            # Скрипт сборки
├── package.json        # Конфигурация проекта
└── dist/               # Собранный бандл (генерируется)
    ├── react-os.bundle.js
    ├── react-os.bundle.min.js
    └── index.html
```

## Архитектура

Проект вдохновлён архитектурой React:

- **OSComponent** - базовый класс компонентов (аналог React.Component)
- **createElement** - создание виртуальных элементов системы
- **Хуки** - useProcess, useMemory, useEffect для управления состоянием
- **Виртуальное дерево** - рендеринг через дерево системных компонентов
- **Reconciliation** - согласование состояния и применение изменений

## Установка

```bash
npm install
```

## Сборка

```bash
npm run build
```

Или напрямую:

```bash
node build.js
```

## Запуск в браузере

Откройте `dist/index.html` в любом современном браузере.

## API

### Базовые компоненты

```javascript
import { OSComponent, createElement } from "./src/core/index.js";

class MyComponent extends OSComponent {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  render() {
    return createElement("div", {}, `Count: ${this.state.count}`);
  }
}
```

### Хуки

```javascript
import { useProcess, useMemory, useEffect } from "./src/hooks/index.js";

function SystemMonitor() {
  const [process, setProcess] = useProcess("init");
  const [memory, setMemory] = useMemory(1024);
  
  useEffect(() => {
    console.log("Component mounted");
  }, []);
  
  return createElement("div", {}, `PID: ${process.pid}`);
}
```

### Ядро

```javascript
import { Kernel } from "./src/kernel/index.js";

const kernel = new Kernel({});
const pid = kernel.createProcess("my-app", 5);
kernel.allocateMemory(512);
kernel.syscall("read", { file: "/etc/config" });
```

### Запуск ОС

```javascript
import { bootOS } from "./src/index.js";

const os = bootOS({ debug: true });
```

## Компоненты

- **Kernel** - управление процессами, памятью, системными вызовами
- **Terminal** - эмулятор терминала с историей команд
- **WindowManager** - оконный менеджер с поддержкой множественных окон
- **ProcessList** - список запущенных процессов
- **MemoryMonitor** - монитор использования памяти
- **Desktop** - рабочее окружение с иконками и панелью задач

## Сборка

Скрипт `build.js`:

1. Читает все исходные файлы из `src/`
2. Удаляет import/export инструкции
3. Объединяет в один бандл
4. Создаёт минифицированную версию
5. Генерирует HTML пример

Результат в папке `dist/`:
- `react-os.bundle.js` - полная версия (~15 KB)
- `react-os.bundle.min.js` - минифицированная (~11 KB)
- `index.html` - пример использования в браузере

## Лицензия

MIT
