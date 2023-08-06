Psychic Disco
-----------------------------------
Pythonic microservices for AWS Lambda. Define Lambda functions as python modules, automatically create and upload deployment packages, register API Gateway methods to trigger your lambdas. Do that thing where your configuration lives in your code.

Install like so::

 pip install psychic_disco

Assumptions
-----------

 * All your microservices live in python modules
 * All your entrypoints are decorated with @lambda_entry_point

Declaring Entrypoints and API methods
-------------------------------------
Make a new entrypoint::

  @lambda_entry_point
  def handler(event, context):
    # important code here

Making a new api method automatically registers the entrypoint::

  @api_method("POST", "/cereal"):
  def create_cereal(event, context):
    # cereal creation logic here

Definitions for your API methods are available in ``psychic_disco.Api``.

Discovering Entrypoints
-----------------------

Do this thing::

  psychic_disco discover_entrypoints

Or, if your code lives elsewhere::

  psychic_disco --repo path/to/st/elsewhere discover_entrypoints

Creating a Deployment Package
-----------------------------
Do this thing::

  psychic_disco bundle

That will make a virtualenv, install your dependencies, and zip it all up for you


