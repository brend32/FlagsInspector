init -505 python:
    def flags_inspector_activate():
        global Flags, SceneFlags, flags_log_text, flags_log

        Flags = FlagVaultModed()
        SceneFlags = FlagVaultModed()

        if renpy.get_screen("flags_inspector") is None:
            renpy.show_screen("flags_inspector")
        renpy.restart_interaction()

        flags_log_text = ""
        flags_log = []  
        

    def flags_inspector_deactivate():
        global Flags, SceneFlags

        if (renpy.get_screen("flags_inspector") is None) == False:
            renpy.hide_screen("flags_inspector")
        renpy.restart_interaction()

        Flags = FlagVault()
        SceneFlags = FlagVault()

    flags_log_text = ""
    flags_inspector_tool = ModTool(flags_inspector_activate, flags_inspector_deactivate, "flags_inspector", "Flags inspector", "_BrenD_", "1.0", "mod/flags_inspector/icon.png", "https://www.youtube.com/channel/UCATCV8pfte6-lyUy0sjGXUQ")
    Mod.tools.register(flags_inspector_tool)

init -505 screen flags_inspector:
    zorder 2000

    if flags_inspector_tool.activated:
        text "Flags inspector:\n[flags_log_text]":
            xpos 1920 - 20
            text_align 1
            xanchor 1.0
            xsize 300
            ypos 100
            line_spacing -15
            color "ffffff"
            font "font/russia.ttf"
            size 50

define flags_log = []     
init python:
    class FlagsLogEntry:

        def __init__(self, event, value, color):
            self.event = event
            self.value = value
            self.color = color
            self.cl = 0

        def __str__(self):
            return '{color=%s}%s: %s{/color}' %(self.color, self.event, self.value)

        def _value(self):
            return self.value

        def __nonzero__(self):
            import sys, traceback
            import inspect
            all_stack_frames = inspect.stack()
            caller_stack_frame = all_stack_frames[1]
            caller_name = caller_stack_frame[3]

            if caller_name != "get_sensitive":
                add_flags_log_entry(self.event, self.color, self.value)
            
            return self.value

    def add_flags_log_entry(event, flag, value = True):
        global flags_log_text

        red = "#d14444"
        orange = "#e8ae31"
        green = "#65dd47"

        if event == "Raise":
            color = orange
        elif value == True and event != "Drop":
            color = green
        else:
            color = red

        flags_log.insert(0, str(FlagsLogEntry(event, flag, color)))
        if len(flags_log) > 10:
            flags_log.remove(flags_log[len(flags_log) - 1])
        
        flags_log_text = "\n".join(flags_log)
        if renpy.get_screen("flags_inspector") is None:
            renpy.show_screen("flags_inspector")
        renpy.restart_interaction()


    class FlagVaultModed:
        def __init__(self):
            self.vault = set()
        
        def Raise(self, flag):
            add_flags_log_entry("Raise", flag)
            self.vault.add(flag)
        
        def Drop(self, flag):
            add_flags_log_entry("Drop", flag)
            self.vault.discard(flag)
        
        def Has(self, flag):
            add_flags_log_entry("Has", flag, flag in self.vault)
            return FlagsLogEntry("Has check", flag in self.vault, flag)
        
        def Seen(self, flag):
            ret = self.Has(flag)
            add_flags_log_entry("Seen", flag, ret._value())
            self.Raise(flag)
            return ret
        
        def Reset(self):
            flags_log = []
            self.vault.clear()