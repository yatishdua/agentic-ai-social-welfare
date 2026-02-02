from abc import ABC, abstractmethod


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, text: str) -> dict:
        """
        Must return:
        {
          "fields": {
            field_name: {
              "value": any,
              "confidence": float,
              "source": "REGEX" | "LLM"
            }
          },
          "overall_confidence": float
        }
        """
        pass
