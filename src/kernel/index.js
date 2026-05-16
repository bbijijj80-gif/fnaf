// Kernel - The heart of the OS
// Manages processes, memory, and system calls

import { OSComponent, createElement } from '../core/index.js';
import { setCurrentComponent } from '../hooks/index.js';

export class Kernel extends OSComponent {
  constructor(props) {
    super(props);
    this.state = {
      processes: [],
      memory: { total: 8192, used: 0, free: 8192 },
      filesystem: {},
      syscalls: 0,
    };
    this.pidCounter = 1;
  }

  createProcess(name, priority = 1) {
    const process = {
      pid: this.pidCounter++,
      name,
      priority,
      status: 'running',
      memory: 0,
      createdAt: Date.now(),
    };
    
    this.setState({
      processes: [...this.state.processes, process],
    });
    
    return process.pid;
  }

  killProcess(pid) {
    const process = this.state.processes.find(p => p.pid === pid);
    if (process) {
      process.status = 'terminated';
      this.setState({
        processes: this.state.processes.filter(p => p.pid !== pid),
      });
    }
  }

  allocateMemory(size) {
    if (size > this.state.memory.free) {
      throw new Error('Not enough memory');
    }
    
    this.setState({
      memory: {
        ...this.state.memory,
        used: this.state.memory.used + size,
        free: this.state.memory.free - size,
      },
    });
  }

  syscall(name, args) {
    this.setState({ syscalls: this.state.syscalls + 1 });
    console.log(`[SYSCALL] ${name}(${JSON.stringify(args)})`);
    return { success: true, result: null };
  }

  render() {
    setCurrentComponent(this);
    
    return createElement(
      'kernel',
      { id: 'main-kernel' },
      createElement('memory-manager', { memory: this.state.memory }),
      createElement('process-scheduler', { processes: this.state.processes }),
      createElement('filesystem', { fs: this.state.filesystem }),
      createElement('syscall-handler', { count: this.state.syscalls })
    );
  }
}

export class ProcessScheduler extends OSComponent {
  constructor(props) {
    super(props);
    this.state = { currentProcess: null, queue: [] };
  }

  schedule(processes) {
    const sorted = [...processes].sort((a, b) => b.priority - a.priority);
    this.setState({
      queue: sorted,
      currentProcess: sorted[0] || null,
    });
  }

  render() {
    setCurrentComponent(this);
    
    return createElement(
      'scheduler',
      { 
        current: this.state.currentProcess?.name || 'idle',
        queueLength: this.state.queue.length 
      }
    );
  }
}

export class MemoryManager extends OSComponent {
  constructor(props) {
    super(props);
    this.state = { heap: [], stack: [] };
  }

  allocate(size, type = 'heap') {
    const block = {
      id: Math.random().toString(36).substr(2, 9),
      size,
      type,
      allocated: Date.now(),
    };
    
    this.setState({
      [type]: [...this.state[type], block],
    });
    
    return block.id;
  }

  render() {
    setCurrentComponent(this);
    
    return createElement(
      'memory',
      { 
        heapSize: this.state.heap.length,
        stackSize: this.state.stack.length 
      }
    );
  }
}
