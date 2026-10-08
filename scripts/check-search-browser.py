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
            for path in ('', 'projects/', 'projects/lazyagents/', 'projects/house-price-predictor/', 'projects/gemma-lora/', 'resume/', 'docs/'):
                response = page.goto(base + '/' + lang + path)
                assert response.ok
                assert page.locator('html').get_attribute('lang') == ('en' if lang else 'pt-BR')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, lang, path)
                assert page.locator('h1').count() > 0
                if path in ('', 'projects/lazyagents/'):
                    video = page.locator('.lazy-showcase video')
                    assert video.count() == 1
                    assert video.get_attribute('controls') is not None
                    assert video.get_attribute('autoplay') is None
                    assert video.get_attribute('preload') == 'none'
                    assert page.locator('.lazy-brand img').evaluate('(img) => img.complete && img.naturalWidth > 0')
            page.goto(base + '/' + lang)
            assert page.locator('a[href="/' + lang + 'projects/lazyagents/"]').count() > 0
            page.keyboard.press('Tab')
            assert page.evaluate('document.activeElement.matches("a, button, input, summary")')
            page.locator('a[href$="#cookies"]').click()
            expect(page.locator('[data-consent-box]')).to_be_visible()
            page.locator('[data-consent="denied"]').focus()
            page.keyboard.press('Enter')
            expect(page.locator('[data-consent-box]')).to_be_hidden()
            assert page.evaluate('localStorage.getItem("analytics-consent")') == 'denied'
            assert page.locator('script[src*="googletagmanager"]').count() == 0
            if width < 768:
                toggle = page.locator('label[for="mobile-menu-toggle"]').first
                toggle.focus()
                page.keyboard.press('Enter')
                expect(page.locator('#mobile-menu-dialog')).to_be_visible()
                page.locator('#mobile-menu-dialog a[href="/' + lang + 'projects/"]').click()
                assert page.url.endswith('/' + lang + 'projects/')
            page.close()
    for width in (320, 390, 1024, 1440):
        for lang in ('', 'en/'):
            page = browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base + '/' + lang + 'docs/lazyagents/')
            assert page.locator('.lazy-showcase--docs video').count() == 1
            assert page.locator('.docs-brand-logo').evaluate('(img) => img.complete && img.naturalWidth > 0')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
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
    page.goto(base + '/projects/lazyagents/')
    page.locator('.lazy-demo video').evaluate('(video) => video.play()')
    page.wait_for_function('document.querySelector(".lazy-demo video").currentTime > 0')
    assert 12 < page.locator('.lazy-demo video').evaluate('(video) => video.duration') < 14
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
print('Browser checks passed: home/projects/resume/docs, keyboard/cookies, both languages, four widths, reading links, search, print, delayed index and clearing.')
