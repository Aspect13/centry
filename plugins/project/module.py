#!/usr/bin/python3
# coding=utf-8

#   Copyright 2021 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Module """

import flask  # pylint: disable=E0401
import jinja2  # pylint: disable=E0401

from flask import request, render_template

from .init_db import init_db

from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import module  # pylint: disable=E0611,E0401
from plugins.base.utils.api_utils import add_resource_to_api

mock_config = {
    "username": "User",
    "default_chapter": "Manage Project",
    "projects": [
        {"name": "Project1", "id": "1", "selected": True},
        {"name": "Project2", "id": "2"},
        {"name": "Project3", "id": "3"}
    ],
    "project_structure": {
        "chapters": [
            {
                "title": "Manage Project", "link": "?chapter=Manage%20Project",
                "nav": [
                    {"title": "Users", "link": "#", "active": True},
                    {"title": "Quotas", "link": "#"},
                    {"title": "Integrations", "link": "#"},
                    {"title": "Plugins", "link": "#"}
                ]
            },
            {
                "title": "Dashboards", "link": "?chapter=Dashboards",
                "nav": [
                    {"title": "Dashboards", "link": "#"},
                    {"title": "Data Explorer", "link": "#"},
                    {"title": "Group Projects", "link": "#", "active": True},
                ]
            },
            {
                "title": "Security", "link": "?chapter=Security",
                "nav": [
                    {"title": "Overview", "link": "#", "active": True},
                    {"title": "Planner", "link": "#"},
                    {"title": "Results", "link": "#"},
                    {"title": "Thresholds", "link": "#"}
                ]
            },
            {
                "title": "Performance", "link": "?chapter=Performance",
                "nav": [
                    {"title": "Overview", "link": "#", "active": True},
                    {"title": "Planner", "link": "#"},
                    {"title": "Results", "link": "#"},
                    {"title": "Thresholds", "link": "#"}
                ]
            }
        ]
    }
}


class Module(module.ModuleModel):
    """ Galloper module """

    def __init__(self, settings, root_path, context):
        self.settings = settings
        self.root_path = root_path
        self.context = context

    def init(self):
        """ Init module """
        log.info("Initializing module Projects")
        init_db()
        from .api.project import ProjectAPI, ProjectSessionAPI
        from .api.statistics import StatisticAPI
        from .api.quota import QuotaAPI
        add_resource_to_api(self.context.api, ProjectAPI, "/project", "/project/<int:project_id>")
        add_resource_to_api(self.context.api, ProjectSessionAPI, "/project-session",
                            "/project-session/<int:project_id>")
        add_resource_to_api(self.context.api, StatisticAPI, "/statistic/<int:project_id>")
        add_resource_to_api(self.context.api, QuotaAPI, "/quota/<int:project_id>")

        from plugins.project.rpc_worker import (
            prj_or_404, list_projects, get_project_statistics, get_storage_quota,
            unsecret_key, get_hidden, set_hidden, set_secrets, check_quota
        )
        self.context.rpc_manager.register_function(prj_or_404, name='project_get_or_404')
        self.context.rpc_manager.register_function(list_projects, name='project_list')
        self.context.rpc_manager.register_function(get_project_statistics, name='project_statistics')
        self.context.rpc_manager.register_function(get_storage_quota, name='project_get_storage_space_quota')
        self.context.rpc_manager.register_function(unsecret_key, name='project_unsecret')
        self.context.rpc_manager.register_function(get_hidden, name='project_get_hidden_secrets')
        self.context.rpc_manager.register_function(set_hidden, name='project_set_hidden_secrets')
        self.context.rpc_manager.register_function(set_secrets, name='project_set_secrets')
        self.context.rpc_manager.register_function(check_quota, name='project_check_quota')



    def deinit(self):  # pylint: disable=R0201
        """ De-init module """
        log.info("De-initializing module")
    #

