Ideogram provides functions for generating visualizations of software projects. The source code is parsed for functions, function calls, classes, and methods. This data can be used to construct d3 visualizations from mustache templates.

ow to use it

In order to get started creating, you must create some Ideogram objects and generate them. For example:

import ideogram 

netwk = ideogram.Ideogram(outdir='network_viz',
                          mode='network',
                          title='Hola, mundo!',
                          font_family='sans-serif',
                          font_size='60px',
                          title_color='rgb(0,0,0)',
                          colorscheme='Spectral',
                          bgcolor='rgb(155,45,0)'
                          )
pack = ideogram.Ideogram(outdir='pack_viz',
                         mode='pack',
                         colorscheme='random',
                         bgcolor='random'
                         )
ideogram.generate('https://github.com/brmscheiner/ideogram',netwk,pack)

Ideogram objects are instantiated with several keyword arguments, which afford some control over the final product. See github.com/brmscheiner/ideogram for more information.

After you're done building your Ideogram objects, pass them to the generate function along with the path to a local directory that contains some Python source code.

ideogram.generate('Desktop/code/myproject',thing1,thing2,thing3)

The generate function also accepts links to github projects.

ideogram.generate('https://github.com/brmscheiner/ideogram',thing1,thing2,thing3,thing4)

Still here? OK, last step! To see your creation, you need to host the output files on a server. Depending on your background that might sound intimidating, but the good news is there's an easy-to-use Python module that takes care of the heavy lifting for you. If you have Python 2, it's called SimpleHTTPServer. In Python 3 it's called http.server. If you're not sure which version of Python is on your computer, just open the terminal and type python --version. Now, navigate to the directory where you put your Ideograms and start serving:

cd path/to/output/files
python -m http.server 8080       OR        python -m SimpleHTTPServer 8080

You should see a message like Serving HTTP on 0.0.0.0 port 8080 ..., possibly followed by some gibberish. All you have to do now is open Chrome or Firefox and navigate to http://localhost:8080/. If everything went according to plan, you should see your visualization! For large projects, it could take a minute for the page to load and process the data.

Credit

This is my first Python package! Many thanks to Drew Garrido, James Porter, Diwank Tomer, and Oren Shoham for their help putting it all together. 