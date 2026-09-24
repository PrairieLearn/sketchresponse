import z from './util/zdom';

/** @knipignore */
export const VERSION = '0.1';
const TOOLBAR_ID = '$__toolbar';
const FIXED_CONTROLS = new Set(['delete', 'undo', 'redo', 'help']);

// from http://stackoverflow.com/a/5775621/1974654
const NULL_SRC = '//:0';

function renderIcon(id, src, alt) {
  return z('img.icon', {
    id,
    src: src || NULL_SRC,
    alt,
  });
}

function renderLabel(id, text, hasDropdown) {
  return z(
    'div.label',
    z('span', { id }, text),
    z.if(
      hasDropdown,
      z('span', { 'aria-label': 'Open dropdown menu' }, ' \u25be'),
    ),
  );
}

export default class Toolbar {
  constructor(id, params, app) {
    this.id = id;
    this.params = params;
    this.app = app;
    this.el = document.getElementById(`${id}-si-toolbar`); // TODO: pass container element in

    this.isActive = false;
    this.focusedItemID = null;
    this.openDropdownID = null; // TODO: better name
    this.overflowOpen = false;

    if (!params.readonly) {
      let resizeFrame;
      const observer = new ResizeObserver(() => {
        cancelAnimationFrame(resizeFrame);
        resizeFrame = requestAnimationFrame(() => this.updateOverflow());
      });
      observer.observe(this.el);
    }

    this.items = [
      {
        id: TOOLBAR_ID,
        activate: this.activate.bind(this),
        deactivate: this.deactivate.bind(this),
      },
    ];

    this.activeItemID = null;
    this.selectedDropdownItemMap = {}; // TODO: better name

    app.registerState({
      id: TOOLBAR_ID,
      dataVersion: VERSION,
      getState: this.getState.bind(this),
      setState: this.setState.bind(this),
    });

    app.__messageBus.on(
      'registerToolbarItem',
      this.registerToolbarItem.bind(this),
    );
    app.__messageBus.on('activateItem', this.activateItem.bind(this));
    app.__messageBus.on('closeDropdown', this.closeDropdown.bind(this));
  }

  // Called when the toolbar plugin itself is activated
  activate() {
    this.isActive = true;
    // TODO: attach keyboard shortcuts here <<<
    this.render();
  }

  deactivate() {
    this.isActive = true;
    // TODO: detach keyboard shortcuts here <<<
    this.render();
  }

  getState() {
    return {
      activeItemID: this.activeItemID,
      selectedDropdownItemMap: this.selectedDropdownItemMap,
    };
  }

  setState(state) {
    this.selectedDropdownItemMap = state.selectedDropdownItemMap;
    this.activateItem(state.activeItemID);
    this.render();
  }

  activateItem(id) {
    if (id === this.activeItemID) return;
    try {
      const allItems = [];
      this.items.forEach((item) => {
        if (item.name === 'group') {
          item.items.forEach((it) => {
            allItems.push(it);
          });
        } else {
          allItems.push(item);
        }
      });
      const oldActiveItem = allItems.find(
        (item) => item.id === this.activeItemID,
      );
      const newActiveItem = allItems.find((item) => item.id === id);

      oldActiveItem && oldActiveItem.deactivate();
      newActiveItem && newActiveItem.activate();

      this.activeItemID = id;
    } catch (error) {
      this.app.__messageBus.emit('warnUser', 'pluginError', error);
    }
    this.render();
  }

  registerToolbarItem(item) {
    if (item.type === 'splitbutton') {
      if (!item.items || !item.items[0] || !item.items[0].id) {
        throw new TypeError(
          'Toolbar split buttons must contain at least one item',
        );
      }
      this.selectedDropdownItemMap[item.id] = item.items[0].id;
    }
    this.items.push(item);
    this.render();
  }

  openDropdown(id) {
    this.openDropdownID = id;
    this.render();
  }

  closeDropdown(event) {
    if (
      event &&
      this.el.contains(event.target) &&
      (event.target.closest('.si-dropdown') ||
        (!this.openDropdownID && event.target.closest('.si-more')))
    )
      return;
    this.setOverflowOpen(false);
    this.openDropdownID = null;
    this.render();
  }

  selectDropdownItem(id, itemId) {
    this.openDropdownID = null;
    this.selectedDropdownItemMap[id] = itemId;
    this.app.__messageBus.emit('finalizeShapes', itemId);
    this.app.__messageBus.emit('activateItem', itemId);
    this.render();
  }

