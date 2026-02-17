"""
Interaction tests - test user interactions with the diagram
Run with: pytest test_interactions.py
"""
import pytest
from conftest import wait_for_diagram_ready


@pytest.mark.interaction
def test_difficulty_filter_basic(page):
    """Test that difficulty filter increases techniques shown cumulatively."""
    wait_for_diagram_ready(page)
    
    # Count techniques with Basic filter (should show only basic)
    basic_button = page.locator('button:has-text("Basic")')
    assert basic_button.locator('..').evaluate('el => el.querySelector(".filter-btn.active")?.textContent') == 'Basic' or \
           basic_button.evaluate('el => el.classList.contains("active")')
    
    basic_techniques = page.locator('.technique-node')
    basic_count = basic_techniques.count()
    assert basic_count > 0, "Should have at least some basic techniques visible"
    
    # Switch to Intermediate - should show basic AND intermediate techniques
    intermediate_button = page.locator('button:has-text("Intermediate")')
    intermediate_button.click()
    page.wait_for_timeout(600)  # Wait for transition
    
    intermediate_techniques = page.locator('.technique-node')
    intermediate_count = intermediate_techniques.count()
    assert intermediate_count >= basic_count, \
        f"Intermediate filter should show at least as many techniques as basic. Basic: {basic_count}, Intermediate: {intermediate_count}"
    
    # Switch to Advanced - should show all techniques
    advanced_button = page.locator('button:has-text("Advanced")')
    advanced_button.click()
    page.wait_for_timeout(600)
    
    advanced_techniques = page.locator('.technique-node')
    advanced_count = advanced_techniques.count()
    assert advanced_count >= intermediate_count, \
        f"Advanced filter should show at least as many techniques as intermediate. Intermediate: {intermediate_count}, Advanced: {advanced_count}"


@pytest.mark.interaction
def test_click_position_shows_detail(page):
    """Test that clicking a position shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Click on Mount position using SVG text
    mount = page.locator('svg text:has-text("Mount")').first
    if mount.count() > 0:
        mount.click(force=True)
        page.wait_for_timeout(300)
        
        # Check that position detail view is shown
        assert page.is_visible('#position-detail')
        detail_title = page.locator('#position-name')
        assert detail_title.is_visible()


@pytest.mark.interaction
def test_click_technique_shows_detail(page):
    """Test that clicking a technique shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Look for any technique in the diagram (they are in SVG g elements with class technique-node)
    techniques = page.locator('.technique-node')
    if techniques.count() > 0:
        # Click the first visible technique
        first_tech = techniques.first
        first_tech.click(force=True)
        page.wait_for_timeout(300)
        
        # Check that technique detail view is shown
        assert page.is_visible('#technique-detail')
        detail_title = page.locator('#technique-name')
        assert detail_title.is_visible()


@pytest.mark.interaction
def test_back_button_returns_to_diagram(page):
    """Test that back button returns from detail view to diagram."""
    wait_for_diagram_ready(page)
    
    # Click on a technique
    techniques = page.locator('.technique-node')
    if techniques.count() > 0:
        first_tech = techniques.first
        first_tech.click(force=True)
        page.wait_for_timeout(300)
        
        # Verify detail view is shown
        assert page.is_visible('#technique-detail')
        
        # Click back button
        back_button = page.locator('#technique-back-btn')
        if back_button.is_visible():
            back_button.click()
            page.wait_for_timeout(300)
            
            # Verify back on diagram view
            assert page.is_visible('#flow-diagram')


@pytest.mark.interaction
def test_zoom_in_button(page):
    """Test that zoom in button works."""
    wait_for_diagram_ready(page)
    
    # Get initial transform (use first top-level group)
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
    
    # Get zoomed transform (first top-level group)
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
    
    # Count visible submissions before toggle (only technique nodes)
    submissions = page.locator('.technique-node[data-category="submission"]')
    initial_visible = sum(1 for sub in submissions.all() if sub.is_visible())
    
    assert initial_visible > 0, "No submissions visible initially"
    
    # Click submission toggle to hide (use header toggle button)
    submission_toggle = page.locator('button.category-toggle[data-category="submission"]')
    # Force the click to avoid overlay/interaction timing issues
    submission_toggle.click(force=True)
    page.wait_for_timeout(800)

    # Wait until no submission nodes are visible (robust against transitions)
    page.wait_for_function("() => Array.from(document.querySelectorAll('.technique-node[data-category=\\\"submission\\\"]')).every(el => { const s = window.getComputedStyle(el); return s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0 || (el.offsetWidth === 0 && el.offsetHeight === 0); })", timeout=2000)
    
    # Check submissions are hidden
    visible_after = sum(1 for sub in submissions.all() if sub.is_visible())
    assert visible_after == 0, f"Expected 0 submissions visible, found {visible_after}"
    
    # Toggle back on
    submission_toggle.click()
    page.wait_for_timeout(600)
    
    # Check submissions are visible again
    visible_restored = sum(1 for sub in submissions.all() if sub.is_visible())
    assert visible_restored > 0, "Submissions should be visible after toggling back"
