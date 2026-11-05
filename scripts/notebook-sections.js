// Section navigation is derived from the article, with native fragment links.
export function setupSections(content, navigation) {
    const headings = Array.from(content.querySelectorAll('h2, h3'))
        .filter((heading) => !heading.closest('.notebook-notes'));
    if (headings.length < 2) {
        return;
    }

    const list = document.createElement('ol');
    const links = headings.map((heading, index) => {
        const label = heading.textContent.trim();
        if (!heading.id) {
            const slug = label.normalize('NFKD').replace(/\p{M}/gu, '')
                .toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '');
            const base = `section-${slug || index + 1}`;
            let id = base;
            let suffix = 2;
            while (document.getElementById(id)) {
                id = `${base}-${suffix++}`;
            }
            heading.id = id;
        }
        heading.tabIndex = -1;

        const item = document.createElement('li');
        if (heading.tagName === 'H3') {
            item.className = 'section-subheading';
        }
        const link = document.createElement('a');
        link.href = `#${encodeURIComponent(heading.id)}`;
        link.textContent = label;
        item.append(link);
        list.append(item);
        return link;
    });
    navigation.replaceChildren(list);
    navigation.hidden = false;

    let frame = 0;
    let active = -1;
    function update() {
        frame = 0;
        // An unheaded introduction belongs to none of the listed sections yet.
        let current = headings[0] === content.firstElementChild ? 0 : -1;
        headings.forEach((heading, index) => {
            if (heading.getBoundingClientRect().top <= 96) {
                current = index;
            }
        });
        // The final heading may never reach the top of a short closing section.
        if (window.scrollY > 0 && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
            current = headings.length - 1;
        }
        if (current !== active) {
            links.forEach((link, index) => {
                if (index === current) {
                    link.setAttribute('aria-current', 'location');
                } else {
                    link.removeAttribute('aria-current');
                }
            });
            active = current;
        }
    }
    function scheduleUpdate() {
        if (!frame) {
            frame = requestAnimationFrame(update);
        }
    }
    window.addEventListener('scroll', scheduleUpdate, { passive: true });
    window.addEventListener('resize', scheduleUpdate);
    new ResizeObserver(scheduleUpdate).observe(content);
    document.fonts.ready.then(scheduleUpdate);
    update();
    return update;
}
