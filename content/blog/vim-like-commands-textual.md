---
title: "Vim-Like Commands in Textual"
description: "A simple trick to add support for more complex actions to a Textual-based application."
image: "/static/images/vim-keybindings.jpg"
tags: ["textual", "python", "tui"]
publication_date: "2024-09-26"
pubDate: "Thu, 26 Sep 2024 00:00:00 +0000"
---

While I was working on lazyfeed, a news feed reader for the terminal I'm building, I noticed that sometimes the list of articles could get pretty large. To make it easier to navigate, I thought it would be cool to add some keyboard shortcuts to jump to the top or the bottom of the list. Luckily for me, Textual's DataTable widget has built-in actions like action_scroll_bottom and action_scroll_top that just do that.

## Vim key bindings

If you're familiar with Vim, you may know the G and gg commands. If you're in normal mode and press G, you will go straight to the bottom of the buffer, while gg does the opposite and places you at the very beginning.

## Adding the 'G' key binding

Adding a new key binding in Textual is pretty straightforward. For example, to make the G key execute the action_scroll_bottom, all you need to do is add the following lines to your class—in my case, the class I am using to display the list of posts and news.

```python
BINDINGS = [
    #...
    Binding("G", "scroll_bottom", "Jump To Bottom", show=False),
    #...
]
```

Note that I don't need to include the action\_ prefix, as stated here.

And this will do it! Now the problem is the `gg` action.

## Dealing with more complex key bindings

The issue with gg is that it requires two quick key presses. I drew inspiration from game development in PyGame, where cooldowns are often implemented to prevent spamming actions. The idea is to track the time since the last key press and allow the action only if the keys are pressed within a specified timeframe. So, I came up with a function that keeps an eye on key presses. Here’s what it does: It checks if the key pressed is g and stores it in a reactive variable. If g is pressed again while the first g is still saved, it executes action_scroll_top.

![screenshot](/static/images/vim-keybindings.jpg)

Here’s how the function looks:

```python
async def on_key(self, event: events.Key) -> None:
    current_time = time.time()

    if event.key == "g":
        if self.prev_key_pressed == "g" and current_time - self.last_key_press_time <= self.key_press_interval:
            self.action_scroll_top()
            self.prev_key_pressed = None
        else:
            self.prev_key_pressed = "g"

        self.last_key_press_time = current_time
```

You could even use an array to store longer key combinations, which could lead to fun stuff like implementing the Konami code in your app!
