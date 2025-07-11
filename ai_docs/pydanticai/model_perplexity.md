## OpenAI-compatible Models

Many models are compatible with the OpenAI API, and can be used with OpenAIModel in PydanticAI. Before getting started, check the installation and configuration instructions above.


## Perplexity
Follow the Perplexity getting started guide to create an API key. Then, you can query the Perplexity API with the following:

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'sonar-pro',
    provider=OpenAIProvider(
        base_url='https://api.perplexity.ai',
        api_key='your-perplexity-api-key',
    ),
)
agent = Agent(model)
...
```