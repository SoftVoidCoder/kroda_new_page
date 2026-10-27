const legacyHouseholdPages = new Set([
  'pipe-freeze-protection.html',
  'pipeline-temperature-maintenance.html',
  'underfloor-heating.html',
  'household-reservoir-heating.html',
  'household-soil-heating.html'
]);

if (legacyHouseholdPages.has(location.pathname.split('/').pop())) {
  document.body.classList.add('inner-page', 'household-detail', 'legacy-household');
  document.querySelector('main')?.classList.add('inner-main');

  const unifiedStyles = document.querySelector('link[href*="household-unified.css"]');
  if (unifiedStyles) document.head.append(unifiedStyles);

  const oldHeader = document.querySelector('body > header');
  if (oldHeader && !oldHeader.classList.contains('site-header')) {
    oldHeader.outerHTML = `
      <header class="site-header">
        <div class="header-primary shell">
          <a class="brand" href="index.html"><img src="assets/korda-mark.png" alt="КОРДА"></a>
          <form class="site-search" role="search" onsubmit="return false">
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg>
            <input id="site-search" type="search" placeholder="Поиск">
          </form>
          <div class="header-contact"><a href="mailto:zayavka@korda.spb.ru">zayavka@korda.spb.ru</a><span>9:00–18:00, пн–пт</span></div>
          <div class="header-phones"><a href="tel:+78005000519">8 (800) 500-05-19</a><a href="tel:+78123333249">8 (812) 333-32-49</a></div>
          <button class="menu-toggle" aria-expanded="false" aria-controls="mobile-menu" aria-label="Открыть меню"><span></span><span></span><span></span></button>
        </div>
        <div class="header-nav-wrap">
          <nav class="header-nav shell">
            <div class="nav-groups">
              <div class="nav-row nav-row-small"><a href="index.html#about">О компании</a><a href="index.html#brands">Бренды</a><a href="index.html#certificates">Сертификаты</a><a href="index.html#faq">FAQ</a><a href="index.html#contacts">Контакты</a></div>
              <div class="nav-row">
                <div class="nav-dropdown"><a class="nav-trigger" href="industrial-solutions.html">Промышленный электрообогрев <span>⌄</span></a><div class="nav-dropdown-menu"><a href="industrial-small.html">Обогрев малых промышленных объектов</a><a href="equipment-heating.html">Электрообогрев оборудования</a><a href="plastic-tanks.html">Обогрев пластиковых ёмкостей</a><a href="large-tanks-heating.html">Обогрев больших ёмкостей</a><a href="pipeline-heating.html">Электрообогрев трубопроводов</a><a href="roof-heating.html">Обогрев кровли</a><a href="surface-heating.html">Обогрев открытых площадок</a><a href="entrance-heating.html">Обогрев входных групп</a><a href="wellhead-heating.html">Обогрев кустовой арматуры</a></div></div>
                <div class="nav-dropdown"><a class="nav-trigger active-nav" href="household-solutions.html">Бытовые решения <span>⌄</span></a><div class="nav-dropdown-menu"><a href="pipe-freeze-protection.html">Защита труб от замерзания</a><a href="pipeline-temperature-maintenance.html">Стабильная температура трубопроводов</a><a href="underfloor-heating.html">Тёплый пол</a><a href="household-roof-gutter-heating.html">Обогрев кровли и водостоков</a><a href="household-entrance-heating.html">Обогрев ступеней, лестниц и входов</a><a href="household-open-area-heating.html">Обогрев открытых площадок</a><a href="household-reservoir-heating.html">Обогрев резервуаров</a><a href="household-soil-heating.html">Обогрев грунта</a></div></div>
                <a href="index.html#product">Подобрать кабель</a><a href="index.html#solutions">Термостаты</a><a href="index.html#solutions">Комплектующие и аксессуары</a>
              </div>
            </div>
            <div class="header-actions"><a class="button button-primary" href="#request">Запросить расчёт</a></div>
          </nav>
          <nav class="mobile-menu" id="mobile-menu" hidden>
            <a href="index.html">Главная</a><a href="index.html#about">О компании</a><a href="index.html#brands">Бренды</a><a href="index.html#certificates">Сертификаты</a><a href="index.html#faq">FAQ</a><a href="index.html#contacts">Контакты</a>
            <strong>Промышленный электрообогрев</strong><a class="mobile-sub" href="industrial-solutions.html">Все решения</a><a class="mobile-sub" href="industrial-small.html">Малые промышленные объекты</a><a class="mobile-sub" href="equipment-heating.html">Оборудование</a><a class="mobile-sub" href="pipeline-heating.html">Трубопроводы</a>
            <strong>Бытовые решения</strong><a class="mobile-sub" href="household-solutions.html">Все решения</a><a class="mobile-sub" href="pipe-freeze-protection.html">Защита труб</a><a class="mobile-sub" href="pipeline-temperature-maintenance.html">Температура трубопроводов</a><a class="mobile-sub" href="underfloor-heating.html">Тёплый пол</a><a class="mobile-sub" href="household-roof-gutter-heating.html">Кровля и водостоки</a><a class="mobile-sub" href="household-entrance-heating.html">Ступени и входы</a><a class="mobile-sub" href="household-open-area-heating.html">Открытые площадки</a><a class="mobile-sub" href="household-reservoir-heating.html">Резервуары</a><a class="mobile-sub" href="household-soil-heating.html">Грунт</a>
          </nav>
        </div>
      </header>`;
  }

  const oldFooter = document.querySelector('body > footer');
  if (oldFooter && !oldFooter.classList.contains('site-footer')) {
    oldFooter.outerHTML = `
      <footer class="site-footer" id="contacts">
        <div class="footer-main shell">
          <div class="footer-brand"><img src="assets/korda-mark.png" alt="КОРДА"><p>Системы электрообогрева и техническая изоляция.</p></div>
          <div class="footer-column"><h2>Контакты</h2><a href="tel:+78123333249">8 (812) 333-32-49</a><a href="tel:+78005000519">8 (800) 500-05-19</a><a href="mailto:zayavka@korda.spb.ru">zayavka@korda.spb.ru</a></div>
          <div class="footer-column"><h2>Адрес</h2><p>Санкт-Петербург,<br>ул. Розенштейна, д. 21, оф. 508</p></div>
          <div class="footer-column"><h2>Бытовые решения</h2><a href="household-solutions.html">Все решения</a><a href="pipe-freeze-protection.html">Защита труб</a><a href="underfloor-heating.html">Тёплый пол</a><a href="household-reservoir-heating.html">Резервуары</a><a href="household-soil-heating.html">Грунт</a></div>
        </div>
        <div class="footer-bottom shell"><span>ООО «ТД КОРДА» · ОГРН 1147847084835</span><span>© 2026 КОРДА</span></div>
      </footer>`;
  }
}

