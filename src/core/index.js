// React-like OS Core
// Inspired by React's architecture: Virtual DOM -> Reconciliation -> Real DOM
// Here: Virtual State -> Reconciliation -> System Calls

export class OSComponent {
  constructor(props) {
    this.props = props;
    this.state = {};
    this.children = [];
  }

  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.render();
  }

  render() {
    throw new Error('render() must be implemented');
  }
}

export function createElement(type, props = {}, ...children) {
  return {
    type,
    props: { ...props, children },
    __osElement: true,
  };
}

export const Fragment = ({ children }) => children;
