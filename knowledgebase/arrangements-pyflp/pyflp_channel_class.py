class Channel(EventModel):
    """Represents a channel in the channel rack."""

    def __repr__(self) -> str:
        return f"{type(self).__name__} (name={self.display_name!r}, iid={self.iid})"

    color = EventProp[RGBA](PluginID.Color)
    """Defaults to #5C656A (granite gray).

    ![](https://bit.ly/3SllDsG)

    Values below 20 for any color component (R, G or B) are ignored by FL.
    """

    # TODO controllers = KWProp[List[RemoteController]]()
    internal_name = EventProp[str](PluginID.InternalName)
    """Internal name of the channel.

    The value of this depends on the type of `plugin`:

    * Native (stock) plugin: Empty *afaik*.
    * VST instruments: "Fruity Wrapper".

    See Also:
        :attr:`name`
    """

    enabled = EventProp[bool](ChannelID.IsEnabled)
    """![](https://bit.ly/3sbN8KU)"""

    @property
    def group(self) -> DisplayGroup:  # TODO Setter
        """Display group / filter under which this channel is grouped."""
        return self._kw["group"]

    icon = EventProp[int](PluginID.Icon)
    """Internal ID of the icon shown beside the ``display_name``.

    ![](https://bit.ly/3zjK2sf)
    """

    iid = EventProp[int](ChannelID.New)
    keyboard = NestedProp(Keyboard, ChannelID.FineTune, ChannelID.RootNote, ChannelID.Parameters)
    """Located at the bottom of :menuselection:`Miscellaneous functions (page)`."""

    locked = EventProp[bool](ChannelID.IsLocked)
    """Whether in a locked state or not; mute / solo acts differently when ``True``.

    ![](https://bit.ly/3BOBc7j)
    """

    name = EventProp[str](PluginID.Name, ChannelID._Name)
    """The name associated with a channel.

    It's value depends on the type of plugin:

    * Native (stock): User-given name, None if not given one.
    * VST instrument: The name obtained from the VST or the user-given name.

    See Also:
        :attr:`internal_name` and :attr:`display_name`.
    """

    @property
    def pan(self) -> int | None:
        """Linear. Bipolar.

        | Min | Max   | Default |
        |-----|-------|---------|
        | 0   | 12800 | 6400    |
        """
        if ChannelID.Levels in self.events.ids:
            return cast(LevelsEvent, self.events.first(ChannelID.Levels))["pan"]

        for id in (ChannelID._PanWord, ChannelID._PanByte):
            if id in self.events.ids:
                return self.events.first(id).value

    @pan.setter
    def pan(self, value: int) -> None:
        if self.pan is None:
            raise PropertyCannotBeSet

        if ChannelID.Levels in self.events.ids:
            cast(LevelsEvent, self.events.first(ChannelID.Levels))["pan"] = value
            return

        for id in (ChannelID._PanWord, ChannelID._PanByte):
            if id in self.events.ids:
                self.events.first(id).value = value

    @property
    def volume(self) -> int | None:
        """Nonlinear.

        | Min | Max   | Default |
        |-----|-------|---------|
        | 0   | 12800 | 10000   |
        """
        if ChannelID.Levels in self.events.ids:
            return cast(LevelsEvent, self.events.first(ChannelID.Levels))["volume"]

        for id in (ChannelID._VolWord, ChannelID._VolByte):
            if id in self.events.ids:
                return self.events.first(id).value

    @volume.setter
    def volume(self, value: int) -> None:
        if self.volume is None:
            raise PropertyCannotBeSet

        if ChannelID.Levels in self.events.ids:
            cast(LevelsEvent, self.events.first(ChannelID.Levels))["volume"] = value
            return

        for id in (ChannelID._VolWord, ChannelID._VolByte):
            if id in self.events.ids:
                self.events.first(id).value = value

    # If the channel is not zipped, underlying event is not stored.
    @property
    def zipped(self) -> bool:
        """Whether the channel is zipped / minimized.

        ![](https://bit.ly/3S2imib)
        """
        if ChannelID.Zipped in self.events.ids:
            return self.events.first(ChannelID.Zipped).value
        return False

    @property
    def display_name(self) -> str | None:
        """The name of the channel that will be displayed in FL Studio."""
        return self.name or self.internal_name  # type: ignore