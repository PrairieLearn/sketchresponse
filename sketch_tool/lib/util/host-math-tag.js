const XHTML = 'http://www.w3.org/1999/xhtml';
const tags = new WeakMap();
const pending = new Set();
let frame = null;
let typesetting = false;

function measure(element) {
  const tag = tags.get(element);
  if (!tag) return;
  const width = tag.wrapper.offsetWidth;
  const height = tag.wrapper.offsetHeight;
  element.setAttribute('width', String(width));
  element.setAttribute('height', String(height));
  const dx =
    tag.align === 'middle' ? -width / 2 : tag.align === 'end' ? -width : 0;
  // Keep the existing SVG text anchor at the HTML line's baseline. Layout
  // offsets are in SVG units, including when the canvas viewport is scaled.
  element.setAttribute(
    'transform',
    `translate(${dx}, ${-tag.baseline.offsetTop})`,
  );
}

function scheduleTypesetting() {
  if (frame !== null || typesetting) return;
  frame = requestAnimationFrame(async () => {
    frame = null;
    const math = window.MathJax;
    const batch = [];
    typesetting = true;
    try {
      for (const element of pending) {
        const tag = tags.get(element);
        if (!tag || !element.isConnected || tag.rendered === tag.value)
          continue;
        if (tag.rendered !== null) math.typesetClear?.([tag.content]);
        tag.content.textContent = tag.value;
        tag.rendered = tag.value;
        tag.typesetting = true;
        batch.push({ element, tag });
      }
      pending.clear();
      if (batch.length) {
        await math.typesetPromise(batch.map(({ tag }) => tag.content));
      }
    } catch (error) {
      console.error(
        'Unable to typeset SketchResponse tags with MathJax.',
        error,
      );
    } finally {
      for (const { element, tag } of batch) {
        tag.typesetting = false;
        if (tags.get(element) === tag && element.isConnected) {
          measure(element);
        } else {
          math.typesetClear?.([tag.content]);
        }
      }
      typesetting = false;
      if (pending.size) scheduleTypesetting();
    }
  });
}

export function updateHostMathTag(element, value, align) {
  let tag = tags.get(element);
  if (!tag) {
    element.setAttribute('width', '100%');
    element.setAttribute('height', '100%');
    const wrapper = document.createElementNS(XHTML, 'div');
    wrapper.style.cssText =
      'display: inline-block; position: relative; white-space: nowrap; width: max-content;';
    const content = document.createElementNS(XHTML, 'span');
    content.className = 'mathjax_process';
    content.textContent = value;
    const baseline = document.createElementNS(XHTML, 'span');
    baseline.style.cssText = 'display: inline-block; width: 0; height: 0;';
    wrapper.append(content, baseline);
    element.append(wrapper);
    tag = {
      wrapper,
      content,
      baseline,
      value,
      align,
      rendered: null,
      typesetting: false,
    };
    tags.set(element, tag);
  }
  tag.value = value;
  tag.align = align;
  measure(element);
  if (tag.rendered !== value) {
    pending.add(element);
    scheduleTypesetting();
  }
}

export function clearHostMathTag(element) {
  const tag = tags.get(element);
  pending.delete(element);
  tags.delete(element);
  // In-flight typesetting clears a removed tag when its promise settles.
  if (tag && !tag.typesetting) window.MathJax.typesetClear?.([tag.content]);
}
