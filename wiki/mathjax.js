window.MathJax = {
     loader: {
        paths: { 'mathjax-stix2': '/wiki/assets/mathjax' }
    },
    chtml: { font: 'mathjax-stix2' },
    tex: {
        inlineMath: [["$", "$"], ["\\(", "\\)"]],
        displayMath: [["$$", "$$"], ["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true
    },
    options: { processHtmlClass: "arithmatex" }
};