from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from config import ScriptConfig


def _tuple_to_string(value: tuple[int, int]) -> str:
    return f"{value[0]}, {value[1]}"


def _parse_location(value: str, field_name: str) -> tuple[int, int]:
    try:
        parts = [int(part.strip()) for part in value.split(",")]
    except ValueError as exc:
        raise ValueError(f"{field_name} must be two integers separated by a comma.") from exc
    if len(parts) != 2:
        raise ValueError(f"{field_name} must be two integers separated by a comma.")
    return parts[0], parts[1]

def _quote_env_value(value: str) -> str:
    if value == "":
        return value
    if any(char in value for char in (" ", "#", "\"", "\n")):
        escaped = value.replace("\\", "\\\\").replace("\"", "\\\"")
        return f"\"{escaped}\""
    return value


def _write_env_file(env_path: Path, values: dict[str, str]) -> None:
    existing_lines: list[str] = []
    if env_path.exists():
        existing_lines = env_path.read_text().splitlines()

    filtered_lines: list[str] = []
    for line in existing_lines:
        stripped = line.strip()
        if "=" in stripped and not stripped.startswith("#"):
            key = stripped.split("=", 1)[0]
            if key in values:
                continue
        filtered_lines.append(line)

    for key, value in values.items():
        if value != "":
            filtered_lines.append(f"{key}={_quote_env_value(value)}")

    env_path.write_text("\n".join(filtered_lines) + ("\n" if filtered_lines else ""))


class ConfigForm:
    def __init__(self, defaults: ScriptConfig) -> None:
        self.defaults = defaults
        self.config: ScriptConfig | None = None

        self.root = tk.Tk()
        self.root.title("Miscrits Script Configuration")

        self._build_form()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_form(self) -> None:
        padding = {"padx": 10, "pady": 6}

        tk.Label(self.root, text="Target Miscrit").grid(row=0, column=0, sticky="w", **padding)
        self.target_miscrit_entry = tk.Entry(self.root, width=30)
        self.target_miscrit_entry.insert(0, self.defaults.target_miscrit)
        self.target_miscrit_entry.grid(row=0, column=1, **padding)

        tk.Label(self.root, text="Alert Email Username").grid(
            row=1, column=0, sticky="w", **padding
        )
        self.mail_username_entry = tk.Entry(self.root, width=30)
        self.mail_username_entry.insert(0, os.getenv("SPRING_MAIL_USERNAME", ""))
        self.mail_username_entry.grid(row=1, column=1, **padding)

        tk.Label(self.root, text="Alert Email Password").grid(
            row=2, column=0, sticky="w", **padding
        )
        self.mail_password_entry = tk.Entry(self.root, width=30, show="*")
        self.mail_password_entry.insert(0, os.getenv("SPRING_MAIL_PASSWORD", ""))
        self.mail_password_entry.grid(row=2, column=1, **padding)

        tk.Label(self.root, text="Location To Find (x, y)").grid(
            row=3,
            column=0,
            sticky="w",
            **padding,
        )
        self.location_to_find_entry = tk.Entry(self.root, width=30)
        self.location_to_find_entry.insert(0, _tuple_to_string(self.defaults.location_to_find))
        self.location_to_find_entry.grid(row=3, column=1, **padding)

        tk.Label(self.root, text="Battle Ability Name").grid(
            row=4,
            column=0,
            sticky="w",
            **padding,
        )
        self.battle_ability_entry = tk.Entry(self.root, width=30)
        self.battle_ability_entry.insert(0, self.defaults.battle_ability_name)
        self.battle_ability_entry.grid(row=4, column=1, **padding)

        tk.Label(self.root, text="Safe Ability Location (x, y)").grid(
            row=5,
            column=0,
            sticky="w",
            **padding,
        )
        self.safe_ability_entry = tk.Entry(self.root, width=30)
        self.safe_ability_entry.insert(0, _tuple_to_string(self.defaults.safe_ability_location))
        self.safe_ability_entry.grid(row=5, column=1, **padding)

        tk.Label(self.root, text="Enable Bonus").grid(row=6, column=0, sticky="w", **padding)
        self.enable_bonus_var = tk.BooleanVar(value=self.defaults.enable_bonus)
        tk.Checkbutton(self.root, variable=self.enable_bonus_var).grid(
            row=6,
            column=1,
            sticky="w",
            **padding,
        )

        tk.Label(self.root, text="Level Up Count (0-3)").grid(
            row=7,
            column=0,
            sticky="w",
            **padding,
        )
        self.level_up_entry = tk.Spinbox(self.root, from_=0, to=3, width=5)
        self.level_up_entry.delete(0, tk.END)
        self.level_up_entry.insert(0, str(self.defaults.level_up_count))
        self.level_up_entry.grid(row=7, column=1, sticky="w", **padding)

        start_button = tk.Button(self.root, text="Start Script", command=self._on_submit)
        start_button.grid(row=8, column=0, columnspan=2, pady=12)

    def _on_submit(self) -> None:
        try:
            level_up_count = int(self.level_up_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Level up count must be an integer.")
            return

        if not 0 <= level_up_count <= 3:
            messagebox.showerror("Invalid input", "Level up count must be between 0 and 3.")
            return

        try:
            location_to_find = _parse_location(
                self.location_to_find_entry.get(),
                "Location to find",
            )
            safe_ability_location = _parse_location(
                self.safe_ability_entry.get(),
                "Safe ability location",
            )
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return

        target_miscrit = self.target_miscrit_entry.get().strip()
        battle_ability_name = self.battle_ability_entry.get().strip()
        mail_username = self.mail_username_entry.get().strip()
        mail_password = self.mail_password_entry.get().strip()

        if not target_miscrit:
            messagebox.showerror("Invalid input", "Target miscrit cannot be empty.")
            return
        if not battle_ability_name:
            messagebox.showerror("Invalid input", "Battle ability name cannot be empty.")
            return

        self.config = ScriptConfig(
            target_miscrit=target_miscrit,
            location_to_find=location_to_find,
            battle_ability_name=battle_ability_name,
            safe_ability_location=safe_ability_location,
            enable_bonus=self.enable_bonus_var.get(),
            level_up_count=level_up_count,
        )
        os.environ["MISCRITS_TARGET_MISCRIT"] = target_miscrit
        os.environ["SPRING_MAIL_USERNAME"] = mail_username
        os.environ["SPRING_MAIL_PASSWORD"] = mail_password

        env_path = Path(__file__).resolve().parents[1] / ".env"
        _write_env_file(
            env_path,
            {
                "MISCRITS_TARGET_MISCRIT": target_miscrit,
                "SPRING_MAIL_USERNAME": mail_username,
                "SPRING_MAIL_PASSWORD": mail_password,
            },
        )
        self.root.destroy()

    def _on_close(self) -> None:
        self.root.destroy()

    def run(self) -> ScriptConfig:
        self.root.mainloop()
        if self.config is None:
            raise SystemExit("Configuration cancelled.")
        return self.config


def prompt_for_config(defaults: ScriptConfig) -> ScriptConfig:
    form = ConfigForm(defaults)
    return form.run()
