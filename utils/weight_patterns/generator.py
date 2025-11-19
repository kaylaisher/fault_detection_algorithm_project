
from .base_patterns import all_zero, all_one
from .one_hot_patterns import one_hot
from .clear_one_patterns import clear_one, explicit_last_zero


class WeightPatternGenerator:
    """
    Modular directed pattern generator for flexible bit_width.
    Each pattern group is isolated into its own module.
    """

    def __init__(self, bit_width, enable_groups=None):
        self.bit_width = bit_width

        # Available groups
        self.available_groups = {
            "all_zero": all_zero,
            "all_one": all_one,
            "one_hot": one_hot,
            "clear_one": clear_one,
            "explicit_last_zero": explicit_last_zero,
        }

        # Default: enable all groups
        self.enabled = enable_groups or list(self.available_groups.keys())

    def enable(self, group):
        if group not in self.available_groups:
            raise ValueError(f"Pattern group '{group}' not found.")
        self.enabled.append(group)

    def disable(self, group):
        if group in self.enabled:
            self.enabled.remove(group)

    def generate(self):
        patterns = []

        for group_name in self.enabled:
            generator_fn = self.available_groups[group_name]
            group_patterns = generator_fn(self.bit_width)
            patterns.extend(group_patterns)

        # Remove duplicates while preserving order
        unique = []
        for p in patterns:
            if p not in unique:
                unique.append(p)

        return unique
