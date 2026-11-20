// Custom Reveal.js current-chapter audience footer, not a native Reveal feature.
// Maps manifest data-chapter values to the deck outline's ordered labels; updates
// on ready, slidechanged and async external replacement, including direct links.
// Displays a label only: no navigation, menu or timer. Requires .reveal .slides,
// #chapter-footer outside .slides and an ordered outline in slide 2 (index 1).
// Load before common.js; see README.md#reusable-chapter-footer-opt-in.
(() => {
    const container = document.querySelector('.reveal .slides');
    const footer = document.querySelector('#chapter-footer');
    // External replacement removes placeholder attributes; retain only their order.
    const chapters = Array.from(container.children, slide => slide.dataset.chapter);
    const update = () => {
        const slides = Array.from(container.children);
        const labels = Array.from(slides[1].querySelectorAll('ol > li'),
            item => item.textContent.trim());
        const chapter = chapters[window.Reveal.getIndices().h];
        const label = labels[Number(chapter) - 1];
        footer.textContent = chapter === 'introduction' ? 'Introduction'
            : chapter === 'review' ? 'Review'
                : label ? `${chapter}. ${label}` : '';
        footer.hidden = !footer.textContent;
    };
    // Handles async external loading even if the current slide does not change.
    new MutationObserver(() => {
        if (window.Reveal && window.Reveal.isReady()) update();
    }).observe(container, { childList: true, subtree: true });
    const attach = () => {
        const deck = window.Reveal;
        if (!deck || typeof deck.on !== 'function') return;
        document.removeEventListener('load', attach, true);
        deck.on('ready', update);
        deck.on('slidechanged', update);
        if (deck.isReady()) update();
    };
    // common.js loads Reveal dynamically. Capturing script loads avoids polling.
    document.addEventListener('load', attach, true);
    attach();
})();
