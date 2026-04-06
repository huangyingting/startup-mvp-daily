document.addEventListener('DOMContentLoaded', () => {
  const tabs = Array.from(document.querySelectorAll('.scenario-tab'));
  if (!tabs.length) return;

  const activate = (tab) => {
    const target = document.querySelector(tab.dataset.tabTarget);
    if (!target) return;

    tabs.forEach((item) => {
      item.setAttribute('aria-pressed', String(item === tab));
      const panel = document.querySelector(item.dataset.tabTarget);
      if (panel) panel.hidden = item !== tab;
    });
  };

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => activate(tab));
  });
});
