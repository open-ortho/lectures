// Module-local chapter navigation; keep it outside Reveal's scaled slide canvas.
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
