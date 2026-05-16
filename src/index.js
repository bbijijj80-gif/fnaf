// Main entry point for React-like OS
// This is where the OS boots up and initializes all components

import { Kernel } from './kernel/index.js';
import { Terminal, WindowManager, ProcessList, MemoryMonitor } from './components/index.js';
import { createElement } from './core/index.js';

// Desktop Environment Component
class Desktop extends Kernel {
  constructor(props) {
    super(props);
    this.state = {
      ...this.state,
      desktop: {
        icons: [
          { id: 'terminal', name: 'Terminal', type: 'app' },
          { id: 'files', name: 'File Manager', type: 'app' },
          { id: 'settings', name: 'Settings', type: 'app' },
        ],
        wallpaper: '/assets/wallpaper.png',
      },
      taskbar: {
        apps: [],
        startTime: Date.now(),
      },
    };
  }

  launchApp(appId) {
    const app = this.state.desktop.icons.find(i => i.id === appId);
    if (app) {
      const pid = this.createProcess(app.name, 5);
      this.setState({
        taskbar: {
          ...this.state.taskbar,
          apps: [...this.state.taskbar.apps, { ...app, pid }],
        },
      });
      return pid;
    }
  }

  render() {
    return createElement(
      'desktop',
      { className: 'os-desktop' },
      createElement('window-manager', {}),
      createElement('div', { className: 'desktop-icons' },
        ...this.state.desktop.icons.map(icon =>
          createElement('div', { 
            key: icon.id, 
            className: 'desktop-icon',
            onDoubleClick: () => this.launchApp(icon.id)
          },
            createElement('img', { src: `/icons/${icon.id}.png` }),
            createElement('span', {}, icon.name)
          )
        )
      ),
      createElement('div', { className: 'taskbar' },
        createElement('button', { className: 'start-menu' }, 'Start'),
        createElement('div', { className: 'taskbar-apps' },
          ...this.state.taskbar.apps.map(app =>
            createElement('div', { 
              key: app.pid, 
              className: 'taskbar-item',
              onClick: () => {/* focus window */}
            }, app.name)
          )
        ),
        createElement('div', { className: 'system-tray' },
          createElement('clock', {}),
          createElement('volume', {}),
          createElement('network', {})
        )
      )
    );
  }
}

// Boot the OS
export function bootOS(options = {}) {
  console.log('[OS] Booting React-like OS...');
  
  const os = new Desktop({
    debug: options.debug || false,
    safeMode: options.safeMode || false,
  });
  
  console.log('[OS] Kernel initialized');
  console.log('[OS] Loading components...');
  
  // Initialize kernel services
  os.createProcess('init', 10);
  os.createProcess('scheduler', 9);
  os.createProcess('memory-manager', 8);
  
  console.log('[OS] System ready!');
  
  return os;
}

// Export everything for external use
export {
  Kernel,
  Terminal,
  WindowManager,
  ProcessList,
  MemoryMonitor,
  Desktop,
};

export * from './core/index.js';
export * from './hooks/index.js';
export * from './kernel/index.js';
export * from './components/index.js';
