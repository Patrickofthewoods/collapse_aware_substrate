class CoordinationManager:
    """
    Minimal coordination manager.

    Responsible for:
    - ordering operations
    - managing frame lifecycle
    - ensuring collapse-aware transitions
    """

    def coordinate(self, frame):
        """
        For now, this is a stub that simply wraps the frame
        with coordination metadata.

        Later this will:
        - enforce timing windows
        - manage dependency ordering
        - apply coordination guards
        - handle multi-primitive interactions
        """
        return {
            "frame": frame,
            "coordination": {
                "status": "coordinated",
            },
        }
