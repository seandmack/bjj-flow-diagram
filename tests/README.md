# BJJ Flow Diagram - UI Test Suite

Comprehensive Puppeteer-based UI tests for the Brazilian Jiu-Jitsu Flow Diagram interactive visualization.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Test Structure](#test-structure)
- [Helper Utilities](#helper-utilities)
- [Writing New Tests](#writing-new-tests)
- [Troubleshooting](#troubleshooting)

## Overview

This test suite uses **Puppeteer** and **Jest** to test all interactive features of the BJJ Flow Diagram:

- ✅ Page load and initial rendering
- ✅ Difficulty filter buttons (basic, intermediate, advanced)
- ✅ Category toggle buttons (escape, counter, submission, sweep, pass, takedown)
- ✅ Position detail views
- ✅ Technique detail views
- ✅ Zoom controls (+, -, reset)
- ✅ SVG zoom and pan behavior
- ✅ Responsive design (mobile/desktop)
- ✅ Filter combinations
- ✅ Performance and stability

## Setup

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

This will install:
- `puppeteer` - Headless Chrome browser automation
- `jest` - Testing framework
- `http-server` - Local development server (optional)

### First-Time Setup

No additional configuration needed! The tests are ready to run out of the box.

## Running Tests

### Run All Tests

```bash
npm test
```

### Run Tests in Watch Mode

Automatically re-run tests when files change:

```bash
npm run test:watch
```

### Run Tests with Coverage

Generate code coverage report:

```bash
npm run test:coverage
```

Coverage reports will be saved to the `coverage/` directory.

### Debug Tests

Run tests with Node debugger:

```bash
npm run test:debug
```

Then open `chrome://inspect` in Chrome and click "inspect" on the Node process.

### Run Specific Test Suite

Run only tests matching a pattern:

```bash
npx jest --testNamePattern="Difficulty Filter"
```

### Run Tests in Headed Mode

To see the browser while tests run (useful for debugging):

1. Edit `tests/ui.test.js`
2. Change `headless: 'new'` to `headless: false`
3. Run tests normally

## Test Coverage

The test suite includes **80+ test cases** organized into the following categories:

| Test Suite | Test Count | Description |
|------------|------------|-------------|
| Initial Page Load | 9 | Page rendering, initial state verification |
| Difficulty Filter Buttons | 6 | Filter switching, active state management |
| Category Toggle Buttons | 6 | Category toggling, multi-select behavior |
| Position Detail View | 5 | Navigation to position details, back navigation |
| Technique Detail View | 3 | Technique detail display and navigation |
| Zoom Controls | 4 | Zoom in, zoom out, reset functionality |
| SVG Zoom and Pan | 2 | Mouse wheel zoom, drag to pan |
| Responsive Behavior | 2 | Viewport resizing, mobile functionality |
| Legend | 2 | Legend display and content |
| Filter Combinations | 2 | Multiple filter interactions |
| Performance and Stability | 3 | Rapid interactions, error handling |

## Test Structure

### Directory Layout

```
tests/
├── README.md          # This file
├── ui.test.js         # Main test suite
└── helpers.js         # Reusable test utilities
```

### Main Test File: `ui.test.js`

The main test suite follows this structure:

```javascript
describe('BJJ Flow Diagram - UI Tests', () => {
  // Setup and teardown
  beforeAll()    // Launch browser
  afterAll()     // Close browser
  beforeEach()   // Create new page
  afterEach()    // Close page

  describe('Feature Category', () => {
    test('specific behavior', async () => {
      // Test implementation
    });
  });
});
```

### Test Lifecycle

1. **beforeAll**: Launch Puppeteer browser instance
2. **beforeEach**: Create new page, navigate to app, wait for diagram to render
3. **Test Execution**: Run individual test
4. **afterEach**: Close page
5. **afterAll**: Close browser

## Helper Utilities

The `helpers.js` file provides reusable functions for common test operations:

### Element Visibility

```javascript
await waitForVisible(page, '#diagram-container');
await waitForHidden(page, '#position-detail');
const visible = await isVisible(page, '#flow-diagram');
```

### Element State

```javascript
const hasActive = await hasClass(page, '.filter-btn', 'active');
const exists = await elementExists(page, '#zoom-controls');
```

### Filter State

```javascript
const activeFilters = await getActiveFilters(page);
const activeCategories = await getActiveCategories(page);
```

### Diagram Interaction

```javascript
await waitForDiagramRender(page);
const nodeCount = await countVisibleNodes(page);
const transform = await getZoomTransform(page);
```

### User Actions

```javascript
await clickAndWait(page, 'button[data-filter="advanced"]');
const text = await getTextContent(page, 'h1');
```

## Writing New Tests

### Example Test Template

```javascript
test('should do something specific', async () => {
  // 1. Perform action
  await clickAndWait(page, 'button.my-button');

  // 2. Wait for state change (if needed)
  await page.waitForTimeout(300);

  // 3. Verify result
  const isActive = await hasClass(page, 'button.my-button', 'active');
  expect(isActive).toBe(true);
});
```

### Best Practices

1. **Use helper functions**: Prefer `clickAndWait()` over raw `page.click()`
2. **Wait for rendering**: Use `waitForDiagramRender()` after navigation
3. **Add timeouts**: Use `page.waitForTimeout()` after state changes
4. **Clear test names**: Use descriptive names like "should show position detail when node is clicked"
5. **One assertion per test**: Keep tests focused on single behaviors
6. **Cleanup**: Don't rely on test order, each test should be independent

### Testing Checklist

When adding new features, test:

- ✅ Initial state
- ✅ User interaction (click, type, etc.)
- ✅ State change verification
- ✅ Visual feedback (classes, visibility)
- ✅ Navigation flow
- ✅ Error handling
- ✅ Edge cases

## Troubleshooting

### Tests Fail on CI/CD

**Issue**: Tests pass locally but fail in CI/CD pipeline

**Solution**: Ensure headless mode is enabled and add these Puppeteer args:

```javascript
browser = await puppeteer.launch({
  headless: 'new',
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage'
  ]
});
```

### Timeout Errors

**Issue**: Tests timeout waiting for elements

**Solution**: Increase timeout in `jest.config.js`:

```javascript
testTimeout: 60000 // 60 seconds
```

Or increase specific wait timeouts in helpers.

### Flaky Tests

**Issue**: Tests sometimes pass, sometimes fail

**Solution**: Add appropriate wait conditions:

```javascript
// Instead of fixed timeout:
await page.waitForTimeout(500);

// Use condition-based waits:
await page.waitForSelector('.element', { visible: true });
await waitForDiagramRender(page);
```

### Browser Not Launching

**Issue**: Puppeteer fails to launch browser

**Solution**: Install browser dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install -y chromium-browser

# Or use bundled Chromium
npx puppeteer browsers install chrome
```

### Tests Can't Find Elements

**Issue**: `page.$()` returns null

**Solution**:
1. Verify selector is correct
2. Ensure page has loaded: `await page.waitForSelector(selector)`
3. Check if element is dynamically created
4. Use `waitForDiagramRender()` for SVG elements

### Memory Issues

**Issue**: Tests consume too much memory

**Solution**: Run fewer tests in parallel:

```javascript
// jest.config.js
maxWorkers: 1, // or '50%'
```

Or close browser between test suites:

```javascript
afterAll(async () => {
  await browser.close();
  browser = null;
});
```

## Performance Tips

1. **Reuse browser instance**: Launch once per test suite, not per test
2. **Create fresh pages**: New page for each test (faster than clearing state)
3. **Parallelize tests**: Jest runs tests in parallel by default
4. **Skip unnecessary waits**: Use condition-based waits instead of fixed timeouts
5. **Disable unnecessary features**: Set `--disable-extensions`, `--disable-gpu` in args

## CI/CD Integration

### GitHub Actions Example

```yaml
name: UI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: test-screenshots
          path: tests/screenshots/
```

## Additional Resources

- [Puppeteer Documentation](https://pptr.dev/)
- [Jest Documentation](https://jestjs.io/)
- [Puppeteer Testing Patterns](https://pptr.dev/guides/testing)
- [D3.js Testing Guide](https://d3js.org/)

## Contributing

When adding new tests:

1. Follow existing test patterns
2. Use helper utilities when possible
3. Add descriptive test names
4. Update this README if adding new test categories
5. Ensure tests pass locally before committing

## License

MIT
