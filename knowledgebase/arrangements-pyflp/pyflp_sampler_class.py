class Sampler(_SamplerInstrument):
    """Represents the native Sampler, either as a clip or a channel.

    ![](https://bit.ly/3DlHPiI)
    """

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]}, sample_path={self.sample_path!r})"

    au_sample_rate = EventProp[int](ChannelID.AUSampleRate)
    """AU-format sample specific."""

    content = NestedProp(Content, ChannelID.SamplerFlags, ChannelID.Parameters)
    """:menuselection:`Sample settings --> Content`"""

    # FL's interface doesn't have an envelope for panning, but still stores
    # the default values in event data.
    @property
    def envelopes(self) -> dict[EnvelopeName, Envelope] | None:
        """An :class:`Envelope` each for Volume, Panning, Mod X, Mod Y and Pitch.

        :menuselection:`Envelope / instruement settings`
        """
        if ChannelID.EnvelopeLFO in self.events.ids:
            envs = [Envelope(e) for e in self.events.separate(ChannelID.EnvelopeLFO)]
            return dict(zip(EnvelopeName.__args__, envs))  # type: ignore

    filter = NestedProp(Filter, ChannelID.Levels)

    fx = NestedProp(
        FX,
        ChannelID.Cutoff,
        ChannelID.FadeIn,
        ChannelID.FadeOut,
        ChannelID.FreqTilt,
        ChannelID.Parameters,
        ChannelID.Pogo,
        ChannelID.Preamp,
        ChannelID.Resonance,
        ChannelID.Reverb,
        ChannelID.RingMod,
        ChannelID.StereoDelay,
        ChannelID.FXFlags,
    )
    """:menuselection:`Sample settings (page) --> Precomputed effects`"""

    @property
    def lfos(self) -> dict[LFOName, SamplerLFO] | None:
        """An :class:`LFO` each for Volume, Panning, Mod X, Mod Y and Pitch.

        :menuselection:`Envelope / instruement settings (page)`
        """
        if ChannelID.EnvelopeLFO in self.events.ids:
            lfos = [SamplerLFO(e) for e in self.events.separate(ChannelID.EnvelopeLFO)]
            return dict(zip(LFOName.__args__, lfos))  # type: ignore

    playback = NestedProp(
        Playback, ChannelID.SamplerFlags, ChannelID.PingPongLoop, ChannelID.Parameters
    )
    """:menuselection:`Sample settings (page) --> Playback`"""

    @property
    def sample_path(self) -> pathlib.Path | None:
        """Absolute path of a sample file on the disk.

        :menuselection:`Sample settings (page) --> File`

        Contains the string ``%FLStudioFactoryData%`` for stock samples.
        """
        if ChannelID.SamplePath in self.events.ids:
            return pathlib.Path(self.events.first(ChannelID.SamplePath).value)

    @sample_path.setter
    def sample_path(self, value: pathlib.Path) -> None:
        if self.sample_path is None:
            raise PropertyCannotBeSet(ChannelID.SamplePath)

        path = "" if str(value) == "." else str(value)
        self.events.first(ChannelID.SamplePath).value = path

    # TODO Find whether ChannelID._StretchTime was really used for attr ``time``.
    stretching = NestedProp(TimeStretching, ChannelID.Parameters)
    """:menuselection:`Sample settings (page) --> Time stretching`"""