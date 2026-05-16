// OS Components - Similar to React components but for system UI
// These are functional and class components for building the OS interface

import { OSComponent, createElement } from '../core/index.js';
import { setCurrentComponent, useProcess, useMemory, useEffect } from '../hooks/index.js';

// Functional Component Example
export function ProcessList({ processes }) {
  return createElement(
    'div',
    { className: 'process-list' },
    createElement('h2', {}, 'Running Processes'),
    createElement('ul', {},
      ...processes.map(p => 
        createElement('li', { key: p.pid, className: `process-${p.status}` },
          `[${p.pid}] ${p.name} (Priority: ${p.priority})`
        )
      )
    )
  );
}

// Functional Component with Hooks
export function MemoryMonitor() {
  const [memory, setMemory] = useMemory(4096);
  
  useEffect(() => {
    console.log('Memory monitor initialized');
  }, []);
  
  const usagePercent = ((memory.used / memory.allocated) * 100).toFixed(2);
  
  return createElement(
    'div',
    { className: 'memory-monitor' },
    createElement('h3', {}, 'Memory Usage'),
    createElement('progress-bar', {
      value: usagePercent,
      max: 100,
      label: `${usagePercent}%`
    }),
    createElement('div', { className: 'stats' },
      `Allocated: ${memory.allocated}MB | Used: ${memory.used}MB | Free: ${memory.free}MB`
    )
  );
}

// Class Component Example
export class Terminal extends OSComponent {
  constructor(props) {
    super(props);
    this.state = {
      history: [],
      currentInput: '',
      isFocused: false,
    };
  }

  executeCommand(command) {
    const output = this.processCommand(command);
    this.setState({
      history: [...this.state.history, { input: command, output }],
      currentInput: '',
    });
  }

  processCommand(cmd) {
    const parts = cmd.trim().split(' ');
    const command = parts[0]?.toLowerCase();
    
    switch (command) {
      case 'help':
        return 'Available commands: help, clear, ps, mem, echo';
      case 'clear':
        this.setState({ history: [] });
        return '';
      case 'ps':
        return 'PID  NAME         STATUS\n1    init         running\n2    scheduler    running';
      case 'mem':
        return 'Total: 8192MB | Used: 2048MB | Free: 6144MB';
      case 'echo':
        return parts.slice(1).join(' ');
      default:
        return `Command not found: ${command}`;
    }
  }

  render() {
    setCurrentComponent(this);
    
    return createElement(
      'div',
      { className: 'terminal', focused: this.state.isFocused },
      createElement('div', { className: 'terminal-header' }, 'Terminal'),
      createElement('div', { className: 'terminal-body' },
        ...this.state.history.map((entry, i) =>
          createElement('div', { key: i, className: 'history-entry' },
            createElement('span', { className: 'prompt' }, `$ ${entry.input}`),
            entry.output ? createElement('span', { className: 'output' }, entry.output) : null
          )
        ),
        createElement('div', { className: 'input-line' },
          createElement('span', { className: 'prompt' }, '$ '),
          createElement('input', {
            value: this.state.currentInput,
            placeholder: 'Enter command...',
            onInput: (e) => this.setState({ currentInput: e.target.value }),
            onKeyPress: (e) => {
              if (e.key === 'Enter') {
                this.executeCommand(this.state.currentInput);
              }
            }
          })
        )
      )
    );
  }
}

// Window Manager Component
export class WindowManager extends OSComponent {
  constructor(props) {
    super(props);
    this.state = {
      windows: [],
      activeWindow: null,
      zIndex: 1,
    };
  }

  openWindow(title, content, options = {}) {
    const window = {
      id: Math.random().toString(36).substr(2, 9),
      title,
      content,
      x: options.x || 100,
      y: options.y || 100,
      width: options.width || 600,
      height: options.height || 400,
      zIndex: ++this.state.zIndex,
      minimized: false,
      maximized: false,
    };
    
    this.setState({
      windows: [...this.state.windows, window],
      activeWindow: window.id,
    });
    
    return window.id;
  }

  closeWindow(id) {
    this.setState({
      windows: this.state.windows.filter(w => w.id !== id),
      activeWindow: this.state.activeWindow === id ? null : this.state.activeWindow,
    });
  }

  focusWindow(id) {
    const window = this.state.windows.find(w => w.id === id);
    if (window) {
      window.zIndex = ++this.state.zIndex;
      this.setState({
        windows: [...this.state.windows],
        activeWindow: id,
      });
    }
  }

  render() {
    setCurrentComponent(this);
    
    return createElement(
      'div',
      { className: 'window-manager' },
      ...this.state.windows.map(win =>
        createElement('div', {
          key: win.id,
          className: `window ${win.id === this.state.activeWindow ? 'active' : ''}`,
          style: {
            left: win.x,
            top: win.y,
            width: win.width,
            height: win.height,
            zIndex: win.zIndex,
            display: win.minimized ? 'none' : 'block',
          },
          onClick: () => this.focusWindow(win.id),
        },
          createElement('div', { className: 'title-bar' },
            createElement('span', {}, win.title),
            createElement('div', { className: 'controls' },
              createElement('button', { onClick: () => {/* minimize */} }, '_'),
              createElement('button', { onClick: () => {/* maximize */} }, '□'),
              createElement('button', { onClick: () => this.closeWindow(win.id) }, '×')
            )
          ),
          createElement('div', { className: 'content' }, win.content)
        )
      )
    );
  }
}
