from playwright.sync_api import sync_playwright
import time

BASE_URL = "file:///workspaces/bjj-flow-diagram/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE_URL)
    page.wait_for_selector('#flow-diagram')
    page.wait_for_selector('.position-node')
    time.sleep(0.5)

    subs = page.locator('[data-category="submission"]')
    print('initial submissions count:', subs.count())
    visible_names = page.evaluate("() => Array.from(document.querySelectorAll('[data-category=\"submission\"]')).filter(el=> el && el.textContent).map(el=>el.textContent.trim())")
    print('initial submission names sample:', visible_names[:5])

    # Click the header toggle
    toggle = page.locator('button.category-toggle[data-category="submission"]')
    print('toggle visible:', toggle.is_visible())
    toggle.click(force=True)
    time.sleep(0.8)

    # Check which submission nodes are still visible/opacity
    info = page.evaluate("() => Array.from(document.querySelectorAll('[data-category=\"submission\"]')).map(el => ({ text: el.textContent.trim(), display: window.getComputedStyle(el).display, visibility: window.getComputedStyle(el).visibility, opacity: window.getComputedStyle(el).opacity, bbox: el.getBoundingClientRect() }))")
    print('post-toggle submission info sample:', info[:10])

    browser.close()
