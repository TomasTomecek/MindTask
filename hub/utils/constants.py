"""Project constants and enums"""

from kobo.types import Enum, EnumItem


#########
# ENUMS #
#########

PRIORITY = Enum(
    EnumItem("LOW", help_text="Low Priority"),
    EnumItem("MEDIUM", help_text="Medium Priority"),
    EnumItem("HIGH", help_text="High Priority"),
)

SEVERITY = Enum(
    EnumItem("RFE", help_text="Request for Enhancement"),
    EnumItem("BUGFIX", help_text="BugFix"),
    EnumItem("NORMAL", help_text="Normal"),
)

PROGRESS = Enum(
    EnumItem("START", help_text="Starting"),
    EnumItem("WORKING", help_text="Working"),
    EnumItem("HALF", help_text="Half"),
    EnumItem("NEAR_COMPLETE", help_text="Near complete"),
    EnumItem("COMPLETED", help_text="Completed"),
    EnumItem("PAUSE", help_text="Pause"),
)

TASK_TYPE = Enum(
    EnumItem("WEBUI", help_text="Web"),
    EnumItem("MINDMAP", help_text="MindMap"),
)

ACTIONS = Enum(
    EnumItem("SYNC", help_text="Sync"),
    EnumItem("NEW", help_text="New"),
    EnumItem("DELETE", help_text="Delete"),
    EnumItem("EDIT", help_text="Edit"),
)

##
# MARKERS
##

TASK_MARKERS = ('task-start', 'task-quarter', 'task-half', 'task-3quar',
                'task-done', 'task-pause',)