"""
Interaction tests - test user interactions with the diagram
Run with: pytest test_interactions.py
"""
import pytest
from conftest import wait_for_diagram_ready


@pytest.mark.interaction
def test_difficulty_filter_basic(page):
    """Test that difficulty filters behave cumulatively: basic -> intermediate -> advanced."""
    wait_for_diagram_ready(page)

    basic_techniques = page.locator('[data-difficulty="basic"]')
    intermediate_techniques = page.locator('[data-difficulty="intermediate"]')
    advanced_techniques = page.locator('[data-difficulty="advanced"]')

    # Initial state should be basic filter
    assert sum(1 for tech in basic_techniques.all() if tech.is_visible()) > 0, "Basics should be visible initially"
    assert sum(1 for tech in intermediate_techniques.all() if tech.is_visible()) == 0, "Intermediate should not be visible under basic filter"
    assert sum(1 for tech in advanced_techniques.all() if tech.is_visible()) == 0, "Advanced should not be visible under basic filter"

    # Select intermediate filter: basic + intermediate visible
    page.locator('button:has-text("Intermediate")').click()
    page.wait_for_timeout(800)

    assert sum(1 for tech in basic_techniques.all() if tech.is_visible()) > 0, "Basics should still be visible under intermediate filter"
    assert sum(1 for tech in intermediate_techniques.all() if tech.is_visible()) > 0, "Intermediate techniques should be visible under intermediate filter"
    assert sum(1 for tech in advanced_techniques.all() if tech.is_visible()) == 0, "Advanced should not be visible under intermediate filter"

    # Select advanced filter: all difficulties visible
    page.locator('button:has-text("Advanced")').click()
    page.wait_for_timeout(800)

    assert sum(1 for tech in basic_techniques.all() if tech.is_visible()) > 0
    assert sum(1 for tech in intermediate_techniques.all() if tech.is_visible()) > 0
    assert sum(1 for tech in advanced_techniques.all() if tech.is_visible()) > 0


@pytest.mark.interaction
def test_click_position_shows_detail(page):
    """Test that clicking a position shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Click on Mount position
    page.wait_for_selector('g.position-node:has-text("Mount")', state='visible', timeout=5000)
    mount = page.locator('g.position-node:has-text("Mount")').first
    mount.click(force=True)
    page.wait_for_timeout(500)
    
    # Check that position detail view is shown
    assert page.is_visible('#position-detail')
    assert page.is_visible('#position-name:has-text("Mount")')
    
    # Check back button exists
    assert page.is_visible('#position-back-btn')


@pytest.mark.interaction
def test_click_technique_shows_detail(page):
    """Test that clicking a technique shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Click on Armbar from Mount (use data-id attribute for stability)
    page.wait_for_selector('g.technique-node[data-id="armbar-from-mount"]', state='visible', timeout=5000)
    armbar = page.locator('g.technique-node[data-id="armbar-from-mount"]').first
    armbar.click(force=True)
    page.wait_for_timeout(500)
    
    # Check that technique detail view is shown
    assert page.is_visible('#technique-detail')
    assert page.is_visible('#technique-name:has-text("Armbar from Mount")')
    
    # Check that steps are shown
    assert page.is_visible('#technique-steps')
    steps = page.locator('#technique-steps li')
    assert steps.count() > 0, "No steps shown for technique"


@pytest.mark.interaction
def test_back_button_returns_to_diagram(page):
    """Test that back button returns from detail view to diagram."""
    wait_for_diagram_ready(page)
    
    # Click on a technique (use id selector)
    page.wait_for_selector('g.technique-node[data-id="armbar-from-mount"]', state='visible', timeout=5000)
    armbar = page.locator('g.technique-node[data-id="armbar-from-mount"]').first
    armbar.click(force=True)
    page.wait_for_timeout(500)
    
    # Verify detail view is shown
    assert page.is_visible('#technique-detail')
    
    # Click back button
    back_button = page.locator('#technique-back-btn')
    back_button.click()
    page.wait_for_timeout(300)
    
    # Verify back on diagram view
    assert page.is_visible('#flow-diagram')
    assert not page.is_visible('#technique-detail')


@pytest.mark.interaction
def test_zoom_in_button(page):
    """Test that zoom in button works."""
    wait_for_diagram_ready(page)
    
    # Get initial transform
    initial_transform = page.locator('#flow-diagram g').first.get_attribute('transform')
    
    # Click zoom in button
    zoom_in = page.locator('button:has-text("➕")')
    zoom_in.click()
    page.wait_for_timeout(400)
    
    # Get new transform
    new_transform = page.locator('#flow-diagram g').first.get_attribute('transform')
    
    # Transform should have changed
    assert initial_transform != new_transform, "Zoom in did not change transform"


@pytest.mark.interaction
def test_zoom_reset_button(page):
    """Test that reset button works."""
    wait_for_diagram_ready(page)
    
    # Zoom in a few times
    zoom_in = page.locator('button:has-text("➕")')
    zoom_in.click()
    page.wait_for_timeout(200)
    zoom_in.click()
    page.wait_for_timeout(200)
    
    # Get zoomed transform
    zoomed_transform = page.locator('#flow-diagram g').first.get_attribute('transform')
    
    # Click reset
    reset_button = page.locator('button:has-text("⟲")')
    reset_button.click()
    page.wait_for_timeout(600)
    
    # Get reset transform
    reset_transform = page.locator('#flow-diagram g').first.get_attribute('transform')
    
    # Transform should be different after reset
    assert zoomed_transform != reset_transform, "Reset did not change transform"


@pytest.mark.interaction
def test_category_filter_submissions(page):
    """Test that submission category filter works."""
    wait_for_diagram_ready(page)
    
    # Count visible submission technique nodes before toggle
    submissions = page.locator('.technique-node[data-category="submission"]')
    initial_visible = sum(1 for sub in submissions.all() if sub.is_visible())
    
    assert initial_visible > 0, "No submissions visible initially"
    
    # Click submission toggle to hide
    submission_toggle = page.locator('button.category-toggle[data-category="submission"]')
    submission_toggle.click(force=True)
    # wait until no submission nodes remain in the DOM (they should be removed during filtering)
    page.wait_for_function(
        "selector => document.querySelectorAll(selector).length === 0",
        arg=".technique-node[data-category=\"submission\"]",
        timeout=5000
    )
    
    # verify none are visible just in case (use a fresh locator)
    visible_after = sum(1 for sub in page.locator('.technique-node[data-category="submission"]').all() if sub.is_visible())
    assert visible_after == 0, f"Expected 0 submissions visible, found {visible_after}"
    
    # Toggle back on and wait for at least one node to reappear in the DOM
    submission_toggle.click()
    page.wait_for_function(
        "selector => document.querySelectorAll(selector).length > 0",
        arg=".technique-node[data-category=\"submission\"]",
        timeout=5000
    )
    # Check submissions are visible again
    visible_restored = sum(1 for sub in submissions.all() if sub.is_visible())
    assert visible_restored > 0, "Submissions should be visible after toggling back"
