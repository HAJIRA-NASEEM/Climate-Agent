import os
import chainlit as cl
from dotenv import load_dotenv
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    Agent,
    Runner,
    function_tool,
    RunConfig,
    input_guardrail,
    output_guardrail,
    set_tracing_disabled,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)

from agents.extensions.models.litellm_model import LitellmModel


load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

model = LitellmModel(
    model="gemini/gemini-2.0-flash",
    api_key=gemini_api_key,
)

run_config = RunConfig(
    model=model,
    tracing_disabled=True
)


@input_guardrail
def check_input(text: str) -> str:
    blocked_words = ["hack", "bomb", "kill"]
    if any(word in text.lower() for word in blocked_words):
        raise InputGuardrailTripwireTriggered("Inappropriate language detected.")
    return text


@output_guardrail
def check_output(text: str) -> str:
    if "i don't know" in text.lower():
        raise OutputGuardrailTripwireTriggered("Model returned an unhelpful response.")
    return text

@function_tool
def policy_advice(topic: str) -> str:
    return f"As a policy expert, I recommend carbon pricing in {topic}."

@function_tool
def get_co2_stats(location: str) -> str:
    return f"{location} emitted ~5.2 metric tons of CO2 per capita in 2024."

@function_tool
def suggest_green_practices(topic: str) -> str:
    return f"To reduce emissions in {topic}, use renewable energy and optimize efficiency."


climate_agent = Agent(
    name="Climate Agent",
    instructions="""
You are a helpful assistant who answers climate-related questions using the correct tool:
- Use `policy_advice` for laws and agreements.
- Use `get_co2_stats` for emissions.
- Use `suggest_green_practices` for eco advice.
    """,
    tools=[policy_advice, get_co2_stats, suggest_green_practices]
)

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    user_input = message.content.strip()

    if user_input.lower() in ["hi", "hello", "hey", "salam", "assalamualaikum"]:
        await cl.Message(content=" Hello! I'm your Climate Agent. Ask me about sustainability, CO2 stats, or policy.").send()
        return

    msg = cl.Message(content="")
    await msg.send()
    history.append({"role": "user", "content": user_input})

    try:
        result = Runner.run_streamed(
            climate_agent,
            input=history,
            run_config=run_config,
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)

        history.append({"role": "assistant", "content": result.final_output})

    except InputGuardrailTripwireTriggered as e:
        await msg.update(content=f"Input blocked: {str(e)}")
    except OutputGuardrailTripwireTriggered as e:
        await msg.update(content=f"Output blocked: {str(e)}")
    except Exception as e:
        await msg.update(content=f"Unexpected error: {str(e)}")

    cl.user_session.set("history", history)