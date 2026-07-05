class FragilityMapper:
    """
    Minimal fragility mapper.

    Responsible for:
    - computing basic fragility indicators
    - attaching fragility metadata to frames
    """

    def map_fragility(self, frame):
        """
        For now, this is a stub that simply marks the frame
        with placeholder fragility values.

        Later this will:
        - compute signal fragility
        - compute measurement fragility
        - compute transition fragility
        - compute scenario fragility
        - integrate gradients and risk surfaces
        """
        return {
            "frame": frame,
            "fragility": {
                "signal": "unknown",
                "measurement": "unknown",
                "transition": "unknown",
                "scenario": "unknown",
            },
        }
