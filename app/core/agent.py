import json
import logging
import time
from typing import Dict, Any
from openai import AsyncOpenAI
from config import settings
from app.core.prompts import SYSTEM_PROMPT
from app.core.tool_definitions import TOOL_DEFINITIONS
from app.core.backend_client import backend_client
from app.core import agent_tools
from app.core.common_utils import generate_conversation_id

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.tool_handlers = {
            "get_order_status": agent_tools.handle_get_order_status,
            "check_stock": agent_tools.handle_check_stock,
            "search_products": agent_tools.handle_search_products,
            "estimate_shipping": agent_tools.handle_estimate_shipping,
            "forward_to_human": agent_tools.handle_forward_to_human,
            "close_case": agent_tools.handle_close_case,
            "reopen_case": agent_tools.handle_reopen_case,
        }
        self.max_iterations = 5

    async def run(self, message: str, email: str, site: str) -> Dict[str, Any]:
        conversation_id = generate_conversation_id(email)
        logger.info(f"Processing {email} on {site}")
        
        history = await backend_client.get_conversation_history(email)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        rag_context = await backend_client.get_context(query=message, email=email)
        if rag_context and rag_context.get("context"):
            messages.append({"role": "system", "content": f"Relevant past info: {rag_context['context']}"})
        
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        final_answer = None
        for i in range(self.max_iterations):
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
                temperature=0.1
            )
            assistant_msg = response.choices[0].message
            messages.append(assistant_msg.model_dump())
            
            if not assistant_msg.tool_calls:
                final_answer = assistant_msg.content or "I couldn't generate a response."
                break
            
            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                handler = self.tool_handlers.get(tool_name)
                if not handler:
                    result = {"error": f"Unknown tool: {tool_name}"}
                else:
                    if tool_name in ["get_order_status", "forward_to_human", "close_case", "reopen_case"]:
                        result = await handler(arguments, email=email)
                    elif tool_name in ["search_products"]:
                        result = await handler(arguments, site=site)
                    else:
                        result = await handler(arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        
        if not final_answer:
            final_answer = "I'm having trouble. Let me forward you to a human."
            await agent_tools.handle_forward_to_human({"reason": "Max iterations"}, email=email)
        
        await backend_client.log_conversation(
            conversation_id=conversation_id,
            customer_email=email,
            question=message,
            ai_answer=final_answer,
            redirected_to_human=("forward_to_human" in str(messages)),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )
        
        return {"answer": final_answer, "conversation_id": conversation_id}

agent = Agent()
