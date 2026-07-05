# Minimal ascent primitives for the collapse-aware substrate.
# All primitives follow the same interface:
#   - apply(frame) → frame

class ContextFrame:
    def apply(self, frame):
        return frame


class LocalCohere:
    def apply(self, frame):
        return frame


class RelativeDistinguish:
    def apply(self, frame):
        return frame


class BoundedIdentity:
    def apply(self, frame):
        return frame


class BoundedAggregation:
    def apply(self, frame):
        return frame


class CollapseAwareTransition:
    def apply(self, frame):
        return frame


class RiskSurfaceMap:
    def apply(self, frame):
        return frame


class ProvisionalAssign:
    def apply(self, frame):
        return frame


class RegimeValidate:
    def apply(self, frame):
        return frame


class ValidOp:
    def apply(self, frame):
        return frame
