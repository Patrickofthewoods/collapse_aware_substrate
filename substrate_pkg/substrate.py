from .collapse_primitives import (
    NoSame, NoDiff, NoRel, NoBound, NoGrad, NoMag,
    NoDist, NoOnt, NoBe, NoState, NoPred, NoMod
)

from .ascent_primitives import (
    ContextFrame,
    LocalCohere,
    RelativeDistinguish,
    BoundedIdentity,
    BoundedAggregation,
    CollapseAwareTransition,
    RiskSurfaceMap,
    ProvisionalAssign,
    RegimeValidate,
    ValidOp,
)

from .telemetry import TelemetryIngestor
from .coordination import CoordinationManager
from .fragility import FragilityMapper
from .cascade import CascadeEngine
from .scenario_engine import ScenarioEngine
from .assembly_engine import AssemblyEngine


class Substrate:
    def __init__(self):
        # Collapse layer
        self.collapse_primitives = [
            NoSame(), NoDiff(), NoRel(), NoBound(), NoGrad(), NoMag(),
            NoDist(), NoOnt(), NoBe(), NoState(), NoPred(), NoMod(),
        ]

        # Ascent layer
        self.ascent_primitives = [
            ContextFrame(),
            LocalCohere(),
            RelativeDistinguish(),
            BoundedIdentity(),
            BoundedAggregation(),
            CollapseAwareTransition(),
            RiskSurfaceMap(),
            ProvisionalAssign(),
            RegimeValidate(),
            ValidOp(),
        ]

        # Telemetry layer
        self.telemetry = TelemetryIngestor()

        # Coordination layer
        self.coordination = CoordinationManager()

        # Fragility layer
        self.fragility = FragilityMapper()

        # Cascade layer
        self.cascade = CascadeEngine()

        # Scenario layer
        self.scenario_engine = ScenarioEngine()

        # Assembly layer
        self.assembly_engine = AssemblyEngine()


    # ------------------------------------------------------------
    # PIPELINE STAGES
    # ------------------------------------------------------------

    def apply_collapse(self, payload):
        for primitive in self.collapse_primitives:
            if primitive.check(payload):
                payload = primitive.apply(payload)
        return payload

    def apply_ascent(self, frame):
        for primitive in self.ascent_primitives:
            frame = primitive.apply(frame)
        return frame

    def apply_coordination(self, frame):
        return self.coordination.coordinate(frame)

    def apply_fragility(self, frame):
        return self.fragility.map_fragility(frame)

    def apply_cascade(self, frame):
        return self.cascade.apply_cascade(frame)

    def apply_scenario(self, frame):
        return self.scenario_engine.assemble(frame)

    def apply_assembly(self, frame):
        return self.assembly_engine.assemble(frame)


    # ------------------------------------------------------------
    # SINGLE INGEST
    # ------------------------------------------------------------

    def ingest(self, records):
        """
        Full pipeline:
        telemetry → collapse → ascent → coordination → fragility → cascade → scenario → assembly
        """
        payload = self.telemetry.ingest(records)
        payload = self.apply_collapse(payload)
        frame = self.apply_ascent(payload)
        frame = self.apply_coordination(frame)
        frame = self.apply_fragility(frame)
        frame = self.apply_cascade(frame)
        frame = self.apply_scenario(frame)
        frame = self.apply_assembly(frame)
        return frame


    # ------------------------------------------------------------
    # BATCH INGEST
    # ------------------------------------------------------------

    def ingest_batch(self, batch_records):
        """
        Batch ingest:
        - batch_records is a list of raw telemetry inputs
        - each element is passed through the full substrate pipeline
        - results are combined into a multi-profile assembly
        """
        frames = []

        for records in batch_records:
            frame = self.ingest(records)
            frames.append(frame)

        return self.assembly_engine.assemble_many(frames)


    # ------------------------------------------------------------
    # PUBLIC ENTRYPOINT
    # ------------------------------------------------------------

    def run(self, records):
        """
        Public substrate entrypoint.
        Runs the full collapse-aware pipeline on a single telemetry input.
        """
        return self.ingest(records)
