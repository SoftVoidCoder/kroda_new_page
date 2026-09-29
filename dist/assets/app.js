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

const leadDialog = document.querySelector('#lead-dialog');
const leadForm = document.querySelector('#lead-form');
const requestType = document.querySelector('#request-type');
const formStatus = document.querySelector('.form-status');

document.querySelectorAll('[data-lead-open]').forEach((button) => {
  button.addEventListener('click', () => {
    requestType.value = button.dataset.leadOpen || 'Заявка с сайта';
    formStatus.textContent = '';
    formStatus.classList.remove('is-error');
    leadDialog.showModal();
  });
});

document.querySelector('[data-lead-close]')?.addEventListener('click', () => leadDialog.close());
leadDialog?.addEventListener('click', (event) => {
  if (event.target === leadDialog) leadDialog.close();
});

leadForm?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const submitButton = leadForm.querySelector('button[type="submit"]');
  const payload = Object.fromEntries(new FormData(leadForm));
  submitButton.disabled = true;
  submitButton.textContent = 'Отправляем…';
  formStatus.textContent = '';
  formStatus.classList.remove('is-error');

  try {
    const response = await fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error('Request failed');
    leadForm.reset();
    formStatus.textContent = 'Заявка принята. Мы свяжемся с вами в рабочее время.';
    setTimeout(() => leadDialog.close(), 1800);
  } catch (error) {
    formStatus.textContent = 'Не удалось отправить. Позвоните 8 (800) 500-05-19.';
    formStatus.classList.add('is-error');
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Отправить заявку';
  }
});

const applicationSlider = document.querySelector('[data-slider]');
document.querySelectorAll('[data-slide]').forEach((button) => {
  button.addEventListener('click', () => {
    const direction = button.dataset.slide === 'next' ? 1 : -1;
    applicationSlider?.scrollBy({ left: applicationSlider.clientWidth * direction, behavior: 'smooth' });
  });
});

const heroImage = document.querySelector('.hero-image');
const heroCurrent = document.querySelector('#hero-current');
const heroSlides = [
  { src: 'assets/hero-industrial.webp', alt: 'Промышленная система электрообогрева трубопровода' },
  { src: 'assets/roof-heating.webp', alt: 'Система электрообогрева кровли и водостоков' },
  { src: 'assets/engineering-service.webp', alt: 'Монтаж и обслуживание системы электрообогрева' }
];
let heroIndex = 0;

document.querySelectorAll('[data-hero]').forEach((button) => {
  button.addEventListener('click', () => {
    const direction = button.dataset.hero === 'next' ? 1 : -1;
    heroIndex = (heroIndex + direction + heroSlides.length) % heroSlides.length;
    heroImage.src = heroSlides[heroIndex].src;
    heroImage.alt = heroSlides[heroIndex].alt;
    heroCurrent.value = `${String(heroIndex + 1).padStart(2, '0')} / ${String(heroSlides.length).padStart(2, '0')}`;
    heroCurrent.textContent = heroCurrent.value;
  });
});