  setOverflowOpen(open) {
    this.overflowOpen = open;
    const button = this.el.querySelector('.si-more-toggle');
    const menu = this.el.querySelector('.si-overflow-menu');
    if (!button) return;
    button.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
  }

  updateOverflow() {
    if (this.params.readonly || !this.el.clientWidth) return;
    const more = this.el.querySelector('.si-more');
    if (!more) return;
    const elements = [
      ...this.el.querySelectorAll(':scope > .item:not(.si-more)'),
    ];
    const separators = [...this.el.querySelectorAll(':scope > hr')];
    const items = this.items.filter((item) =>
      ['button', 'splitbutton'].includes(item.type),
    );
    // Measure hidden tools too, so they can return when the toolbar grows.
    elements.forEach((el) => {
      el.hidden = false;
    });
    const widths = elements.map((el) => el.getBoundingClientRect().width);
    const available = this.el.clientWidth;
    const fits =
      widths.reduce((sum, width) => sum + width, 0) + separators.length * 16 <=
      available;
    more.hidden = fits;
    separators.forEach((el) => {
      el.hidden = !fits && el !== separators[separators.length - 1];
    });
    const visible = new Set();
    if (fits) {
      items.forEach((item) => visible.add(item.id));
    } else {
      // Reserve More, the trailing separator, and all four action controls first.
      let remaining = available - more.getBoundingClientRect().width - 9;
      items.forEach((item, index) => {
        if (FIXED_CONTROLS.has(item.id)) {
          visible.add(item.id);
          remaining -= widths[index];
        }
      });
      const tools = items
        .map((item, index) => ({ item, width: widths[index] }))
        .filter(({ item }) => !FIXED_CONTROLS.has(item.id));
      // Reserve a stable slot so a narrower active tool cannot reveal extra tools.
      const slotWidth = Math.min(
        remaining,
        Math.max(0, ...tools.map(({ width }) => width)),
      );
      remaining -= slotWidth;
      // Keep a contiguous prefix; filling gaps would pull later tools past this slot.
      for (const { item, width } of tools) {
        if (width > remaining) break;
        visible.add(item.id);
        remaining -= width;
      }
      const overflow = tools.filter(({ item }) => !visible.has(item.id));
      const active = overflow.find(
        ({ item }) =>
          item.id === this.activeItemID ||
          item.items?.some((child) => child.id === this.activeItemID),
      );
      const promoted =
        active && active.width <= slotWidth
          ? active
          : overflow.find(({ width }) => width <= slotWidth);
      if (promoted) visible.add(promoted.item.id);
    }
    elements.forEach((el, index) => {
      el.hidden = !visible.has(items[index].id);
    });
    const overflowItems = items.filter((item) => !visible.has(item.id));
    this.renderOverflowMenu(overflowItems);
    if (fits) this.setOverflowOpen(false);
  }

  renderOverflowMenu(items) {
    const menu = this.el.querySelector('.si-overflow-menu');
    z.render(
      menu,
      z.each(items, (item) => {
        if (item.type === 'splitbutton') {
          // Flatten tool groups into sections rather than nesting dropdowns.
          return z(
            'div',
            { role: 'group', 'aria-label': item.label },
            z('div.si-overflow-heading', item.label),
            z.each(item.items, (child) =>
              this.renderDropdownButton(child, item.id, true),
            ),
          );
        }
        return this.renderDropdownButton(item, null, true);
      }),
    );
  }

  renderDropdownButton(item, groupId, overflow = false) {
    const id = `${this.id}-${overflow ? 'overflow' : groupId}-${item.id}`;
    return z(
      'div.si-dropdown-item',
      z(
        'button.si-dropdown-button',
        {
          id,
          type: 'button',
          ...(overflow
            ? {
                'data-is-active': String(item.id === this.activeItemID),
              }
            : {}),
          onclick: () => {
            if (overflow) this.setOverflowOpen(false);
            if (groupId) this.selectDropdownItem(groupId, item.id);
            else {
              this.app.__messageBus.emit('finalizeShapes', item.id);
              item.action ? item.action() : this.activateItem(item.id);
            }
          },
        },
        renderIcon(`${id}-icon`, item.icon.src, ''),
        renderLabel(`${id}-label`, item.label, false),
      ),
    );
  }

