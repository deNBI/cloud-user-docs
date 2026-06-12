window.MathJax = {
      tex: {
          inlineMath: [["$", "$"], ["\\(", "\\)"]],
          displayMath: [["$$", "$$"], ["\\[", "\\]"]],
          processEscapes: true,
          processEnvironments: true
      },
      options: {
          // Remove or comment out the processHtmlClass line to let MathJax
          // process everything unless specifically told not to.
           processHtmlClass: "arithmatex"
      }
  };