"""
Interaction tests - test user interactions with the diagram
Run with: pytest test_interactions.py
"""
import pytest
from conftest import wait_for_diagram_ready


@pytest.mark.interaction
def test_difficulty_filter_basic(page):
    """Test that Basic difficulty filter works."""
    wait_for_diagram_ready(page)
    
    # Click Basic button to toggle off
    basic_button = page.locator('button:has-text("Basic")')
    basic_button.click()
    page.wait_for_timeout(600)  # Wait for transition
    
    # Check that basic techniques are hidden
    basic_techniques = page.locator('[data-difficulty="basic"]')
    visible_count = sum(1 for tech in basic_techniques.all() if tech.is_visible())
    
    # Should be 0 or very few visible (some might be in transition)
    assert visible_count == 0, f"Expected 0 basic techniques visible, found {visible_count}"
    
    # Click again to toggle back on
    basic_button.click()
    page.wait_for_timeout(600)
    
    # Check that basic techniques are visible again
    visible_count = sum(1 for tech in basic_techniques.all() if tech.is_visible())
    assert visible_count > 0, "Basic techniques should be visible after toggling back on"


@pytest.mark.interaction
def test_click_position_shows_detail(page):
    """Test that clicking a position shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Click on Mount position
    mount = page.locator('text="Mount"').first
    mount.click()
    page.wait_for_timeout(300)
    
    # Check that position detail view is shown
    assert page.is_visible('#position-detail')
    assert page.is_visible('#position-name:has-text("Mount")')
    
    # Check back button exists
    assert page.is_visible('#position-back-btn')


@pytest.mark.interaction
def test_click_technique_shows_detail(page):
    """Test that clicking a technique shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Click on Armbar from Mount
    armbar = page.locator('text="Armbar from Mount"').first
    armbar.click()
    page.wait_for_timeout(300)
    
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
    
    # Click on a technique
    armbar = page.locator('text="Armbar from Mount"').first
    armbar.click()
    page.wait_for_timeout(300)
    
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
    initial_transform = page.locator('#flow-diagram g').get_attribute('transform')
    
    # Click zoom in button
    zoom_in = page.locator('button:has-text("➕")')
    zoom_in.click()
    page.wait_for_timeout(400)
    
    # Get new transform
    new_transform = page.locator('#flow-diagram g').get_attribute('transform')
    
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
    zoomed_transform = page.locator('#flow-diagram g').get_attribute('transform')
    
    # Click reset
    reset_button = page.locator('button:has-text("⟲")')
    reset_button.click()
    page.wait_for_timeout(600)
    
    # Get reset transform
    reset_transform = page.locator('#flow-diagram g').get_attribute('transform')
    
    # Transform should be different after reset
    assert zoomed_transform != reset_transform, "Reset did not change transform"


@pytest.mark.interaction
def test_category_filter_submissions(page):
    """Test that submission category filter works."""
    wait_for_diagram_ready(page)
    
    # Count visible submissions before toggle
    submissions = page.locator('[data-category="submission"]')
    initial_visible = sum(1 for sub in submissions.all() if sub.is_visible())
    
    assert initial_visible > 0, "No submissions visible initially"
    
    # Click submission toggle to hide
    submission_toggle = page.locator('.legend-item:has-text("Submission")')
    submission_toggle.click()
    page.wait_for_timeout(600)
    
    # Check submissions are hidden
    visible_after = sum(1 for sub in submissions.all() if sub.is_visible())
    assert visible_after == 0, f"Expected 0 submissions visible, found {visible_after}"
    
    # Toggle back on
    submission_toggle.click()
    page.wait_for_timeout(600)
    
    # Check submissions are visible again
    visible_restored = sum(1 for sub in submissions.all() if sub.is_visible())
    assert visible_restored > 0, "Submissions should be visible after toggling back"
