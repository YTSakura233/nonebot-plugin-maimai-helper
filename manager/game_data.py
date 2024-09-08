import json
import os

from src.plugins.maimai_new.data import root_path


class GameDataManager:
    def __init__(self, resource_type: str):
        resource = self._load_resource_info(os.path.join(root_path, "game_data", f"{resource_type}_list.json"))
        self.resource = resource["data"]
        self.resource_info = resource["info"]

    # 加载资源信息的封装函数
    def _load_resource_info(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    # 改进后的 get_resource 和 have_resource 函数
    def get_resource(self, resource_id: int):
        return self.resource.get(str(resource_id), None)

    def have_resource(self, resource_id: int):
        return str(resource_id) in self.resource
