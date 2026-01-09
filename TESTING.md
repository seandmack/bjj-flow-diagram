# Testing Guide

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Install Chrome for Testing (if not already installed)

The postinstall script will attempt to install Chrome automatically. If it fails, you can install it manually:

```bash
npx puppeteer browsers install chrome@stable
```

**Alternative**: If you already have Chrome/Chromium installed on your system, the tests may use that instead.

### 3. Run Tests

```bash
npm test
```

## What's Included

This comprehensive test suite includes **80+ test cases** covering:

- ✅ Page load and rendering
- ✅ Difficulty filters (basic/intermediate/advanced)
- ✅ Category toggles (escape, counter, submission, sweep, pass, takedown)
- ✅ Position and technique detail views
- ✅ Zoom controls and interactions
- ✅ Responsive design
- ✅ Performance and stability

## Test Commands

```bash
# Run all tests
npm test

# Run tests in watch mode (auto-rerun on changes)
npm run test:watch

# Run with coverage report
npm run test:coverage

# Debug tests
npm run test:debug
```

## Troubleshooting

### Chrome Installation Issues

If you see errors about Chrome not being installed:

**Option 1**: Install Chrome manually
```bash
npx puppeteer browsers install chrome@stable
```

**Option 2**: Use system Chrome
The tests will automatically detect and use Chrome if it's installed on your system.

**Option 3**: Install Chromium
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install chromium
```

### Network Issues

If Chrome download fails with a 403 error, it may be a temporary network issue. Try:

1. Wait a few minutes and try again
2. Check your internet connection
3. Try downloading a specific version: `npx puppeteer browsers install chrome@120`

## File Structure

```
tests/
├── ui.test.js         # Main comprehensive test suite (80+ tests)
├── helpers.js         # Reusable test utilities
└── README.md          # Detailed testing documentation
```

## Learn More

See [tests/README.md](tests/README.md) for comprehensive documentation including:

- Detailed test coverage breakdown
- Helper function reference
- Writing new tests
- Advanced configuration
- CI/CD integration

## Running Tests in CI/CD

The tests are configured to run in headless mode by default, making them perfect for CI/CD pipelines. See the main test README for GitHub Actions example configuration.
