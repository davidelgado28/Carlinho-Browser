# Carlinho Browser 

**Carlinho Browser** is a lightweight, customizable, privacy-conscious web browser built on top of **Electron** and the **Chromium Rendering Engine**. Designed for speed, minimalism, and safety, Carlinho provides an intuitive multi-tab interface with essential web browsing capabilities and integrated privacy hooks.

---

## 🌟 Key Features

- ⚡ **Chromium-Powered Speed:** Leveraging Chromium's state-of-the-art V8 engine and Blink renderer.
- 🗂️ **Multi-Tab Architecture:** Smooth, dynamic tab switching, creation, and management.
- 🛡️ **Privacy First:** Built-in "Do Not Track" (DNT) headers and isolated process model.
- 🔍 **Smart Navigation Bar:** Seamless URL resolution and instant Google search fallback.
- 🎨 **Sleek Modern UI:** Ergonomic dark design based on the Catppuccin color scheme.
- 📦 **Automated .exe Installer:** Continuous integration workflow via GitHub Actions to compile standalone Windows executables.

---

## 📁 Repository Architecture

```text
carlinho-browser/
├── .github/
│   └── workflows/
│       └── build.yml          # Automated CI/CD pipeline for generating .exe installers
├── assets/
│   └── icons/                 # App icon resources (.ico and .png)
├── src/
│   ├── main/                  # Electron Main Process (System level)
│   │   ├── main.js            # Window initialization, security hooks, and session setup
│   │   └── preload.js         # Context bridge between main process and renderer UI
│   └── renderer/              # Electron Renderer Process (Browser Shell UI)
│       ├── index.html         # Chrome layout structure (TabBar, Nav Controls, Webviews)
│       ├── renderer.js        # Dynamic tab manager, URL parser, and webview event handling
│       └── ui.css             # Theme variables and responsive styling
├── .gitignore                 # Files ignored by git (node_modules, build outputs)
├── package.json               # Node.js manifest, dependencies, and electron-builder configs
└── README.md                  # Complete project documentation
