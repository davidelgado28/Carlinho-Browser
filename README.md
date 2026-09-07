# Carlinho Browser - base architecture

Monorepo scaffold for a privacy-first browser.

- `core/`: shared C++ privacy policy primitives.
- `desktop/`: native desktop shell using Qt 6 + Qt WebEngine (Chromium).
- `mobile/`: React Native UI plus native WebView adapters.
- `rules/`: placeholder block-list inputs.
- `.github/workflows/release.yml`: tag-driven CI/CD.

This is a foundation, not a production-hardened browser. Before distribution:
- pin third-party dependencies/actions;
- add code signing, notarization and Android/iOS signing;
- implement secure filter-list updates and signature verification;
- add browser security regression tests;
- replace Linux staging with a real AppImage build;
- implement PSL-aware site comparison for cookie policy;
- publish complete third-party license/notice files.
