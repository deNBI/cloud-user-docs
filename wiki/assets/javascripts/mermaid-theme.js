/*
 * Adds the de.NBI figure style to Material's Mermaid theme: 1.5px lines,
 * 8px node corners, tinted subgraphs and navy numbers on cyan circles in
 * sequence diagrams. Colours come from the CSS variables
 * in assets/css/denbi.css. Material renders each diagram in a closed shadow
 * root, so this CSS is passed to mermaid.initialize instead of a stylesheet.
 * Load this before Material's bundle, which loads and initialises Mermaid.
 */
(function () {
  var figureCSS =
    ".node rect,.node polygon,.node circle,.node ellipse,.node path{stroke-width:1.5px}" +
    ".node rect{rx:8px;ry:8px}" +
    ".edgePath .path,.flowchart-link{stroke-width:1.5px}" +
    ".cluster rect{fill:var(--denbi-mermaid-cluster-bg-color);stroke:none;rx:8px;ry:8px}" +
    "rect.actor{stroke-width:1.5px;rx:8px;ry:8px}" +
    ".actor-line{stroke:var(--md-mermaid-sequence-actor-line-color)}" +
    ".messageLine0,.messageLine1{stroke-width:1.5px}" +
    "marker[id$='-sequencenumber'] circle{fill:var(--md-mermaid-sequence-number-bg-color)}" +
    "marker[id$='-arrowhead'] path,marker[id$='-crosshead'] path{fill:var(--md-mermaid-edge-color);stroke:var(--md-mermaid-edge-color)}";

  function patch(mermaid) {
    if (!mermaid || mermaid.denbiThemed || typeof mermaid.initialize !== "function") {
      return mermaid;
    }
    var initialize = mermaid.initialize.bind(mermaid);
    mermaid.initialize = function (config) {
      config = Object.assign({}, config);
      config.themeCSS = (config.themeCSS || "") + figureCSS;
      return initialize(config);
    };
    mermaid.denbiThemed = true;
    return mermaid;
  }

  if (window.mermaid) {
    patch(window.mermaid);
    return;
  }
  var current;
  Object.defineProperty(window, "mermaid", {
    configurable: true,
    get: function () { return current; },
    set: function (value) { current = patch(value); }
  });
})();
