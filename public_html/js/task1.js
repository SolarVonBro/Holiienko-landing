const CBR_URL   = 'https://www.cbr-xml-daily.ru/daily_json.js';
const FORM_URL  = 'https://docs.google.com/forms/d/e/1FAIpQLSc_sJpZ-t2y-Mt_HsDADgh4-et7OGLGFqZNXseLRQlGwciWoQ/formResponse';

const $surname    = document.getElementById('surname');
const $amount     = document.getElementById('amount');
const $convertBtn = document.getElementById('convert-btn');
const $resultBox  = document.getElementById('result-box');
const $resultVal  = document.getElementById('result-value');
const $resultDet  = document.getElementById('result-detail');

async function doConvert() {
  const surname = $surname.value.trim();
  const amount  = parseFloat($amount.value);

  if (!surname) { $surname.focus(); return; }
  if (!amount || amount <= 0) { $amount.focus(); return; }

  $convertBtn.disabled = true;
  $convertBtn.textContent = 'Загрузка курса...';

  try {
    const res  = await fetch(CBR_URL);
    const data = await res.json();
    const rate = data.Valute.CNY.Value;
    const cny  = amount / rate;

    await fetch(FORM_URL, {
      method: 'POST',
      mode:   'no-cors',
      body:   new URLSearchParams({
        'entry.138719531': surname,
        'entry.1949578643': cny.toFixed(2),
      }),
    });

    $resultVal.textContent = `${surname}: ${cny.toFixed(2)} ¥`;
    $resultDet.textContent = `${amount.toLocaleString('ru-RU')} ₽ / ${rate.toFixed(4)} = ${cny.toFixed(2)} CNY · Данные отправлены в форму`;
    $resultBox.classList.remove('d-none');
  } catch (err) {
    $resultVal.textContent = 'Не удалось получить курс или отправить данные';
    $resultDet.textContent = '';
    $resultBox.classList.remove('d-none');
  } finally {
    $convertBtn.disabled = false;
    $convertBtn.textContent = 'Конвертировать';
  }
}

$convertBtn.addEventListener('click', doConvert);
[$surname, $amount].forEach(el => {
  el.addEventListener('keydown', e => { if (e.key === 'Enter') doConvert(); });
});