  renderMore() {
    return z(
      'div.item.si-more',
      {
        hidden: true,
        // The legacy canvas double-tap workaround suppresses quick menu selections.
        ontouchstart: (event) => event.stopPropagation(),
      },
      z(
        'button.si-more-toggle',
        {
          type: 'button',
          'aria-expanded': String(this.overflowOpen),
          'aria-controls': `${this.id}-overflow-menu`,
          onclick: () => this.setOverflowOpen(!this.overflowOpen),
        },
        z('span.icon.si-more-icon', { 'aria-hidden': 'true' }, '⋯'),
        renderLabel(`${this.id}-more-label`, 'More', false),
      ),
      z('menu.si-dropdown.si-overflow-menu', {
        id: `${this.id}-overflow-menu`,
        hidden: !this.overflowOpen,
      }),
    );
  }

  render() {
    const renderableItems = this.items.filter(
      (item) => ['separator', 'button', 'splitbutton'].indexOf(item.type) >= 0,
    );

    const separatorIndex = renderableItems.findLastIndex(
      (item) => item.type === 'separator',
    );
    renderableItems.splice(
      separatorIndex === -1 ? renderableItems.length : separatorIndex,
      0,
      { type: 'overflow' },
    );

    z.render(
      this.el,
      z.each(
        renderableItems,
        ({ type, id, icon, label, color, items, action }) => {
          if (type === 'separator') return z('hr');
          if (type === 'overflow') return this.renderMore();
          let selectedItem;
          let isActive;
          if (type === 'splitbutton') {
            selectedItem = items.find(
              (item) => item.id === this.selectedDropdownItemMap[id],
            );
            icon = selectedItem.icon;
            color = selectedItem.color;
            isActive = selectedItem.id === this.activeItemID;
          } else if (type === 'button') {
            isActive = id === this.activeItemID;
          }

          const hasDropdown = items && items.length;
          const isOpen = id === this.openDropdownID;

          return z(
            'div.item',
            {
              id,
              'data-is-open': isOpen,
              'data-is-active': isActive,
              style: isActive ? `border-bottom-color: ${color};` : '',
            },
            z.if(
              type === 'button',
              z(
                'button',
                {
                  onclick: () => {
                    // Finalize any shape that isn't
                    this.app.__messageBus.emit('finalizeShapes', id);
                    action ? action() : this.activateItem(id);
                  },
                  'aria-labelledby': `${id}-label ${id}-icon`,
                  type: 'button',
                },
                renderIcon(`${id}-icon`, icon.src, icon.alt),
                renderLabel(`${id}-label`, label, hasDropdown),
              ),
            ),
            z.if(
              type === 'splitbutton',
              z(
                'button.split-button-main',
                {
                  onclick: () => {
                    // Finalize any shape that isn't
                    this.app.__messageBus.emit(
                      'finalizeShapes',
                      this.selectedDropdownItemMap[id],
                    );
                    this.activateItem(this.selectedDropdownItemMap[id]);
                  },
                  'aria-labelledby': `${id}-label ${id}-icon`,
                  type: 'button',
                },
                renderIcon(`${id}-icon`, icon.src, icon.alt), // TODO: title
              ),
              z(
                'button.split-button-aux',
                {
                  onclick: () => {
                    // Finalize any shape that isn't
                    this.app.__messageBus.emit(
                      'finalizeShapes',
                      this.selectedDropdownItemMap[id],
                    );
                    this.activateItem(this.selectedDropdownItemMap[id]);
                    this.openDropdown(id);
                  },
                  'aria-haspopup': 'true',
                  type: 'button',
                },
                renderLabel(`${id}-label`, label, hasDropdown),
              ),
            ),
            z.if(
              hasDropdown,
              z(
                'menu.si-dropdown',
                { ontouchstart: (event) => event.stopPropagation() },
                z.each(items, (item) => this.renderDropdownButton(item, id)),
              ),
            ),
          );
        },
      ),
    );

    // zdom owns the menu shell; its buttons are updated separately for responsive layout.
    this.updateOverflow();
    this.setOverflowOpen(this.overflowOpen);

    // Update focus if needed
    if (this.isActive && document.activeElement.id !== this.focusedItemID) {
      document.getElementById(`${this.id}-${this.focusedItemID}`).focus();
    }
  }
}
