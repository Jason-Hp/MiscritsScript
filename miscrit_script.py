from __future__ import annotations

import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pyautogui
import pytesseract
from rapidfuzz import fuzz

from coordinates import Coordinates
from kafka_producer import Action, MiscritInfo, MiscritsKafkaProducer, example_publish
from location import Location


@dataclass(frozen=True)
class ScriptConfig:
    """Configuration values for the Miscrits automation script."""

    target_miscrit: str = "papa"
    location_to_find: tuple[int, int] = (653, 239)
    battle_ability_name: str = "bastion"
    ready_to_train_text: str = "ready to train"
    evolution_image_name: str = "evolution.png"
    close_image_name: str = "close.png"


@dataclass(frozen=True)
class CapturePolicy:
    """Strategy for determining capture and grade decisions."""

    high_grade_threshold: int = 31
    capture_threshold: int = 65

    def is_high_grade_or_rare(self, capture_rate: int) -> bool:
        if capture_rate <= 0:
            return False
        return capture_rate <= self.high_grade_threshold

    def should_capture(self, capture_rate: int) -> bool:
        if capture_rate == 0:
            return True
        return capture_rate >= self.capture_threshold


class CountStore:
    """Persistence helper for the encounter counter."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> int:
        if not self.path.exists():
            return 0
        try:
            return int(self.path.read_text().strip())
        except ValueError:
            return 0

    def write(self, value: int) -> None:
        self.path.write_text(str(value))


class MiscritsAutomation:
    """Main automation workflow for Miscrits."""

    def __init__(
        self,
        config: ScriptConfig,
        producer: MiscritsKafkaProducer,
        count_store: CountStore,
        capture_policy: CapturePolicy,
    ) -> None:
        self.config = config
        self.producer = producer
        self.count_store = count_store
        self.capture_policy = capture_policy
        self.base_dir = Path(__file__).resolve().parent

    def click(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(0.03)
        pyautogui.mouseUp()

    def click_point(self, point: tuple[int, int]) -> None:
        x, y = point
        self.click(x, y)

    def get_text(self, region: tuple[int, int, int, int]) -> str:
        screenshot = pyautogui.screenshot(region=region)
        return pytesseract.image_to_string(screenshot, config="--psm 6").strip().lower()

    def parse_percentage(self) -> int:
        screenshot = pyautogui.screenshot(region=Coordinates.CAPTURE_RATE.value)
        raw_percentage = pytesseract.image_to_string(screenshot, config="--psm 7").strip()
        match = re.search(r"(\d+)", raw_percentage)
        if not match:
            return -1
        return int(match.group(1))

    def matches_text(self, region: tuple[int, int, int, int], expected: str) -> bool:
        obtained = self.get_text(region)

        if expected == self.config.target_miscrit:
            print(f"miscrit: {obtained}")
            print(f"fuzz: {fuzz.ratio(obtained, expected)}")
            if obtained == "":
                capture_rate = self.parse_percentage()
                return 0 < capture_rate < 5

        return fuzz.ratio(obtained, expected) > 70

    def do_battle(self) -> None:
        self.click_point(Location.ABILITY_TO_USE_LOCATION.value)
        time.sleep(8)

    def check_all_level_up_ready(self, level_checker: Iterable[tuple[int, int, int, int]]) -> bool:
        for location in level_checker:
            if not self.matches_text(location, self.config.ready_to_train_text):
                return False
        return True

    def perform_level_up(self) -> None:
        self.click_point(Location.TRAIN_LOCATION.value)
        time.sleep(2)

        for miscrit_location in (
            Location.FIRST_MISCRIT_TO_TRAIN.value,
            Location.SECOND_MISCRIT_TO_TRAIN.value,
            Location.THIRD_MISCRIT_TO_TRAIN.value,
        ):
            self.click_point(miscrit_location)
            time.sleep(1)

            self.click_point(Location.TRAIN_NOW_BUTTON_LOCATION.value)
            time.sleep(2)

            self.click_point(Location.BONUS_LOCATION.value)
            self.click_point(Location.BONUS_LOCATION.value)
            time.sleep(3)
            self.click_point(Location.BONUS_LOCATION.value)
            time.sleep(5)

            self.click_point(Location.NEW_SKILL_CONTINUE.value)
            time.sleep(4)

            evolution_path = self.base_dir / self.config.evolution_image_name
            if evolution_path.exists():
                evolution = pyautogui.locateOnScreen(
                    str(evolution_path),
                    confidence=0.7,
                    grayscale=True,
                )
                if evolution:
                    print("close evolution")
                    self.click_point(Location.EVOLUTION_CLOSE.value)
                    time.sleep(2)
                else:
                    print("no evolution")

        self.click_point(Location.EXIT_TRAIN.value)
        time.sleep(3)

    def report_find_action(self, count: int) -> None:
        action = Action(
            id=count,
            is_successful=True,
            description="Successfully found and is battling a miscrit",
            name="find",
        )
        self.producer.send_action(action, key="find")

    def report_capture(self, count: int, miscrit_name: str) -> None:
        action = Action(
            id=count,
            is_successful=True,
            description=miscrit_name,
            name="capture",
        )
        self.producer.send_action(action, key="capture")

    def report_miscrit_info(self) -> None:
        capture_rate = self.parse_percentage()
        info = MiscritInfo(
            miscrit_name=self.get_text(Coordinates.MISCRIT_NAME_LOCATION.value),
            is_high_grade_or_rare=self.capture_policy.is_high_grade_or_rare(capture_rate),
            initial_capture_rate=capture_rate,
        )
        self.producer.send_miscrit_info(info)

    def close_overlays(self) -> None:
        close_path = self.base_dir / self.config.close_image_name
        if not close_path.exists():
            return

        while True:
            close_location = pyautogui.locateOnScreen(
                str(close_path),
                confidence=0.75,
                grayscale=True,
            )
            if close_location:
                print("need closing")
                pyautogui.click(close_location)
                time.sleep(3)
            else:
                break

    def run(self) -> None:
        count = self.count_store.read()
        time.sleep(5)

        while True:
            count += 1
            print(count)
            self.count_store.write(count)

            self.click_point(self.config.location_to_find)
            time.sleep(7)

            if not self.matches_text(
                Coordinates.BATTLE_ABILITY_LOCATION.value,
                self.config.battle_ability_name,
            ):
                time.sleep(20)
                continue

            self.report_find_action(count)
            produced_miscrit_info_message = False
            to_catch = False

            while self.matches_text(
                Coordinates.BATTLE_ABILITY_LOCATION.value,
                self.config.battle_ability_name,
            ):
                if not produced_miscrit_info_message:
                    self.report_miscrit_info()
                    produced_miscrit_info_message = True

                if self.matches_text(
                    Coordinates.MISCRIT_NAME_LOCATION.value,
                    self.config.target_miscrit,
                ):
                    print("FOUND!")
                    time.sleep(2)
                    while True:
                        self.click_point(Location.SAFE_ABILITY_LOCATION.value)
                        time.sleep(10)

                capture_rate = self.parse_percentage()
                if to_catch or self.capture_policy.is_high_grade_or_rare(capture_rate):
                    to_catch = True
                    if self.capture_policy.should_capture(capture_rate):
                        miscrit_name = self.get_text(Coordinates.MISCRIT_NAME_LOCATION.value)
                        self.report_capture(count, miscrit_name)
                        self.click_point(Location.CAPTURE_LOCATION.value)
                        time.sleep(10)
                        self.click_point(Location.ACCEPT_CAPTURE.value)

                self.do_battle()

            time.sleep(5)
            all_ready = self.check_all_level_up_ready(
                (
                    Coordinates.LEVEL_UP_BOTTOM_RIGHT.value,
                    Coordinates.LEVEL_UP_BOTTOM_LEFT.value,
                    Coordinates.LEVEL_UP_TOP_RIGHT.value,
                )
            )
            self.click_point(Location.CONTINUE_AFTER_BATTLE.value)
            time.sleep(5)

            if all_ready:
                self.perform_level_up()

            self.close_overlays()


def publish_kafka_examples() -> None:
    """Publish example Kafka events for quick integration testing."""

    example_publish()


def main() -> None:
    config = ScriptConfig()
    producer = MiscritsKafkaProducer()
    count_store = CountStore(Path(__file__).with_name("count.txt"))
    automation = MiscritsAutomation(
        config=config,
        producer=producer,
        count_store=count_store,
        capture_policy=CapturePolicy(),
    )

    try:
        automation.run()
    finally:
        producer.close()


if __name__ == "__main__":
    main()
