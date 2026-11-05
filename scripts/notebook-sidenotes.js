function collectFootnotes(content) {
    const section = content.querySelector('[data-footnotes]');
    if (!section) {
        return [];
    }

    section.classList.add('notebook-notes');
    const references = Array.from(content.querySelectorAll('[data-footnote-ref]'));
    return Array.from(section.querySelectorAll(':scope > ol > li')).map((note) => {
        const reference = references.find((link) => link.getAttribute('href') === `#${note.id}`);
        return { note, reference };
    });
}

function collectReferences(content) {
    const notes = [];
    const citations = Array.from(content.querySelectorAll('a[href^="#ref-"]'));
    for (const heading of content.querySelectorAll(':scope > h2')) {
        const list = heading.nextElementSibling;
        if (!/^(references|bibliography)$/i.test(heading.textContent.trim()) || list?.tagName !== 'OL') {
            continue;
        }

        // Recognize the existing Markdown bibliography convention. Leave other
        // lists alone, including bibliographies containing uncited entries.
        const entries = Array.from(list.children).map((note) => {
            const anchor = note.querySelector(':scope > a[id^="ref-"], :scope > p > a[id^="ref-"]');
            const links = anchor ? citations.filter((link) =>
                link.getAttribute('href') === `#${anchor.id}` && !list.contains(link)
            ) : [];
            return { note, anchor, links };
        });
        if (!entries.length || entries.some(({ links }) => !links.length)) {
            continue;
        }

        const section = document.createElement('section');
        section.className = 'notebook-notes references';
        heading.before(section);
        section.append(heading, list);

        entries.forEach(({ note, anchor, links }, index) => {
            // Move the existing fragment ID onto the focusable entry. No second
            // bibliography or cloned math is needed for the desktop margin.
            note.id = anchor.id;
            anchor.removeAttribute('id');
            if (!anchor.textContent && !anchor.hasAttribute('href')) {
                anchor.remove();
            }
            links.forEach((link, occurrence) => {
                link.id ||= `citation-${note.id}-${occurrence + 1}`;
                link.dataset.referenceRef = '';
                link.setAttribute('aria-label', `Reference ${index + 1}`);
                if (/^\d+$/.test(link.textContent.trim())) {
                    link.textContent = `[${link.textContent.trim()}]`;
                }
                const back = document.createElement('a');
                back.href = `#${link.id}`;
                back.dataset.referenceBackref = '';
                back.setAttribute('aria-label', `Back to citation ${occurrence + 1} of reference ${index + 1}`);
                back.textContent = '↩';
                if (occurrence > 0) {
                    const number = document.createElement('sup');
                    number.textContent = occurrence + 1;
                    back.append(number);
                }
                // Loose Markdown lists wrap entry text in a paragraph.
                const last = note.lastElementChild;
                const target = last?.tagName === 'P' ? last : note;
                target.append(' ', back);
            });
            notes.push({ note, reference: links[0] });
        });
    }
    return notes;
}

// One copy of every note stays in its semantic end list. Both kinds share the
// same margin and collision handling, ordered by their first citation in the text.
export function setupSidenotes(content) {
    const notes = [...collectFootnotes(content), ...collectReferences(content)]
        .filter(({ reference }) => reference)
        .sort((a, b) => a.reference.compareDocumentPosition(b.reference) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);
    if (!notes.length) {
        return;
    }
    notes.forEach(({ note }) => {
        note.classList.add('sidenote');
        note.tabIndex = -1;
    });
    const wideScreen = window.matchMedia('screen and (min-width: 1280px)');
    let frame = 0;

    function layout() {
        frame = 0;
        content.classList.toggle('has-sidenotes', wideScreen.matches);
        if (!wideScreen.matches) {
            content.style.removeProperty('--sidenotes-height');
            return;
        }

        const contentTop = content.getBoundingClientRect().top;
        let bottom = 0;
        for (const { note, reference } of notes) {
            const top = Math.max(reference.getBoundingClientRect().top - contentTop, bottom);
            note.style.setProperty('--sidenote-top', `${top}px`);
            // Nearby notes stack with breathing room instead of overlapping.
            bottom = top + note.getBoundingClientRect().height + 16;
        }
        // Leave room above the footer if the margin outlasts the article.
        content.style.setProperty('--sidenotes-height', `${bottom}px`);
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
    return layout;
}
