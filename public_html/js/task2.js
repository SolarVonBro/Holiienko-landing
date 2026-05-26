const rawXml = `<строка>
  <операнд>σ</операнд>
  <оператор>=</оператор>
  <корень>
    <строка>
      <дробь>
        <строка><число>1</число></строка>
        <строка><операнд>N</операнд></строка>
      </дробь>
      <строка>
        <низверх>
          <строка><оператор>∑</оператор></строка>
          <строка><операнд>i</операнд><оператор>=</оператор><число>1</число></строка>
          <строка><операнд>N</операнд></строка>
        </низверх>
        <строка>
          <верх>
            <строка>
              <оператор>(</оператор>
              <низ>
                <строка><операнд>x</операнд></строка>
                <строка><операнд>i</операнд></строка>
              </низ>
              <оператор>−</оператор>
              <операнд>μ</операнд>
              <оператор>)</оператор>
            </строка>
            <строка><число>2</число></строка>
          </верх>
        </строка>
      </строка>
    </строка>
  </корень>
  <оператор>.</оператор>
</строка>`;

const rawXslt = `<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/1998/Math/MathML">

  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/">
    <math display="block">
      <mrow>
        <mi>σ</mi>
        <mo>=</mo>
        <msqrt>
          <mrow>
            <mfrac>
              <mn>1</mn>
              <mi>N</mi>
            </mfrac>
            <mo>&#x2061;</mo>
            <munderover>
              <mo>∑</mo>
              <mrow>
                <mi>i</mi>
                <mo>=</mo>
                <mn>1</mn>
              </mrow>
              <mi>N</mi>
            </munderover>
            <msup>
              <mrow>
                <mo>(</mo>
                <msub>
                  <mi>x</mi>
                  <mi>i</mi>
                </msub>
                <mo>-</mo>
                <mi>μ</mi>
                <mo>)</mo>
              </mrow>
              <mn>2</mn>
            </msup>
          </mrow>
        </msqrt>
      </mrow>
    </math>
  </xsl:template>

</xsl:stylesheet>`;

function highlight(src) {
  return src
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/(&lt;\?[^?]*\?&gt;)/g, '<span class="xml-decl">$1</span>')
    .replace(/(&lt;!--[\s\S]*?--&gt;)/g, '<span class="xml-comment">$1</span>')
    .replace(
      /(&lt;\/?[a-zA-ZЀ-ӿ][a-zA-Z0-9Ѐ-ӿ:_.-]*)((?:\s+[a-zA-Z:_][a-zA-Z0-9:_.-]*="[^"]*")*)\s*(\/?&gt;)/g,
      (m, tag, attrs, close) => {
        const coloredAttrs = attrs.replace(
          /(\s+)([a-zA-Z:_][a-zA-Z0-9:_.-]*)="([^"]*)"/g,
          '$1<span class="xml-attr">$2</span>=<span class="xml-value">"$3"</span>'
        );
        return `<span class="xml-tag">${tag}</span>${coloredAttrs}<span class="xml-tag">${close}</span>`;
      }
    );
}

document.getElementById('xml-display').innerHTML  = highlight(rawXml);
document.getElementById('xslt-display').innerHTML = highlight(rawXslt);

document.getElementById('transform-btn').addEventListener('click', () => {
  const errorDiv  = document.getElementById('error-display');
  const outputBlk = document.getElementById('output-block');
  const srcCard   = document.getElementById('mathml-source-card');
  const mathmlPre = document.getElementById('mathml-display');

  errorDiv.innerHTML = '';
  outputBlk.innerHTML = '';

  try {
    const parser = new DOMParser();

    const xmlDoc = parser.parseFromString(rawXml, 'application/xml');
    const xmlErr = xmlDoc.querySelector('parsererror');
    if (xmlErr) throw new Error('Ошибка парсинга XML: ' + xmlErr.textContent.slice(0, 200));

    const xslDoc = parser.parseFromString(rawXslt, 'application/xml');
    const xslErr = xslDoc.querySelector('parsererror');
    if (xslErr) throw new Error('Ошибка парсинга XSLT: ' + xslErr.textContent.slice(0, 200));

    const xsltProc = new XSLTProcessor();
    xsltProc.importStylesheet(xslDoc);
    const result = xsltProc.transformToFragment(xmlDoc, document);

    if (!result || result.childNodes.length === 0) {
      throw new Error('XSLT вернул пустой результат. Проверьте шаблоны.');
    }

    outputBlk.appendChild(result);

    const serializer = new XMLSerializer();
    let mathmlSource = '';
    outputBlk.querySelectorAll('math').forEach(m => {
      mathmlSource += serializer.serializeToString(m) + '\n\n';
    });

    mathmlPre.innerHTML = highlight(mathmlSource.trim());
    srcCard.classList.remove('d-none');

  } catch (err) {
    errorDiv.innerHTML = `<div class="alert alert-danger py-2 mb-0">${err.message}</div>`;
    outputBlk.innerHTML = '<p class="text-muted text-center mb-0 py-3">Преобразование не удалось. См. ошибку выше.</p>';
    srcCard.classList.add('d-none');
  }
});
