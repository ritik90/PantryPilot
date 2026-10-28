import asyncio
from mcp import Client
from server import mcp

async def main():
    async with Client(mcp) as client:
        await client.call_tool("add_document", {
            "text": "KV-cache quantization reduces memory usage during LLM inference by storing cached key/value tensors at lower precision.",
            "source": "dissertation notes"
        })
        await client.call_tool("add_document", {
            "text": "STAR method: Situation, Task, Action, Result — use it to structure behavioral interview answers.",
            "source": "interview prep"
        })

        result = await client.call_tool("search_knowledge", {"query": "how to answer behavioral interview questions"})
        print("search result:\n" + result.structured_content["result"])

asyncio.run(main())