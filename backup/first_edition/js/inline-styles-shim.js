// Runtime shim: replace inline style attributes with pre-defined external classes
// Maps exact inline style strings to the class names created in styles.css
(function(){
  const map = new Map([
    ["font-size: 37.95px;", "ex-style-1"],
    ["pointer-events: auto;", "ex-style-2"],
    ["right: 0px; left: 0px;", "ex-style-3"],
    ["display: none;", "ex-style-4"],
    ["top: 20px; inset-inline-end: 0px;", "ex-style-5"],
    ["min-width: 20px; min-height: 20px;", "ex-style-6"],
    ["top: -999px; left: -999px;", "ex-style-7"],
    ["text-align: left;", "ex-style-8"],
    ["width: 100%; height: fit-content;", "ex-style-9"],
    ["min-width: 16px; min-height: 16px; color: var(--theme-icon-quaternary);", "ex-style-10"],
    ["width: 12px; height: 12px; border-radius: 50%;", "ex-style-11"],
    ["min-width: 16px; min-height: 16px; margin-right: 4px;", "ex-style-12"],
    ["min-width: 12px; min-height: 12px;", "ex-style-13"]
  ]);

  function normalize(s){
    return s.trim().replace(/\s+/g, ' ').replace(/\s*;\s*$/,';');
  }

  function migrateOnce(){
    const nodes = Array.from(document.querySelectorAll('[style]'));
    if(nodes.length === 0) return;
    nodes.forEach(el => {
      const raw = el.getAttribute('style');
      if(!raw) return;
      const n = normalize(raw);
      const className = map.get(n);
      if(className){
        el.classList.add(className);
        el.removeAttribute('style');
      }
    });
  }

  // Run on DOMContentLoaded and also later in case dynamic content is added
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', migrateOnce);
  } else {
    setTimeout(migrateOnce, 0);
  }

  // Observe additions: when new elements with inline style are added, migrate them
  const mo = new MutationObserver(muts => {
    let found = false;
    muts.forEach(m => {
      m.addedNodes && m.addedNodes.forEach(node => {
        if(node.nodeType === 1){
          if(node.hasAttribute && node.hasAttribute('style')) found = true;
          if(node.querySelector && node.querySelector('[style]')) found = true;
        }
      });
    });
    if(found) migrateOnce();
  });
  mo.observe(document.documentElement || document.body, { childList: true, subtree: true });
})();
