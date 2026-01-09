"""Kafka producer utilities for MiscritsScript.

This module mirrors the data structures consumed by the Spring Boot
consumer service (Action and MiscritInfo) and exposes a thin wrapper
around :class:`kafka.KafkaProducer` for publishing events from the
Python automation script.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from kafka import KafkaProducer


@dataclass
class KafkaSettings:
    """Configuration values used to build a Kafka producer."""

    bootstrap_servers: str = "localhost:9092"
    client_id: str = "miscrits-script"
    find_action_topic: str = "find-action"
    miscrit_info_topic: str = "miscrit-info"

    def to_kafka_kwargs(self) -> Dict[str, Any]:
        return {
            "bootstrap_servers": self.bootstrap_servers,
            "client_id": self.client_id,
            "value_serializer": lambda value: json.dumps(value).encode("utf-8"),
            "key_serializer": lambda key: key.encode("utf-8") if key is not None else None,
        }


@dataclass
class Action:
    """Represents an action taken by the automation script."""

    id: int
    is_successful: bool
    description: Optional[str]
    name: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "isSuccessful": self.is_successful,
            "description": self.description,
            "name": self.name,
        }


@dataclass
class MiscritInfo:
    """Information about a Miscrit encounter."""

    miscrit_name: str
    is_high_grade_or_rare: bool
    initial_capture_rate: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "miscritName": self.miscrit_name,
            "highGradeOrRare": self.is_high_grade_or_rare,
            "initialCaptureRate": self.initial_capture_rate,
        }


class MiscritsKafkaProducer:
    """Helper wrapper around :class:`kafka.KafkaProducer`."""

    def __init__(self, settings: Optional[KafkaSettings] = None) -> None:
        self.settings = settings or KafkaSettings()
        self._producer = KafkaProducer(**self.settings.to_kafka_kwargs())

    def send_action(self, action: Action, key: str) -> None:
        """Publish an :class:`Action` to the configured action topic.

        The Spring Boot consumer expects the message key to route to the
        correct handler; use "find" for find events and "capture" for
        capture events.
        """

        self._producer.send(
            topic=self.settings.find_action_topic,
            key=key,
            value=action.to_dict(),
        )

    def send_miscrit_info(self, info: MiscritInfo) -> None:
        """Publish :class:`MiscritInfo` to the Miscrit info topic."""

        self._producer.send(
            topic=self.settings.miscrit_info_topic,
            value=info.to_dict(),
        )

    def flush(self) -> None:
        self._producer.flush()

    def close(self) -> None:
        self._producer.flush()
        self._producer.close()

__all__ = [
    "KafkaSettings",
    "Action",
    "MiscritInfo",
    "MiscritsKafkaProducer",
    "example_publish",
]