const menuButton = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');

const householdItems = [
  ['household-reservoir-heating.html', 'Обогрев резервуаров'],
  ['household-soil-heating.html', 'Обогрев грунта']
];

document.querySelectorAll('a').forEach((link) => {
  if (link.textContent.trim().startsWith('Промышленный электрообогрев')) {
    link.href = 'industrial-solutions.html';
  }
});

document.querySelectorAll('.nav-dropdown-menu').forEach((menu) => {
  if (!menu.querySelector('a[href="pipe-freeze-protection.html"]')) return;
  householdItems.forEach(([href, label]) => {
    if (menu.querySelector(`a[href="${href}"]`)) return;
    const link = document.createElement('a');
    link.href = href;
    link.textContent = label;
    menu.append(link);
  });
});

document.querySelectorAll('.mobile-menu').forEach((menu) => {
  const householdStart = [...menu.querySelectorAll('strong, a')].find((item) => item.textContent.trim() === 'Бытовые решения');
  if (!householdStart) return;
  const insertBefore = [...menu.querySelectorAll('a')].find((link) => link.textContent.trim() === 'Подобрать кабель');
  householdItems.forEach(([href, label]) => {
    if (menu.querySelector(`a[href="${href}"]`)) return;
    const link = document.createElement('a');
    link.className = 'mobile-sub';
    link.href = href;
    link.textContent = label;
    menu.insertBefore(link, insertBefore || null);
  });
});

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
const heroSlides = [
  { src: 'assets/hero-industrial.webp', alt: 'Промышленная система электрообогрева трубопровода' },
  { src: 'assets/roof-heating.webp', alt: 'Система электрообогрева кровли и водостоков' },
  { src: 'assets/engineering-service.webp', alt: 'Монтаж и обслуживание системы электрообогрева' }
];
let heroIndex = 0;

if (heroImage) {
  heroSlides.slice(1).forEach(({ src }) => {
    const image = new Image();
    image.src = src;
  });

  setInterval(() => {
    heroIndex = (heroIndex + 1) % heroSlides.length;
    heroImage.classList.add('is-changing');
    setTimeout(() => {
    heroImage.src = heroSlides[heroIndex].src;
    heroImage.alt = heroSlides[heroIndex].alt;
      heroImage.classList.remove('is-changing');
    }, 180);
  }, 8000);
}
