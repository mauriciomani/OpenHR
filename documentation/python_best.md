# How should I write my code to follow the best practices on OpenHR 

## This is a very short summary on the most important PEP 8 conventions & documenting Python.
We highly recommend you follow this conventions. However remember this is not necessary for the well functioning of the code, but on the form of the same. Currently is better to make functioning code, however, since this project is to follow the best, we recommend you do it on the form as well.
### Writing Python code
* Try to keep all your lines limited to **72 characters**. 
* Avoid line breaks after a binary operator (this was a common recommended style), since this make readability more difficult
* Kindly surround with **2 blank lines, both functions and classes**.
* Do not add white spaces inmediately inside parenthesis, brackets or braces. And add spaces after commas, semicolons or colons.
* Classes should begin with capital letter and naming constants should have all letters uppercase. For function names, variables and modules keep all lower case. 
* Remember is better to have explicit rather than implicit names.
* Comments should be initialized in capital letter and be written in english, plus, they should be complete sentences
* Separate inline comments by at least 2 spaces, and try to avoid them. Do not explain obvious, unless it is to keep follow. 


For more information on PEP 8, please visit the following [official link](https://www.python.org/dev/peps/pep-0008/) or a nice [summary](https://realpython.com/python-pep8/).


### Documenting your functions and classes
We will focus in documenting Python code base using docstrings specified in PEP 257 and specifically **class docstrings**. We mainly follow the [NumPy/SciPy Docstrings](https://numpydoc.readthedocs.io/en/latest/format.html) This are very helpful when using **help** and we need to include:
* Description of what is used for.
* Arguments
* Exceptions

Then you will document a class as:
```
class OpenHR:
    """
    A class used to represent OpenHR example

    ...

    Attributes
    ----------
    help : str
        a formatted string to print what OpenHR is
    contributors : list
        name of all contributors

    Methods
    -------
    any_function(any_arg=None)
        Do anything helpful for the class
    """
```

And functions will be documented as:
```
def any_function(self, any_arg=None):
    """Do anything helpful for the class.
    If any_args is not passed then it will happen something special.

    Parameters
    ----------
    any_args : str, optional
        Anything useful for the any_function (default is None)
    
    Returns
    -------
    list
        A list of all the things you can do

    Raises
    ------
    NotImplementedError
        If no any_args is set.
    """
```

For more information, please visit [PEP 257](https://www.python.org/dev/peps/pep-0257/) or a [more comprehensive guide](https://realpython.com/documenting-python-code/)

### Using OpenHR for your repos exposition
I highly recommend you use [cookiecutter](https://github.com/cookiecutter/cookiecutter) to make sure your python project has all the necessary files, it has a 12 factor philosophy. Also use lint-like tools to perform static analysis on the quality of your code. You can use [Flake8](https://flake8.pycqa.org/en/latest/) to test your code against PEP8. If follow PEP 257 you can use [Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html) to **auto-generate** documentation.