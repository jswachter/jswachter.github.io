// Keep one semantic endnote list. Only its visual position changes on wide screens.
// Markdown parsing and math rendering remain the viewer's responsibility.
export function setupFootnotes(content) {
    const section = content.querySelector('[data-footnotes]');
    if (!section) {
        return;
    }

    const references = Array.from(content.querySelectorAll('[data-footnote-ref]'));
    const notes = Array.from(section.querySelectorAll(':scope > ol > li')).map((note) => {
        const reference = references.find((link) => link.getAttribute('href') === `#${note.id}`);
        note.tabIndex = -1;
        return { note, reference };
    });
    const wideScreen = window.matchMedia('screen and (min-width: 1280px)');
    let frame = 0;

    function layout() {
        frame = 0;
        content.classList.toggle('has-sidenotes', wideScreen.matches);
        if (!wideScreen.matches) {
            section.style.removeProperty('--footnotes-space');
            return;
        }

        const contentTop = content.getBoundingClientRect().top;
        let bottom = 0;
        for (const { note, reference } of notes) {
            if (!reference) {
                continue;
            }
            const top = Math.max(reference.getBoundingClientRect().top - contentTop, bottom);
            note.style.setProperty('--footnote-top', `${top}px`);
            // Nearby notes stack with breathing room instead of overlapping.
            bottom = top + note.getBoundingClientRect().height + 16;
        }
        const sectionTop = section.getBoundingClientRect().top - contentTop;
        section.style.setProperty('--footnotes-space', `${Math.max(0, bottom - sectionTop)}px`);
    }

    function scheduleLayout() {
        if (!frame) {
            frame = requestAnimationFrame(layout);
        }
    }

    // Math, images and fonts can reflow the article after its Markdown is rendered.
    const observer = new ResizeObserver(scheduleLayout);
    observer.observe(content);
    notes.forEach(({ note }) => observer.observe(note));
    content.addEventListener('load', scheduleLayout, true);
    wideScreen.addEventListener('change', scheduleLayout);
    document.fonts.ready.then(scheduleLayout);
    layout();

    // Hash links can be opened before the asynchronous notebook has been rendered.
    if (window.location.hash) {
        const target = document.getElementById(window.location.hash.slice(1));
        if (target && content.contains(target)) {
            requestAnimationFrame(() => target.scrollIntoView());
        }
    }
}
