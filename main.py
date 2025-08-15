import asyncio
import tkinter as tk
from ui.app import App


async def main():
    loop = asyncio.get_running_loop()
    root = tk.Tk()
    App(root, loop)

    # Integra asyncio com Tkinter
    def tk_update():
        root.update()
        loop.call_later(0.01, tk_update)

    loop.call_soon(tk_update)


if __name__ == "__main__":
    asyncio.run(main())
