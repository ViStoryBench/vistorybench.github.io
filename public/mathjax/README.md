MathJax fonts
=============

To render equations offline we need MathJax’s CHTML font assets. Copy the
contents of `output/chtml/fonts/woff-v2` from an official MathJax 3 release
into this folder so the runtime can load the CSS (`tex-woff-v2.css`) and all
`.woff2` files such as `MathJax_Main-Regular.woff2`.

A quick way to collect them is:

1. Download the MathJax bundle once, for example  
   `npx degit mathjax/MathJax#3.2.2 es5` or copy it from
   `node_modules/mathjax-full/es5` if you already have the package locally.
2. Copy `es5/output/chtml/fonts/woff-v2` into `public/mathjax/fonts/woff-v2`.

After the files are in place, `src/pages/metrics.astro` will point MathJax to
`mathjax/fonts/woff-v2` so the site continues to work without an internet
connection.
