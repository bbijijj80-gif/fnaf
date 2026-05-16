// Build script for React-like OS
// Bundles all source files into a single distributable file

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SRC_DIR = join(__dirname, 'src');
const DIST_DIR = join(__dirname, 'dist');

// Simple bundler that concatenates and processes ES modules
function bundle() {
  console.log('🔨 Building React-like OS...\n');
  
  // Create dist directory if it doesn't exist
  if (!existsSync(DIST_DIR)) {
    mkdirSync(DIST_DIR, { recursive: true });
  }
  
  // Read all source files
  const files = [
    'src/core/index.js',
    'src/hooks/index.js',
    'src/kernel/index.js',
    'src/components/index.js',
    'src/index.js',
  ];
  
  let bundledCode = `// React-like OS - Bundled Distribution\n`;
  bundledCode += `// Generated at: ${new Date().toISOString()}\n\n`;
  bundledCode += `// ============================================\n\n`;
  
  files.forEach(file => {
    const filePath = join(__dirname, file);
    try {
      const content = readFileSync(filePath, 'utf-8');
      
      // Remove import statements for the bundled version
      const withoutImports = content.replace(/^import\s+[\s\S]*?from\s+['"].*?['"];?\s*/gm, '');
      
      // Remove export keywords (keep the declarations)
      const withoutExports = withoutImports.replace(/\bexport\s+/g, '');
      
      bundledCode += `// ===== ${file} =====\n\n`;
      bundledCode += withoutExports;
      bundledCode += `\n\n`;
    } catch (error) {
      console.error(`Error reading ${file}:`, error.message);
    }
  });
  
  // Add bootstrap code
  bundledCode += `
// ============================================
// Bootstrap
// ============================================

// Auto-execute boot function in browser environment
if (typeof window !== 'undefined') {
  console.log('React-like OS loaded in browser');
  window.ReactOS = {
    boot: bootOS,
    Kernel,
    createElement,
    OSComponent,
  };
}

// Export for Node.js environment
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    bootOS,
    Kernel,
    Desktop,
    Terminal,
    WindowManager,
    ProcessList,
    MemoryMonitor,
    createElement,
    OSComponent,
    useProcess,
    useMemory,
    useEffect,
  };
}
`;
  
  // Write bundled file
  const outputPath = join(DIST_DIR, 'react-os.bundle.js');
  writeFileSync(outputPath, bundledCode);
  
  console.log(`✅ Build complete!`);
  console.log(`📦 Output: ${outputPath}`);
  console.log(`📊 Size: ${(Buffer.byteLength(bundledCode, 'utf-8') / 1024).toFixed(2)} KB\n`);
  
  // Also create a minified version
  const minified = bundledCode
    .replace(/\/\*[\s\S]*?\*\//g, '')  // Remove multi-line comments
    .replace(/\/\/.*$/gm, '')          // Remove single-line comments
    .replace(/^\s*$/gm, '')            // Remove empty lines
    .replace(/\s+/g, ' ');             // Collapse whitespace
  
  const minifiedPath = join(DIST_DIR, 'react-os.bundle.min.js');
  writeFileSync(minifiedPath, minified);
  
  console.log(`🗜️  Minified: ${minifiedPath}`);
  console.log(`📊 Size: ${(Buffer.byteLength(minified, 'utf-8') / 1024).toFixed(2)} KB\n`);
  
  // Create HTML example
  const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>React-like OS</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #1a1a2e;
      color: #eee;
      overflow: hidden;
    }
    .os-desktop {
      width: 100vw;
      height: 100vh;
      position: relative;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .desktop-icons {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
    .desktop-icon {
      width: 80px;
      text-align: center;
      cursor: pointer;
      padding: 10px;
      border-radius: 8px;
      transition: background 0.2s;
    }
    .desktop-icon:hover {
      background: rgba(255,255,255,0.1);
    }
    .desktop-icon img {
      width: 48px;
      height: 48px;
      margin-bottom: 5px;
    }
    .taskbar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 48px;
      background: rgba(0,0,0,0.8);
      display: flex;
      align-items: center;
      padding: 0 10px;
      gap: 10px;
    }
    .start-menu {
      padding: 8px 16px;
      background: #4a9eff;
      border: none;
      border-radius: 4px;
      color: white;
      cursor: pointer;
      font-weight: bold;
    }
    .taskbar-apps {
      flex: 1;
      display: flex;
      gap: 5px;
    }
    .taskbar-item {
      padding: 6px 12px;
      background: rgba(255,255,255,0.1);
      border-radius: 4px;
      cursor: pointer;
      font-size: 13px;
    }
    .system-tray {
      display: flex;
      gap: 15px;
      padding: 0 10px;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script src="react-os.bundle.js"></script>
  <script>
    // Boot the OS when page loads
    document.addEventListener('DOMContentLoaded', () => {
      console.log('Starting React-like OS...');
      const os = ReactOS.boot({ debug: true });
      console.log('OS instance:', os);
    });
  </script>
</body>
</html>
`;
  
  const htmlPath = join(DIST_DIR, 'index.html');
  writeFileSync(htmlPath, htmlContent);
  
  console.log(`🌐 HTML Example: ${htmlPath}\n`);
  console.log('✨ Build finished successfully!\n');
}

// Run build
bundle();
