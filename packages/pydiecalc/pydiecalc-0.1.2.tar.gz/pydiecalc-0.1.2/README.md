#pydiecalc

##Installation

`pip install pydiecalc`

##Usage

###As a CLI

To run the pydiecalc library as an interactive CLI you run the application
without arguments:

`pydiecalc`

###From the Command Line

To run the pydiecalc library from the command line you run the application with
arguments that will be parsed:

`pydiecalc 1d6 + 10`

###As a library

To use pydiecalc as a library you need to import it and then handle the output:

```
import pydiecalc

result, rolls = pydiecalc.roll('1d6 + 10')
```

`pydiecalc.roll` will raise `CaughtRollParsingError` if the parsing fails.
