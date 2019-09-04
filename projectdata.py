from targettype import TargetType


class ProjectData:

    def __init__(self, target_name, full_path, target_type):
        assert isinstance(target_name, str)
        assert isinstance(full_path, str)
        assert isinstance(target_type, TargetType)

        self.target_name = target_name
        self.directory = None
        self.full_path = full_path
        self.target_type = target_type
