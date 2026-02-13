"""
Counter tests - tests specific to counter functionality
Run with: pytest test_counters.py
"""
import pytest
from conftest import wait_for_diagram_ready, get_element_position, check_overlap


@pytest.mark.interaction
def test_counter_toggle_button(page):
    """Test that the counter toggle button works."""
    wait_for_diagram_ready(page)
    
    # Find the counter category toggle button (not the legend item)
    counter_toggle = page.locator('button[data-category="counter"]')
    assert counter_toggle.is_visible()
    assert 'active' in counter_toggle.get_attribute('class'), "Counter button should start as active"
    
    # Click to toggle off
    counter_toggle.click()
    page.wait_for_timeout(600)  # Wait for transition
    
    # Verify the button is no longer active
    assert 'active' not in counter_toggle.get_attribute('class'), "Counter button should not be active after clicking"
    
    # Verify no counter technique nodes are rendered
    counter_nodes = page.locator('.technique-node[data-category="counter"]')
    assert counter_nodes.count() == 0, "No counter nodes should be visible when toggle is off"
    
    # Click to toggle on
    counter_toggle.click()
    page.wait_for_timeout(600)
    
    # Verify the button is active again
    assert 'active' in counter_toggle.get_attribute('class'), "Counter button should be active after clicking again"
    
    # Verify counter nodes are rendered again
    counter_nodes = page.locator('.technique-node[data-category="counter"]')
    assert counter_nodes.count() > 0, "Counter nodes should be visible when toggle is on"


@pytest.mark.visual
def test_armbar_counters_exist(page):
    """Test that armbar from mount has 3 counters."""
    wait_for_diagram_ready(page)
    
    # Set difficulty filter to advanced to show all counter techniques
    page.locator('button[data-filter="advanced"]').click()
    page.wait_for_timeout(600)
    
    # Counters should now be visible
    posture_defense = page.get_by_text("Posture")
    hitchhiker = page.locator('g:has-text("Hitchhiker")')
    cartwheel = page.locator('g:has-text("Cartwheel")')
    
    # All three counters should exist
    assert posture_defense.count() > 0, "Posture & Stack Defense counter not found"
    assert hitchhiker.count() > 0, "Hitchhiker Roll-Through counter not found"
    assert cartwheel.count() > 0, "Cartwheel Escape counter not found"


@pytest.mark.visual
def test_counters_positioned_left_of_submissions(page):
    """Test that counters appear to the left of their parent submissions."""
    wait_for_diagram_ready(page)
    
    # Set difficulty filter to advanced to show all counter techniques
    page.locator('button[data-filter="advanced"]').click()
    page.wait_for_timeout(600)
    
    # Find armbar from mount
    armbar = page.get_by_text("Armbar from Mount").first
    if not armbar.is_visible():
        pytest.skip("Armbar from Mount not visible")
    
    armbar_box = armbar.bounding_box()
    
    # Find its counters using partial text matching
    counters = [
        page.locator('g:has-text("Posture")').first,
        page.locator('g:has-text("Hitchhiker")').first,
        page.locator('g:has-text("Cartwheel")').first
    ]
    
    for counter in counters:
        if counter.is_visible():
            counter_box = counter.bounding_box()
            # Counter should be to the left (smaller x) than the submission
            assert counter_box['x'] < armbar_box['x'], \
                f"Counter not positioned left of armbar submission"


@pytest.mark.visual
def test_counters_vertically_centered(page):
    """Test that multiple counters are vertically centered around submission."""
    wait_for_diagram_ready(page)
    
    # Set difficulty filter to advanced to show all counter techniques
    page.locator('button[data-filter="advanced"]').click()
    page.wait_for_timeout(600)
    
    # Find armbar from mount
    armbar = page.get_by_text("Armbar from Mount").first
    if not armbar.is_visible():
        pytest.skip("Armbar from Mount not visible")
    
    armbar_box = armbar.bounding_box()
    armbar_center_y = armbar_box['y'] + armbar_box['height'] / 2
    
    # Find counters - use partial text matching
    counters = [
        page.locator('g:has-text("Posture")').first,
        page.locator('g:has-text("Hitchhiker")').first,
        page.locator('g:has-text("Cartwheel")').first
    ]
    
    visible_counters = [c for c in counters if c.is_visible()]
    
    if len(visible_counters) == 0:
        pytest.skip("No visible counters found")
    
    # Calculate the center Y of all counters
    counter_ys = []
    for counter in visible_counters:
        box = counter.bounding_box()
        center_y = box['y'] + box['height'] / 2
        counter_ys.append(center_y)
    
    # The middle counter should be roughly aligned with armbar
    # or the average of all counters should be near armbar center
    avg_counter_y = sum(counter_ys) / len(counter_ys)
    
    # Allow 100px tolerance for centering
    tolerance = 100
    assert abs(avg_counter_y - armbar_center_y) < tolerance, \
        f"Counters not centered around armbar. Armbar Y: {armbar_center_y}, Counter avg Y: {avg_counter_y}"


@pytest.mark.visual
def test_counters_do_not_overlap(page):
    """Test that counters don't overlap with other techniques."""
    wait_for_diagram_ready(page)
    
    # Get all visible technique nodes
    all_techniques = page.locator('.technique-node').all()
    
    # Get bounding boxes for all visible techniques
    boxes = []
    for tech in all_techniques:
        if tech.is_visible():
            box = tech.bounding_box()
            if box:
                boxes.append(box)
    
    # Check for overlaps
    overlaps = []
    for i, box1 in enumerate(boxes):
        for j, box2 in enumerate(boxes[i+1:], i+1):
            if check_overlap(box1, box2):
                overlaps.append((i, j))
    
    assert len(overlaps) == 0, \
        f"Found {len(overlaps)} overlapping technique pairs"


@pytest.mark.interaction
def test_counter_detail_view(page):
    """Test that clicking a counter shows its detail view."""
    wait_for_diagram_ready(page)
    
    # Set difficulty filter to advanced to show all counter techniques
    page.locator('button[data-filter="advanced"]').click()
    page.wait_for_timeout(600)
    
    # Click on a counter - use partial text match for "Posture"
    posture_defense = page.locator('g:has-text("Posture")').first
    if not posture_defense.is_visible():
        pytest.skip("Posture & Stack Defense counter not visible")
    
    posture_defense.click()
    page.wait_for_timeout(300)
    
    # Check that detail view is shown
    assert page.is_visible('#technique-detail')
    
    # Check that it shows counter info
    assert page.is_visible('#technique-name:has-text("Posture")')
    assert page.is_visible('#technique-category:has-text("counter")')
