(() => {
  const controls = document.querySelector('.work-filters');
  const collection = document.querySelector('#work-collection');
  if (!controls || !collection) return;

  const buttons = [...controls.querySelectorAll('[data-filter]')];
  const entries = [...collection.querySelectorAll('.work-entry')];
  const groups = [...collection.querySelectorAll('.featured-work, .work-grid')];
  const status = document.querySelector('#filter-status');

  function select(filter) {
    const active = buttons.find(button => button.dataset.filter === filter);
    if (!active) return;

    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button === active));
    });
    entries.forEach(entry => {
      const topics = entry.dataset.topics.split(' ');
      const matches = filter === 'all'
        || (filter === 'selected' ? entry.dataset.selected === 'true' : topics.includes(filter));
      entry.hidden = !matches;
    });
    groups.forEach(group => {
      group.hidden = ![...group.querySelectorAll('.work-entry')].some(entry => !entry.hidden);
    });
    const count = entries.filter(entry => !entry.hidden).length;
    status.textContent = `${active.textContent}: ${count} ${count === 1 ? 'project' : 'projects'} shown.`;
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => select(button.dataset.filter));
  });
  select('selected');
  controls.hidden = false;
})();
