"""
Smoke tests - quick tests to verify basic functionality
Run with: pytest -m smoke
"""
import pytest
from conftest import wait_for_diagram_ready


@pytest.mark.smoke
def test_page_loads(page):
    """Test that the page loads successfully."""
    # Page has a title
    assert page.title() == "BJJ Technique Flow Diagram"
    assert page.is_visible('#flow-diagram')


@pytest.mark.smoke
def test_header_elements_present(page):
    """Test that all header elements are present."""
    wait_for_diagram_ready(page)
    
    # Check that some header exists
    assert page.locator('h1, h2').count() > 0, "No header found"
    
    # Check filter buttons
    assert page.is_visible('button:has-text("Basic")')
    assert page.is_visible('button:has-text("Intermediate")')
    assert page.is_visible('button:has-text("Advanced")')


@pytest.mark.smoke
def test_positions_render(page):
    """Test that position nodes are rendered."""
    wait_for_diagram_ready(page)
    
    # Check that position nodes exist
    positions = page.locator('.position-node')
    count = positions.count()
    
    assert count > 0, "No position nodes found"
    assert count >= 7, f"Expected at least 7 positions, found {count}"


@pytest.mark.smoke
def test_techniques_render(page):
    """Test that technique nodes are rendered."""
    wait_for_diagram_ready(page)
    
    # Check that technique nodes exist
    techniques = page.locator('.technique-node')
    count = techniques.count()
    
    assert count > 0, "No technique nodes found"
    assert count >= 30, f"Expected at least 30 techniques, found {count}"


@pytest.mark.smoke
def test_zoom_controls_present(page):
    """Test that zoom controls are present and functional."""
    wait_for_diagram_ready(page)
    
    # Check zoom buttons exist
    assert page.is_visible('button:has-text("➕")')  # Zoom in
    assert page.is_visible('button:has-text("➖")')  # Zoom out
    assert page.is_visible('button:has-text("⟲")')  # Reset


@pytest.mark.smoke
def test_category_toggles_present(page):
    """Test that category toggle buttons are present."""
    wait_for_diagram_ready(page)
    
    categories = ['Escape', 'Submission', 'Sweep', 'Pass', 'Takedown', 'Counter']
    
    for category in categories:
        assert page.is_visible(f'.legend-item:has-text("{category}")'), \
            f"Category toggle '{category}' not found"
