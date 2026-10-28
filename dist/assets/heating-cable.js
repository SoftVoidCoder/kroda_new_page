const tabs = [...document.querySelectorAll('.cable-tabs button')];
const filters = [...document.querySelectorAll('.cable-filters input')];
const cards = [...document.querySelectorAll('.cable-card')];
const count = document.querySelector('#cable-count');
const empty = document.querySelector('.cable-empty');

function updateCatalog() {
  const category = tabs.find(tab => tab.classList.contains('active'))?.dataset.category || 'all';
  const selected = filters.filter(input => input.checked);
  let visible = 0;
  cards.forEach(card => {
    const tags = card.dataset.filters.split(' ');
    const matches = (category === 'all' || card.dataset.category === category) &&
      ['app', 'env', 'maker'].every(group => {
        const choices = selected.filter(input => input.dataset.group === group);
        return !choices.length || choices.some(input => tags.includes(input.value));
      });
    card.hidden = !matches;
    if (matches) visible++;
  });
  count.textContent = `Найдено: ${visible}`;
  empty.hidden = visible > 0;
}

tabs.forEach(tab => tab.addEventListener('click', () => {
  tabs.forEach(other => {
    other.classList.toggle('active', other === tab);
    other.setAttribute('aria-selected', String(other === tab));
  });
  updateCatalog();
}));
filters.forEach(input => input.addEventListener('change', updateCatalog));
document.querySelector('#clear-filters')?.addEventListener('click', () => {
  filters.forEach(input => input.checked = false);
  updateCatalog();
});
document.querySelector('#filter-toggle')?.addEventListener('click', event => {
  const open = document.querySelector('.cable-filters').classList.toggle('is-open');
  event.currentTarget.setAttribute('aria-expanded', String(open));
  event.currentTarget.textContent = open ? 'Скрыть фильтры' : 'Показать фильтры';
});
updateCatalog();
