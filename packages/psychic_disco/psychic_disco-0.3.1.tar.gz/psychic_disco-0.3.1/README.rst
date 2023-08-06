Psychic Disco
-----------------------------------
Pythonic microservices for AWS Lambda. Define Lambda functions as python modules, automatically create and upload deployment packages, register API Gateway methods to trigger your lambdas. Do that thing where your configuration lives in your code.

Install like so::

 pip install psychic_disco

Assumptions
-----------

 * All your microservices live in python modules
 * All your entrypoints are decorated with @lambda_entry_point

Discovering Entrypoints
-----------------------

Do this thing::

  psychic_disco discover_entrypoints

Or, if your code lives elsewhere::

  psychic_disco --repo path/to/st/elsewhere discover_entrypoints
