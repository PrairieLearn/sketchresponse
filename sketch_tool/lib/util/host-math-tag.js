import { getHostMath } from './host-math';

const XHTML = 'http://www.w3.org/1999/xhtml';
const tags = new WeakMap();
const wrappers = new WeakMap();
const live = new Set();
const pending = new Set();
const measurements = new Set();
let observer;
let frame = null;
let measureFrame = null;
let typesetting = false;

function measure(element) {
  const tag = tags.get(element);
  if (!tag || !element.isConnected) return;
  const width = tag.wrapper.offsetWidth;
  const height = tag.wrapper.offsetHeight;
  // Hidden tags will be measured by the observer when they become visible.
  if (!width || !height) return;
  element.setAttribute('width', String(width));
  element.setAttribute('height', String(height));
  const dx =
    tag.align === 'middle' ? -width / 2 : tag.align === 'end' ? -width : 0;
  // Layout offsets stay in SVG units when the canvas viewport is scaled.
  element.setAttribute(
    'transform',
    `translate(${dx}, ${-tag.baseline.offsetTop})`,
  );
}

function scheduleMeasurement(element) {
  measurements.add(element);
  if (measureFrame !== null) return;
  measureFrame = requestAnimationFrame(() => {
    measureFrame = null;
    for (const element of measurements) measure(element);
    measurements.clear();
  });
}

function observe(element, wrapper) {
  if (!observer) {
    observer = new ResizeObserver((entries) => {
      for (const { target } of entries) {
        const element = wrappers.get(target);
        if (element && !element.isConnected) clearHostMathTag(element);
        else if (element) scheduleMeasurement(element);
      }
    });
    document.fonts.ready.then(() => {
      for (const element of live) scheduleMeasurement(element);
    });
  }
  wrappers.set(wrapper, element);
  live.add(element);
  observer.observe(wrapper);
}

function reportError(error) {
  console.error('Unable to typeset SketchResponse tags with MathJax.', error);
}

function scheduleTypesetting() {
  if (frame !== null || typesetting) return;
  frame = requestAnimationFrame(async () => {
    frame = null;
    const candidates = [...pending];
    pending.clear();
    const batch = [];
    let math;
    typesetting = true;
    try {
      math = await getHostMath();
      if (!math) {
        for (const element of candidates) {
          const tag = tags.get(element);
          if (tag && element.isConnected) {
            tag.content.textContent = tag.value;
            scheduleMeasurement(element);
          }
        }
        return;
      }
      await math.whenReady(() => {
        for (const element of candidates) {
          const tag = tags.get(element);
          if (!tag || !element.isConnected || tag.rendered === tag.value)
            continue;
          // Startup's page scan may already have processed this content.
          math.typesetClear([tag.content]);
          tag.rendered = null;
          const value = tag.value;
          tag.content.textContent = value;
          tag.typesetting = true;
          batch.push({ element, tag, value });
        }
      });
      // Enqueue outside whenReady: awaiting a nested queued operation deadlocks.
      if (batch.length) {
        await math.typesetPromise(batch.map(({ tag }) => tag.content));
        for (const { tag, value } of batch) tag.rendered = value;
      }
    } catch (error) {
      // Failed content stays dirty so a later render can retry the same value.
      reportError(error);
    } finally {
      const removed = [];
      for (const { element, tag } of batch) {
        tag.typesetting = false;
        if (tags.get(element) === tag && element.isConnected) {
          scheduleMeasurement(element);
        } else {
          removed.push(tag.content);
        }
      }
      if (removed.length) {
        await math
          .whenReady(() => math.typesetClear(removed))
          .catch(reportError);
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
    observe(element, wrapper);
  }
  tag.value = value;
  tag.align = align;
  scheduleMeasurement(element);
  if (tag.rendered !== value) {
    pending.add(element);
    scheduleTypesetting();
  }
}

export function clearHostMathTag(element) {
  const tag = tags.get(element);
  pending.delete(element);
  measurements.delete(element);
  live.delete(element);
  tags.delete(element);
  if (!tag) return;
  observer.unobserve(tag.wrapper);
  wrappers.delete(tag.wrapper);
  // An in-flight batch clears removed content when its typesetting settles.
  if (!tag.typesetting) {
    getHostMath()
      .then((math) => math?.whenReady(() => math.typesetClear([tag.content])))
      .catch(reportError);
  }
}
