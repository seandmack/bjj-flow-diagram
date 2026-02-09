"""
Pytest configuration and shared fixtures for BJJ Flow Diagram tests
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, Page
import time
import os

# Base URL for testing - HTML file is in parent directory
BASE_URL = "http://localhost:8000/index.html"


@pytest.fixture(scope="session")
def browser():
    """
    Session-scoped browser instance.
    Launches once and reused across all tests.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Set to False to see browser during tests
            slow_mo=50      # Slow down actions by 50ms for easier debugging
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """
    Function-scoped page instance.
    Each test gets a fresh page.
    """
    page = browser.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state('networkidle')
    yield page
    page.close()


@pytest.fixture
def screenshot_on_failure(request, page):
    """
    Automatically capture screenshot on test failure.
    """
    yield
    if request.node.rep_call.failed:
        screenshot_dir = "test-reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = f"{screenshot_dir}/{request.node.name}.png"
        page.screenshot(path=screenshot_path)
        print(f"\nScreenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to make test result available to fixtures.
    Used by screenshot_on_failure fixture.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# Helper functions for tests
def wait_for_diagram_ready(page):
    """Wait for the diagram to be fully loaded and rendered."""
    page.wait_for_selector('#flow-diagram', state='visible')
    page.wait_for_selector('.position-node', state='visible')
    time.sleep(0.5)  # Additional wait for D3 transitions


def get_element_position(page, selector):
    """Get the bounding box of an element."""
    element = page.locator(selector)
    return element.bounding_box()


def check_overlap(box1, box2):
    """
    Check if two bounding boxes overlap.
    Returns True if they overlap, False otherwise.
    """
    if not box1 or not box2:
        return False
    
    # Check if boxes don't overlap
    no_overlap = (
        box1['x'] + box1['width'] <= box2['x'] or  # box1 is left of box2
        box2['x'] + box2['width'] <= box1['x'] or  # box2 is left of box1
        box1['y'] + box1['height'] <= box2['y'] or # box1 is above box2
        box2['y'] + box2['height'] <= box1['y']    # box2 is above box1
    )
    
    return not no_overlap
