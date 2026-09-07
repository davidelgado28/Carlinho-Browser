# Security checklist

Do not ship the scaffold unchanged.

1. Use a Public Suffix List aware origin/site implementation for cookies.
2. Verify filter-list licensing and integrity.
3. Sign filter-list updates and update manifests.
4. Add code signing / notarization and Android/iOS signing.
5. Add SAST, dependency scanning and browser regression tests.
6. Pin GitHub Actions to immutable commit SHAs for a hardened release pipeline.
7. Publish Qt/Chromium and other third-party notices.
