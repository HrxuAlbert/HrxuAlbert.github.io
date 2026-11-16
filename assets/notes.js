/* Small, progressive enhancements; article text works without JavaScript. */
document.querySelectorAll('.note-content table').forEach((table) => {
  const scroll = document.createElement('div');
  scroll.className = 'table-scroll';
  scroll.tabIndex = 0;
  scroll.setAttribute('role', 'region');
  scroll.setAttribute('aria-label', 'Scrollable data table');
  table.before(scroll);
  scroll.append(table);
});

document.querySelectorAll('.note-content pre').forEach((block) => {
  block.tabIndex = 0;
  block.setAttribute('aria-label', 'Code block');
});

const noteContent = document.querySelector('.note-content');
if (noteContent && window.renderMathInElement) {
  window.renderMathInElement(noteContent, {
    delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '\\[', right: '\\]', display: true },
      { left: '\\(', right: '\\)', display: false }
    ],
    throwOnError: false,
    trust: false
  });
}
