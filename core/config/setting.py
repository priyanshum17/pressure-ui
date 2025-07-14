import json
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError


class Settings(BaseModel):
    DATA_DIRECTORY: str = Field()
    ALTERNATIVE_LIMIT: int = Field()

    @classmethod
    def from_json_file(cls, json_path: Path) -> "Settings":
        """
        Load settings from a JSON file path.

        Args:
            json_path (Path): Path to the JSON config file.

        Returns:
            Settings: An instance of Settings with validated data.
        """
        if not json_path.is_file():
            raise FileNotFoundError(f"Config file not found: {json_path}")

        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(**data)


settings = Settings.from_json_file(Path("settings.json"))
