from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScriptConfig:
    """Configuration values for the Miscrits automation script."""

    target_miscrit: str = "papa"
    location_to_find: tuple[int, int] = (653, 239)
    battle_ability_name: str = "bastion"
    ready_to_train_text: str = "ready to train"
    evolution_image_name: str = "evolution.png"
    close_image_name: str = "close.png"
    safe_ability_location: tuple[int, int] = (550, 735)
    enable_bonus: bool = False
    level_up_count: int = 3
