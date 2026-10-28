# PantryPilot

PantryPilot is a small Model Context Protocol (MCP) server for managing a household pantry. It stores items in a local SQLite database and exposes them to any MCP client through six tools and one resource, so an AI assistant can add food, update quantities, and flag items that are about to expire using plain language.

I built it to learn MCP by building something real, testing every tool in process with a Python MCP client.

## Features

- Add, list, update and remove pantry items (name, quantity, unit, expiry date)
- Expiry tracking: list everything that is expired or expires within N days
- Case-insensitive item matching
- Data persists between runs in a local `pantry.db` file (created automatically)
- A `pantry://current` resource that an MCP client can read as context, for example to suggest recipes or a shopping list from what is in stock

## Tools

| Tool | Arguments | What it does |
|---|---|---|
| `ping` | none | Health check |
| `add_item` | `name`, `quantity`, `unit` (optional), `expiry_date` (optional, `YYYY-MM-DD`) | Adds an item |
| `list_items` | none | Lists every item with quantity and expiry |
| `update_quantity` | `name`, `new_quantity` | Sets a new quantity for matching items |
| `remove_item` | `name` | Removes all entries matching the name |
| `check_expiring` | `days` (default 7) | Lists expired items and items expiring within `days` |

## Resource

| URI | Contents |
|---|---|
| `pantry://current` | Current pantry contents, ordered by expiry date |

Recipe ideas need no extra code on the server side. A client reads this resource and the model reasons over it.

## Tech stack

- Python 3.10+
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (`mcp[cli]`)
- SQLite (standard library `sqlite3`)

## Getting started

1. Clone the repo and create a virtual environment:

   ```bash
   git clone https://github.com/ritik90/PantryPilot.git
   cd PantryPilot
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the test client. It starts the server in process, calls every tool, reads the resource, and cleans up after itself, so it is safe to run many times:

   ```bash
   python test_client.py
   ```

4. Optional: explore the tools in the MCP Inspector:

   ```bash
   mcp dev server.py
   ```

## Example output

```
tools: ['add_item', 'check_expiring', 'list_items', 'ping', 'remove_item', 'update_quantity']
ping: PantryPilot is up and running!
list_items:
- demo-milk: 2.0 liters, expires 2026-10-31
- demo-yogurt: 1.0 tub, expires 2026-10-26
update_quantity: Updated DEMO-MILK to 1.0.
check_expiring:
- demo-yogurt: 1.0 tub (EXPIRED)
- demo-milk: 1.0 liters (expires 2026-10-31)
resource pantry://current:
- demo-yogurt: 1.0 tub, expires 2026-10-26
- demo-milk: 1.0 liters, expires 2026-10-31
remove_item: Removed 1 entry of demo-milk from the pantry.
remove_item: Removed 1 entry of demo-yogurt from the pantry.
after cleanup: The pantry is empty.
```

## Project structure

```
PantryPilot/
  server.py          MCP server: SQLite setup, six tools, one resource
  test_client.py     In-process test that exercises every tool and the resource
  requirements.txt   Python dependencies
```

## How it works

`server.py` creates a `pantry_items` table on startup if it does not exist (`id`, `name`, `quantity`, `unit`, `expiry_date`, `added_date`). Each tool opens a short SQLite connection, runs one query, and returns a readable string. The database path is resolved relative to `server.py`, so it works no matter where the process is launched from.

## Known limitations

- Claude Desktop integration is not working yet. The server was tested with a Python MCP client and the MCP Inspector, but Claude Desktop's chat interface did not pick up the tools in my setup.
- `remove_item` deletes every entry with a matching name, and `update_quantity` updates every matching entry. There is no per-row id yet.
- `add_item` does not merge duplicates, so adding the same item twice creates two rows.
- Expiry dates must be `YYYY-MM-DD`. Rows in any other format are skipped by `check_expiring`.

## Ideas for next steps

- Merge duplicate items and support removing part of a quantity
- Categories and low-stock alerts
- Shopping list tool built from low or expired items
- Get the Claude Desktop connection working and add a short demo
