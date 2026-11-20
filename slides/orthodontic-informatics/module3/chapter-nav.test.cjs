// Run with node --test slides/orthodontic-informatics/module3/chapter-nav.test.cjs.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const moduleDir = __dirname;
const manifest = fs.readFileSync(path.join(moduleDir, 'index.html'), 'utf8');
const chapterIds = [...manifest.matchAll(/data-chapter="([^"]+)"/g)].map(match => match[1]);
const outline = fs.readFileSync(path.join(moduleDir, 'slides/outline.html'), 'utf8');
const labels = [...outline.split('<aside')[0].matchAll(/<li>(.*?)<\/li>/g)].map(match => match[1]);

// A small DOM/Reveal host: production logic runs unmodified in a fresh JS context.
function host({ loaded = true, reveal = true } = {}) {
    const footer = { textContent: '', hidden: true };
    let slides = chapterIds.map(chapter => ({
        dataset: { chapter },
        querySelectorAll: () => [],
    }));
    const slideContainer = { get children() { return slides; } };
    const events = {};
    const documentEvents = {};
    let mutation;
    let index = 0;
    const deck = {
        on: (name, callback) => { events[name] = callback; },
        getIndices: () => ({ h: index }),
        isReady: () => true,
    };
    const document = {
        querySelector: selector => ({
            '.reveal .slides': slideContainer,
            '#chapter-footer': footer,
        })[selector],
        addEventListener: (name, callback) => { documentEvents[name] = callback; },
        removeEventListener: name => { delete documentEvents[name]; },
    };
    const window = reveal ? { Reveal: deck } : {};
    function loadSlides() {
        // The external-replace plugin discards every placeholder attribute.
        slides = chapterIds.map((_, i) => ({
            dataset: {},
            querySelectorAll: () => i === 1 ? labels.map(textContent => ({ textContent })) : [],
        }));
    }
    if (loaded) loadSlides();
    const script = path.join(moduleDir, 'chapter-nav.js');
    assert.ok(fs.existsSync(script), 'Module chapter navigation script must exist');
    // Start with manifest placeholders so the script can snapshot their chapter IDs.
    const loadedSlides = slides;
    slides = chapterIds.map(chapter => ({ dataset: { chapter }, querySelectorAll: () => [] }));
    vm.runInNewContext(fs.readFileSync(script, 'utf8'), {
        window, document,
        MutationObserver: class {
            constructor(callback) { mutation = callback; }
            observe() {}
        },
    });
    slides = loadedSlides;
    return {
        footer, events, documentEvents, deck, window,
        mutate: () => mutation(),
        loadSlides,
        move: value => { index = value; events.slidechanged(); },
    };
}

test('initial ready event shows Introduction outside externally replaced slides', () => {
    const browser = host();
    browser.events.ready();
    assert.equal(browser.footer.textContent, 'Introduction');
    assert.equal(browser.footer.hidden, false);
});

test('late Reveal script loading registers events and handles an already-ready deep link', () => {
    const browser = host({ reveal: false });
    browser.window.Reveal = browser.deck;
    browser.documentEvents.load();
    browser.move(16);
    assert.equal(browser.footer.textContent, '5. Current clinical informatics standards');
});

test('async external replacement fills an initially hidden deep-link chapter without another navigation', () => {
    const browser = host({ loaded: false });
    browser.move(14);
    assert.equal(browser.footer.hidden, true);
    assert.equal(browser.footer.textContent, '');
    browser.loadSlides();
    browser.mutate();
    assert.equal(browser.footer.textContent, '4. Vendor-specific vs shared-standards communications');
    assert.equal(browser.footer.hidden, false);
});

test('forward and backward navigation uses the original 27-slide manifest after replacement', () => {
    const browser = host();
    browser.events.ready();
    for (const i of [...chapterIds.keys(), ...[...chapterIds.keys()].reverse()]) {
        browser.move(i);
        const id = chapterIds[i];
        assert.equal(browser.footer.textContent,
            id === 'introduction' ? 'Introduction' : id === 'review' ? 'Review' : `${id}. ${labels[Number(id) - 1]}`);
    }
});
