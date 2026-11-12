const type = new URLSearchParams(location.search).get('type');
const forms = [...document.querySelectorAll('[data-questionnaire-form]')];
const selected = forms.find((form) => form.dataset.questionnaireForm === type);
const requiredCheckboxGroups = ['heating_purpose[]', 'insulation_coverage[]', 'drawings_format[]', 'heated_area_types[]', 'delivery_scope[]'];

document.querySelector('[data-questionnaire-picker]').hidden = Boolean(selected);
document.querySelector('[data-questionnaire-shell]').hidden = !selected;
forms.forEach((form) => { form.hidden = form !== selected; });

if (selected) {
  document.title = `${selected.dataset.title} — КОРДА`;
  selected.querySelector('[name="source_page"]').value = location.href;
  selected.querySelector('[name="submitted_at"]').value = new Date().toISOString();
}

document.querySelectorAll('[data-add-row]').forEach((button) => {
  button.addEventListener('click', () => {
    const list = document.querySelector(button.dataset.target);
    const template = document.querySelector(button.dataset.template);
    const max = Number(button.dataset.max);
    const index = list.children.length;
    if (index >= max) return;
    const fragment = template.content.cloneNode(true);
    fragment.querySelectorAll('[name]').forEach((input) => {
      input.name = input.name.replace('__INDEX__', index);
    });
    fragment.querySelector('[data-row-title]').textContent = `${button.dataset.rowLabel} ${index + 1}`;
    list.append(fragment);
    button.disabled = list.children.length >= max;
  });
});

forms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    const contact = form.querySelector('input[type="tel"]');
    const email = form.querySelector('input[type="email"]');
    const status = form.querySelector('.questionnaire-status');
    const missingGroup = requiredCheckboxGroups
      .map((name) => [...form.querySelectorAll('input[type="checkbox"]')].filter((input) => input.name === name))
      .find((group) => group.length && !group.some((input) => input.checked));
    if (missingGroup) {
      event.preventDefault();
      status.textContent = 'Выберите хотя бы один вариант в каждом обязательном блоке.';
      status.classList.add('is-error');
      missingGroup[0].focus();
      return;
    }
    if (!contact.value.trim() && !email.value.trim()) {
      event.preventDefault();
      status.textContent = 'Укажите телефон или e-mail для связи.';
      status.classList.add('is-error');
      contact.focus();
      return;
    }
    if (location.hostname === 'softvoidcoder.github.io' || location.hostname === '127.0.0.1' || location.hostname === 'localhost') {
      event.preventDefault();
      status.textContent = 'Форма заполнена корректно. Передачу менеджеру подключит команда КОРДА.';
      status.classList.remove('is-error');
    }
  });
});
