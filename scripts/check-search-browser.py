from playwright.sync_api import sync_playwright, expect
import sys

base = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8765').rstrip('/')

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox'])
    errors = []
    for width in (320, 390, 1024, 1440):
        for lang in ('', 'en/'):
            page = browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base + '/' + lang + 'docs/lazyagents/')
            pager = page.locator('.docs-pagination')
            assert pager.locator('[rel=prev]').count() == 0
            pager.locator('[rel=next]').click()
            assert page.locator('.docs-pagination [rel=prev]').get_attribute('href') == '/' + lang + 'docs/lazyagents/'
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.keyboard.press('Control+k')
            page.wait_for_function('indexed')
            page.locator('#search-query').fill('SP Night')
            page.locator('#search-results a[href="https://sp-night.github.io/ports/"]').wait_for()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.locator('#search-query').fill('Skills')
            page.locator('#search-results a[href="/' + lang + 'docs/lazyagents/guide/skills/"]').click()
            assert page.url.endswith('/' + lang + 'docs/lazyagents/guide/skills/')
            page.emulate_media(media='print')
            assert not page.locator('.docs-pagination').is_visible()
            page.close()
    page = browser.new_page(reduced_motion='reduce')
    page.on('pageerror', lambda error: errors.append(str(error)))
    pending = []
    page.route('**/index.json', lambda route: pending.append(route))
    page.goto(base + '/docs/')
    page.keyboard.press('Control+k')
    page.locator('#search-query').fill('Skills')
    assert not page.evaluate('indexed')
    page.wait_for_timeout(100)
    assert pending
    for route in pending:
        route.continue_()
    page.locator('#search-results a[href="/docs/lazyagents/guide/skills/"]').wait_for()
    page.locator('#search-query').fill('')
    expect(page.locator('#search-results li')).to_have_count(0)
    page.locator('#search-query').fill('   ')
    expect(page.locator('#search-results li')).to_have_count(0)
    assert not errors, errors
    browser.close()
print('Browser checks passed: both languages, four widths, reading links, external/internal search, print, delayed index and clearing.')
