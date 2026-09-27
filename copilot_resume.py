#!/usr/bin/env python3
"""
https://claude.ai/chat/366913d8-1a07-4898-8f8e-a7a4e32f3c5b

copilot_resume - list recent Copilot CLI sessions for the current directory
and let the user pick one to resume with arrow keys.

Controls:
  Up/Down  - move selection
  Enter    - resume the currently highlighted session (defaults to the first)
  Esc / q  - cancel without resuming
"""

import curses
import os
import sqlite3
import subprocess
import sys


DB_PATH = os.path.join(os.path.expanduser("~"), ".copilot", "session-store.db")


def fetch_sessions(cwd: str):
    """Return a list of (id, updated_at, summary) tuples for this cwd."""
    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, substr(updated_at, 1, 16), summary
            FROM sessions
            WHERE cwd = ?
            ORDER BY updated_at DESC
            LIMIT 20;
            """,
            (cwd,),
        )
        return cur.fetchall()
    finally:
        conn.close()


def pick_session(stdscr, sessions):
    """Curses UI: arrow-key select, Enter confirms, Esc/q cancels.

    Returns the selected index, or None if cancelled.
    """
    curses.curs_set(0)
    stdscr.keypad(True)

    # Respect the terminal's own colors/theme instead of forcing curses'
    # default black-on-white (or black-on-black) palette.
    curses.start_color()
    curses.use_default_colors()
    stdscr.bkgd(" ", curses.color_pair(0))

    selected = 0
    n = len(sessions)

    while True:
        stdscr.erase()
        stdscr.addstr(0, 0, "Select session to resume (Enter to confirm, Esc to cancel):")
        stdscr.addstr(1, 0, "")

        for i, (sid, updated, summary) in enumerate(sessions):
            line = f"{i + 1:2d}) [{updated}] {summary}"
            y = i + 2
            try:
                if i == selected:
                    stdscr.addstr(y, 0, line, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 0, line)
            except curses.error:
                # Terminal too small for the full line/height; ignore overflow.
                pass

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % n
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % n
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return selected
        elif key in (27, ord("q")):  # Esc or q
            return None


def main():
    cwd = os.getcwd()
    print(f"Sessions for {cwd}:")

    sessions = fetch_sessions(cwd)
    if not sessions:
        print("No sessions found.")
        return

    choice = curses.wrapper(pick_session, sessions)

    if choice is None:
        print("Cancelled.")
        return

    selected_id = sessions[choice][0]
    subprocess.run(["copilot", f"--resume={selected_id}"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
