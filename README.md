# ACT-12.4.1 

ORTHODONTIC SOFTWARE INTEROPERABILITY Introductory Presentation

See it live [http://www.open-ortho.org/ACT-12.4.1/](http://www.open-ortho.org/ACT-12.4.1/).

## How to edit this document

This presentation is written using the [reveal.js presentation framework](https://revealjs.com/).

* Slide content are in the [index.html](./index.html) file. Add and remove slides by adding and removing `<section>` tags.
* Slide configuration is also in the [index.html](./index.html) file.
* The framework is in the [dist](./dist) and [plugin](./plugin) folders.
* Vie the changes by opening the `index.html` file with your browser.

### Adding QR Codes

1. Install `qrencode` with `apt`, `yum`, `brew`, ...
2. `qrencode -t SVG -o ./presentations/mypresentation_url_qrcode.svg "https://open-ortho.org/"`

## Deployment

This project is being hosted as a static site on GitHub Pages from the `main` branch. Committing and pushing to the master branch will deploy the presentation.


## Upgrading Reveal-JS

1. Download latest [zip compiled from github](https://github.com/hakimel/reveal.js/archive/master.zip).
2. Unzip
3. Replace `dist/` and `plugin/` folders with the ones found in the zip archive. Example:

        cd ~/Downloads
        curl -O https://github.com/hakimel/reveal.js/archive/master.zip
        unzip ~/Downloads/master.zip
        cd -
        rsync -av --delete ~/Downloads/reveal.js-master/plugin/ plugin/
        rsync -av --delete ~/Downloads/reveal.js-master/dist/ dist/

