/**
 * Test Helper Utilities for BJJ Flow Diagram UI Tests
 * Provides reusable functions for common test operations
 */

/**
 * Wait for an element to be visible on the page
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @param {number} timeout - Maximum wait time in ms
 */
async function waitForVisible(page, selector, timeout = 5000) {
  await page.waitForSelector(selector, { visible: true, timeout });
}

/**
 * Wait for an element to be hidden on the page
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @param {number} timeout - Maximum wait time in ms
 */
async function waitForHidden(page, selector, timeout = 5000) {
  await page.waitForSelector(selector, { hidden: true, timeout });
}

/**
 * Check if an element is visible
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @returns {Promise<boolean>} True if visible, false otherwise
 */
async function isVisible(page, selector) {
  try {
    const element = await page.$(selector);
    if (!element) return false;

    const box = await element.boundingBox();
    return box !== null;
  } catch (error) {
    return false;
  }
}

/**
 * Check if an element has a specific class
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @param {string} className - Class name to check
 * @returns {Promise<boolean>} True if class exists, false otherwise
 */
async function hasClass(page, selector, className) {
  return await page.evaluate(
    (sel, cls) => {
      const element = document.querySelector(sel);
      return element ? element.classList.contains(cls) : false;
    },
    selector,
    className
  );
}

/**
 * Get all active filter buttons
 * @param {Page} page - Puppeteer page object
 * @returns {Promise<string[]>} Array of active filter values
 */
async function getActiveFilters(page) {
  return await page.evaluate(() => {
    const activeButtons = Array.from(
      document.querySelectorAll('.filter-btn.active')
    );
    return activeButtons.map(btn => btn.dataset.filter);
  });
}

/**
 * Get all active category toggles
 * @param {Page} page - Puppeteer page object
 * @returns {Promise<string[]>} Array of active category values
 */
async function getActiveCategories(page) {
  return await page.evaluate(() => {
    const activeToggles = Array.from(
      document.querySelectorAll('.category-toggle.active')
    );
    return activeToggles.map(btn => btn.dataset.category);
  });
}

/**
 * Count visible SVG nodes in the diagram
 * @param {Page} page - Puppeteer page object
 * @returns {Promise<number>} Number of visible nodes
 */
async function countVisibleNodes(page) {
  return await page.evaluate(() => {
    const nodes = document.querySelectorAll('#flow-diagram .node');
    return Array.from(nodes).filter(node => {
      const display = window.getComputedStyle(node).display;
      const opacity = window.getComputedStyle(node).opacity;
      return display !== 'none' && opacity !== '0';
    }).length;
  });
}

/**
 * Get current zoom transform values
 * @param {Page} page - Puppeteer page object
 * @returns {Promise<{x: number, y: number, k: number}>} Transform values
 */
async function getZoomTransform(page) {
  return await page.evaluate(() => {
    const g = document.querySelector('#flow-diagram g');
    if (!g) return { x: 0, y: 0, k: 1 };

    const transform = g.getAttribute('transform');
    if (!transform) return { x: 0, y: 0, k: 1 };

    // Parse transform string: "translate(x,y) scale(k)"
    const translateMatch = transform.match(/translate\(([^,]+),([^)]+)\)/);
    const scaleMatch = transform.match(/scale\(([^)]+)\)/);

    return {
      x: translateMatch ? parseFloat(translateMatch[1]) : 0,
      y: translateMatch ? parseFloat(translateMatch[2]) : 0,
      k: scaleMatch ? parseFloat(scaleMatch[1]) : 1
    };
  });
}

/**
 * Wait for diagram to finish rendering
 * @param {Page} page - Puppeteer page object
 * @param {number} timeout - Maximum wait time in ms
 */
async function waitForDiagramRender(page, timeout = 3000) {
  // Wait for SVG to exist and have child elements
  await page.waitForFunction(
    () => {
      const svg = document.querySelector('#flow-diagram');
      const nodes = document.querySelectorAll('#flow-diagram .node');
      return svg && nodes.length > 0;
    },
    { timeout }
  );

  // Add small delay to ensure rendering is complete
  await page.waitForTimeout(500);
}

/**
 * Click and wait for navigation/state change
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector to click
 * @param {number} waitTime - Time to wait after click (ms)
 */
async function clickAndWait(page, selector, waitTime = 300) {
  await page.click(selector);
  await page.waitForTimeout(waitTime);
}

/**
 * Get text content of an element
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @returns {Promise<string>} Text content
 */
async function getTextContent(page, selector) {
  return await page.evaluate(sel => {
    const element = document.querySelector(sel);
    return element ? element.textContent.trim() : '';
  }, selector);
}

/**
 * Check if element exists in DOM
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @returns {Promise<boolean>} True if exists, false otherwise
 */
async function elementExists(page, selector) {
  const element = await page.$(selector);
  return element !== null;
}

/**
 * Get count of elements matching selector
 * @param {Page} page - Puppeteer page object
 * @param {string} selector - CSS selector
 * @returns {Promise<number>} Count of matching elements
 */
async function getElementCount(page, selector) {
  return await page.evaluate(sel => {
    return document.querySelectorAll(sel).length;
  }, selector);
}

module.exports = {
  waitForVisible,
  waitForHidden,
  isVisible,
  hasClass,
  getActiveFilters,
  getActiveCategories,
  countVisibleNodes,
  getZoomTransform,
  waitForDiagramRender,
  clickAndWait,
  getTextContent,
  elementExists,
  getElementCount
};
