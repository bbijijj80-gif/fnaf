// Custom Hooks for OS operations
// Similar to React hooks but for system-level operations

import { OSComponent } from '../core/index.js';

let currentComponent = null;
let hookIndex = 0;
const componentHooks = new Map();

export function useProcess(initialValue = null) {
  const component = currentComponent;
  if (!component) {
    throw new Error('useProcess must be called within a component');
  }

  const id = `${component.constructor.name}-${hookIndex++}`;
  
  if (!componentHooks.has(component)) {
    componentHooks.set(component, {});
  }

  const hooks = componentHooks.get(component);
  
  if (!hooks[id]) {
    hooks[id] = {
      value: initialValue,
      pid: Math.floor(Math.random() * 10000),
      status: 'running',
    };
  }

  return [
    hooks[id].value,
    (newValue) => {
      hooks[id].value = newValue;
      component.render();
    },
  ];
}

export function useMemory(initialSize = 1024) {
  const component = currentComponent;
  if (!component) {
    throw new Error('useMemory must be called within a component');
  }

  const id = `${component.constructor.name}-${hookIndex++}`;
  
  if (!componentHooks.has(component)) {
    componentHooks.set(component, {});
  }

  const hooks = componentHooks.get(component);
  
  if (!hooks[id]) {
    hooks[id] = {
      allocated: initialSize,
      used: 0,
      free: initialSize,
    };
  }

  return [
    hooks[id],
    (size) => {
      if (size > 0) {
        hooks[id].allocated += size;
        hooks[id].free += size;
      } else {
        const deallocate = Math.abs(size);
        hooks[id].allocated = Math.max(0, hooks[id].allocated - deallocate);
        hooks[id].free = Math.max(0, hooks[id].free - deallocate);
      }
      component.render();
    },
  ];
}

export function useEffect(callback, dependencies = []) {
  const component = currentComponent;
  if (!component) {
    throw new Error('useEffect must be called within a component');
  }

  const id = `${component.constructor.name}-effect-${hookIndex++}`;
  
  if (!componentHooks.has(component)) {
    componentHooks.set(component, {});
  }

  const hooks = componentHooks.get(component);
  
  const shouldRun = !hooks[id] || 
    dependencies.some((dep, i) => dep !== (hooks[id].deps?.[i]));

  if (shouldRun) {
    hooks[id] = { deps: dependencies };
    callback();
  }
}

export function setCurrentComponent(component) {
  currentComponent = component;
  hookIndex = 0;
}

export function resetHooks() {
  componentHooks.clear();
}
