## Running Agents

- agent.run() — a coroutine which returns a RunResult containing a completed response.
- agent.run_sync() — a plain, synchronous function which returns a RunResult containing a completed response - (internally, this just calls loop.run_until_complete(self.run())).
- agent.run_stream() — a coroutine which returns a StreamedRunResult, which contains methods to stream a response as an async iterable.

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.output)
#> Rome


async def main():
    result = await agent.run('What is the capital of France?')
    print(result.output)
    #> Paris

    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_output())
        #> London
```

### Model (Run) Settings

PydanticAI offers a settings.ModelSettings structure to help you fine tune your requests. This structure allows you to configure common parameters that influence the model's behavior, such as temperature, max_tokens, timeout, and more.

There are two ways to apply these settings: 1. Passing to run{_sync,_stream} functions via the model_settings argument. This allows for fine-tuning on a per-request basis. 2. Setting during Agent initialization via the model_settings argument. These settings will be applied by default to all subsequent run calls using said agent. However, model_settings provided during a specific run call will override the agent's default settings.

For example, if you'd like to set the temperature setting to 0.0 to ensure less random behavior, you can do the following:

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync(
    'What is the capital of Italy?', model_settings={'temperature': 0.0}
)
print(result_sync.output)
#> Rome
```
### Runs vs. Conversations

An agent run might represent an entire conversation — there's no limit to how many messages can be exchanged in a single run. However, a conversation might also be composed of multiple runs, especially if you need to maintain state between separate interactions or API calls.

Here's an example of a conversation comprised of multiple runs:
```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# First run
result1 = agent.run_sync('Who was Albert Einstein?')
print(result1.output)
#> Albert Einstein was a German-born theoretical physicist.

# Second run, passing previous messages
result2 = agent.run_sync(
    'What was his most famous equation?',
    message_history=result1.new_messages(),  # Continue the conversation; without message_history the model would not know who "his" was referring to.
)
print(result2.output)
#> Albert Einstein's most famous equation is (E = mc^2).
```
