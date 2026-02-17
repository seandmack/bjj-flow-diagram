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

    posture = page.locator('g:has-text("Posture")').first
    print('count:', posture.count())
    try:
        print('visible before:', posture.is_visible())
    except Exception as e:
        print('visible check error', e)
    try:
        box = posture.bounding_box()
        print('box:', box)
    except Exception as e:
        print('bounding_box error', e)

    try:
        # Try clicking the text element specifically
        text_el = page.locator('g:has-text("Posture") text').first
        if text_el.count() > 0:
            text_el.click(force=True)
            print('clicked text')
        else:
            posture.click(force=True)
            print('clicked group')
    except Exception as e:
        print('click error', e)

    # Also try dispatching a native click event on the group element
    dispatch_result = page.evaluate("() => { const groups = Array.from(document.querySelectorAll('g')); const g = groups.find(el => el.textContent && el.textContent.includes('Posture')); if (g) { g.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true})); return true; } return false; }")
    print('dispatched click via evaluate:', dispatch_result)
    # Inspect whether the matched group has D3 event listeners
    nodes_info = page.evaluate("() => { return Array.from(document.querySelectorAll('.technique-node')).map(g => ({ text: g.textContent, has_on: !!g.__on, on_types: g.__on ? g.__on.map(o => o.type) : null })); }")
    print('technique-node info (sample):', nodes_info[:5])
    posture_info = page.evaluate("() => { const g = Array.from(document.querySelectorAll('.technique-node')).find(el => el.textContent && el.textContent.includes('Posture')); if (!g) return null; return { text: g.textContent, has_on: !!g.__on, on_types: g.__on ? g.__on.map(o => o.type) : null, children: Array.from(g.querySelectorAll('*')).map(n => n.tagName) }; }")
    print('posture node info:', posture_info)

    time.sleep(0.5)
    print('technique-detail visible:', page.is_visible('#technique-detail'))
    print('technique-detail class:', page.evaluate("() => document.getElementById('technique-detail').className"))
    print('technique-detail style.display:', page.evaluate("() => document.getElementById('technique-detail').style.display"))
    print('technique-name text:', page.locator('#technique-name').text_content())
    print('any .technique-node count:', page.locator('.technique-node').count())
    # Print names of technique nodes that include 'Posture'
    names = page.evaluate("() => Array.from(document.querySelectorAll('.technique-node text')).map(t => t.textContent).filter(n => n && n.includes('Posture'))")
    print('matching names:', names)

    browser.close()
