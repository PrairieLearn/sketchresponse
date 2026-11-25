const config = {
  width: 800,
  height: 450,
  xrange: [-4, 4],
  yrange: [-2.25, 2.25],
  enforceBounds: true,
  plugins: [
    { name: 'axes', id: 'axes' },
    {
      name: 'spline',
      id: 'reference',
      readonly: true,
      color: 'purple',
      tag: { xoffset: 8, yoffset: -12, align: 'start', position: 'start' },
    },
    { name: 'point', id: 'p', label: 'Point \\((x, y)\\)' },
    { name: 'line-segment', id: 'line' },
    {
      name: 'group',
      id: 'curves',
      label: 'Curves \\(f(x)\\)',
      plugins: [
        { name: 'polyline', id: 'poly', label: 'Polyline \\(C_1\\)' },
        { name: 'spline', id: 'spline', label: 'Spline \\(C_2\\)' },
      ],
    },
    {
      name: 'freeform',
      id: 'free',
      label: 'Cubic branch for \\(x < 1\\)',
    },
  ],
  initialstate: {
    reference: [
      [
        { x: 200, y: 125, tag: 'Reference \\(f(x) = \\frac{x^2}{4}\\)' },
        { x: 400, y: 225 },
        { x: 600, y: 125 },
      ],
    ],
  },
};

function embed(target, id, options) {
  const container = document.createElement('div');
  container.id = `${id}-si-container`;
  container.className = 'si-container';
  container.tabIndex = 0;
  document.getElementById(target).append(container);
  return new window.sketchresponse.default(container, id, options);
}

embed('question', 'question', { ...config });
const submission = embed('submission', 'submission', {
  ...config,
  readonly: true,
  plugins: [
    ...config.plugins,
    {
      name: 'line-segment',
      id: 'solution',
      readonly: true,
      overlay: true,
      color: 'green',
      tag: { xoffset: 8, yoffset: -12, align: 'start', position: 'end' },
    },
  ],
  initialstate: {
    ...config.initialstate,
    p: [{ x: 400, y: 225 }],
    solution: [
      { x: 200, y: 350, tag: 'Solution \\(y = \\frac{5x}{8}\\)' },
      { x: 600, y: 100 },
    ],
    line: [
      { x: 200, y: 325 },
      { x: 600, y: 125 },
    ],
  },
});

embed('all-tools', 'all-tools', {
  ...window.loadConfig('allPlugins'),
  width: config.width,
  height: config.height,
});

embed(
  'instructor-labels',
  'instructor-labels',
  window.loadConfig('instructorLabels'),
);

submission.messageBus.on('ready', () => {
  const wrapper = document.createElement('div');
  wrapper.className = 'position-relative';
  wrapper.innerHTML = `
    <button
      id="overlay-toggle"
      type="button"
      class="js-overlay-toggle btn btn-light border border-dark position-absolute translate-middle bottom-0 end-0 m-3"
      title="Toggle solution display"
      aria-label="Toggle solution display"
      aria-pressed="true"
    >
      <i class="bi bi-layers-fill" aria-hidden="true"></i>
    </button>
  `;
  submission.el.append(wrapper);
  const overlayToggle = wrapper.querySelector('button');
  overlayToggle.addEventListener('click', () => {
    const visible = overlayToggle.getAttribute('aria-pressed') !== 'true';
    overlayToggle.setAttribute('aria-pressed', String(visible));
    submission.el.querySelectorAll('.overlay').forEach((el) => {
      el.style.display = visible ? '' : 'none';
    });
    const icon = overlayToggle.querySelector('i');
    icon.classList.toggle('bi-layers-fill', visible);
    icon.classList.toggle('bi-layers-half', !visible);
  });
});
