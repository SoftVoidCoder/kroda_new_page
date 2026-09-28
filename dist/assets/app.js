const menuButton = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  mobileMenu.hidden = isOpen;
  menuButton.setAttribute('aria-label', isOpen ? 'Открыть меню' : 'Закрыть меню');
});

mobileMenu?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    mobileMenu.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
  });
});

const scope = document.querySelector('#scope');
const scopeValue = document.querySelector('#scope-value');
const taskType = document.querySelector('#task-type');
const objectType = document.querySelector('#object-type');
const calculator = document.querySelector('#calculator');
const estimate = document.querySelector('#estimate');

function updateScope() {
  const unit = taskType.value === 'floor' || taskType.value === 'roof' ? 'м²' : 'м';
  scopeValue.value = `${scope.value} ${unit}`;
  scopeValue.textContent = `${scope.value} ${unit}`;
}

scope?.addEventListener('input', updateScope);
taskType?.addEventListener('change', updateScope);

calculator?.addEventListener('submit', (event) => {
  event.preventDefault();
  const rates = { pipe: 1800, roof: 2450, floor: 2100, tank: 2800 };
  const factors = { industrial: 1.18, commercial: 1.08, private: 1 };
  const total = Math.round((Number(scope.value) * rates[taskType.value] * factors[objectType.value]) / 10000) * 10000;
  estimate.innerHTML = `Предварительный бюджет: <strong>от ${new Intl.NumberFormat('ru-RU').format(total)} ₽</strong>. Точная стоимость зависит от проекта и комплектации.`;
});

const search = document.querySelector('#site-search');
const searchableLinks = [...document.querySelectorAll('.header-nav a[href^="#"]')];
search?.addEventListener('input', () => {
  const query = search.value.trim().toLowerCase();
  if (query.length < 2) return;
  const match = searchableLinks.find((link) => link.textContent.toLowerCase().includes(query));
  if (match) search.setAttribute('aria-label', `Найдено: ${match.textContent}`);
});
