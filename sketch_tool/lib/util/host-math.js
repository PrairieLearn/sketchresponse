export async function getHostMath() {
  // Async host scripts may not have installed their startup promise yet.
  if (document.readyState === 'loading' && !window.MathJax?.startup?.promise) {
    await new Promise((resolve) =>
      window.addEventListener('load', resolve, { once: true }),
    );
  }
  await window.MathJax?.startup?.promise;
  const math = window.MathJax;
  return typeof math?.typesetPromise === 'function' &&
    typeof math?.whenReady === 'function'
    ? math
    : null;
}
