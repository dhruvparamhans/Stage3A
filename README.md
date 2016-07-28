# Non linear fit to absorption spectra 

Provides a simple and interactive way to fit absorption curves for Rubidium atoms. 

To run the application, a certain number of dependencies are required. The simplest way is to have a working distribution of conda working on your machine. For more details go [here](https://www.continuum.io/downloads). 

Once you have conda installed on your machine, from a console run the following command

    conda install --file conda-requirements.txt

This should install the necessary dependencies. If you do not wish to install the complete conda suite, you can install the dependenices by running 

		pip install -r requirements.txt
		
Once these dependencies are installed, verify that bokeh is installed correctly by typing 

		bokeh info

This should give something like 

		Python version      :  2.7.12 |Anaconda 4.0.0 (64-bit)| (default, Jul  2 2016, 17:42:40) 
		IPython version     :  4.1.2
		Bokeh version       :  0.12.0
		BokehJS static path :  /home/dhruv/anaconda2/lib/python2.7/site-packages/bokeh/server/static
		
Once this has been verified, run the app by typing in a shell 

		bokeh serve --show fit_app.py

This should automatically open a browser window where the app will run. Usually the address is 

		localhost:5006/fit_app


