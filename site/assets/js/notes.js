/**
 * Notes functionality: wiki-link parsing, backlinks loading, related notes
 */

(function () {
  'use strict';

  /**
   * Convert [[slug]] patterns to clickable links
   * Runs on .prose elements within notes
   */
  function parseWikiLinks() {
    const proseElements = document.querySelectorAll('.note-main .prose');
    if (!proseElements.length) return;

    // Match [[slug]] or [[slug|display text]]
    const wikiLinkPattern = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;

    proseElements.forEach(function (prose) {
      const walker = document.createTreeWalker(
        prose,
        NodeFilter.SHOW_TEXT,
        null,
        false
      );

      const textNodes = [];
      let node;
      while ((node = walker.nextNode())) {
        if (wikiLinkPattern.test(node.textContent)) {
          textNodes.push(node);
        }
        wikiLinkPattern.lastIndex = 0;
      }

      textNodes.forEach(function (textNode) {
        const content = textNode.textContent;
        const fragment = document.createDocumentFragment();
        let lastIndex = 0;
        let match;

        wikiLinkPattern.lastIndex = 0;
        while ((match = wikiLinkPattern.exec(content)) !== null) {
          // Add text before the match
          if (match.index > lastIndex) {
            fragment.appendChild(
              document.createTextNode(content.slice(lastIndex, match.index))
            );
          }

          // Create the link
          const slug = match[1].trim();
          const displayText = match[2] ? match[2].trim() : slug;
          const link = document.createElement('a');
          link.href = '/notes/' + slug + '/';
          link.className = 'wikilink';
          link.dataset.noteSlug = slug;
          link.textContent = displayText;
          fragment.appendChild(link);

          lastIndex = match.index + match[0].length;
        }

        // Add remaining text
        if (lastIndex < content.length) {
          fragment.appendChild(
            document.createTextNode(content.slice(lastIndex))
          );
        }

        textNode.parentNode.replaceChild(fragment, textNode);
      });
    });
  }

  /**
   * Load and display backlinks for the current note
   */
  function loadBacklinks() {
    const container = document.getElementById('backlinks-list');
    if (!container) return;

    const noteSlug = container.dataset.noteSlug;
    if (!noteSlug) return;

    fetch('/notes/index.json')
      .then(function (response) {
        if (!response.ok) throw new Error('Backlinks not available');
        return response.json();
      })
      .then(function (data) {
        const backlinks = data[noteSlug] || [];

        if (backlinks.length === 0) {
          container.innerHTML =
            '<p class="empty-notice">No other notes link here yet.</p>';
          return;
        }

        const list = document.createElement('ul');
        list.className = 'backlinks-items';

        backlinks.forEach(function (link) {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.href = link.url;
          a.textContent = link.title;
          li.appendChild(a);

          if (link.excerpt) {
            const excerpt = document.createElement('span');
            excerpt.className = 'backlink-excerpt';
            excerpt.textContent = ' — ' + link.excerpt;
            li.appendChild(excerpt);
          }

          list.appendChild(li);
        });

        container.innerHTML = '';
        container.appendChild(list);
      })
      .catch(function () {
        container.innerHTML =
          '<p class="empty-notice">Backlinks unavailable.</p>';
      });
  }

  /**
   * Load and display related notes based on shared tags
   */
  function loadRelatedNotes() {
    const container = document.getElementById('related-notes-list');
    if (!container) return;

    const noteSlug = container.dataset.noteSlug;
    const noteTags = container.dataset.noteTags;
    if (!noteSlug || !noteTags) return;

    const tags = noteTags.split(',').filter(Boolean);
    if (tags.length === 0) {
      container.innerHTML =
        '<p class="empty-notice">Add tags to discover related notes.</p>';
      return;
    }

    fetch('/index.json')
      .then(function (response) {
        if (!response.ok) throw new Error('Search index not available');
        return response.json();
      })
      .then(function (data) {
        // Filter to notes only, exclude current note
        const notes = data.filter(function (item) {
          return item.section === 'notes' && !item.permalink.includes(noteSlug);
        });

        // Score notes by shared tags
        const scored = notes.map(function (note) {
          const noteTags = note.tags || [];
          const sharedTags = tags.filter(function (t) {
            return noteTags.includes(t);
          });
          return { note: note, score: sharedTags.length };
        });

        // Sort by score descending, take top 5
        const related = scored
          .filter(function (item) {
            return item.score > 0;
          })
          .sort(function (a, b) {
            return b.score - a.score;
          })
          .slice(0, 5);

        if (related.length === 0) {
          container.innerHTML =
            '<p class="empty-notice">No related notes found.</p>';
          return;
        }

        const list = document.createElement('ul');
        list.className = 'related-items';

        related.forEach(function (item) {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.href = item.note.permalink;
          a.textContent = item.note.title;
          li.appendChild(a);
          list.appendChild(li);
        });

        container.innerHTML = '';
        container.appendChild(list);
      })
      .catch(function () {
        container.innerHTML =
          '<p class="empty-notice">Related notes unavailable.</p>';
      });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    parseWikiLinks();
    loadBacklinks();
    loadRelatedNotes();
  }
})();
