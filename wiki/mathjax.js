window.MathJax = {
    loader: {
        paths: { 'mathjax-stix2': '/assets/mathjax' }
    },
    tex: {
        inlineMath: [["$", "$"], ["\\(", "\\)"]],
        displayMath: [["$$", "$$"], ["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true
    },
    options: {
        processHtmlClass: "arithmatex"
    }
};