# -*- mode:python; coding:utf-8 -*-

# Copyright (c) 2022 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import List
from ..models import TaskCall, Annotation, RiskAnnotation, VariableAnnotation
from .variable_resolver import VARIABLE_ANNOTATION_TYPE
from .risk_annotator_base import RiskAnnotator, AnnotatorCategory


class AnsibleBuiltinRiskAnnotator(RiskAnnotator):
    name: str = "ansible.builtin"
    enabled: bool = True

    def match(self, taskcall: TaskCall) -> bool:
        resolved_name = taskcall.spec.resolved_name
        return resolved_name.startswith("ansible.builtin.")

    # embed "analyzed_data" field in Task
    def run(self, taskcall: TaskCall) -> List[Annotation]:
        if not self.match(taskcall):
            return taskcall
        resolved_name = taskcall.spec.resolved_name
        options = taskcall.spec.module_options
        var_annos = taskcall.get_annotation_by_type(VARIABLE_ANNOTATION_TYPE)
        var_anno = var_annos[0] if len(var_annos) > 0 else VariableAnnotation()
        resolved_options = var_anno.resolved_module_options
        mutable_vars_per_mo = var_anno.mutable_vars_per_mo
        resolved_variables = var_anno.resolved_variables

        annotations = []
        # builtin modules
        if resolved_name == "ansible.builtin.get_url":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.INBOUND)
            res.data = self.get_url(options, mutable_vars_per_mo)
            for ro in resolved_options:
                res.resolved_data.append(self.get_url(ro, mutable_vars_per_mo))
            annotations.append(res)

        if resolved_name == "ansible.builtin.fetch":
            res = RiskAnnotation(type=self.type)
            res.data = self.fetch(options)
            for ro in resolved_options:
                res.resolved_data.append(self.fetch(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.command":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.CMD_EXEC)
            res.data = self.command(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.command(ro, resolved_variables))
            annotations.append(res)

        if resolved_name == "ansible.builtin.apt":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.PACKAGE_INSTALL)
            res.data = self.apt(options)
            for ro in resolved_options:
                res.resolved_data.append(self.apt(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.add_host":
            res = RiskAnnotation(type=self.type)
            res.data = self.add_host(options)
            for ro in resolved_options:
                res.resolved_data.append(self.add_host(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.apt_key":
            res = RiskAnnotation(type=self.type)
            res.data = self.apt_key(options)
            for ro in resolved_options:
                res.resolved_data.append(self.apt_key(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.apt_repository":
            res = RiskAnnotation(type=self.type)
            res.data = self.apt_repository(options)
            for ro in resolved_options:
                res.resolved_data.append(self.apt_repository(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.assemble":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.assemble(options)
            for ro in resolved_options:
                res.resolved_data.append(self.assemble(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.assert":
            res = RiskAnnotation(type=self.type)
            res.data = self.builtin_assert(options)
            for ro in resolved_options:
                res.resolved_data.append(self.builtin_assert(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.async_status":
            res = RiskAnnotation(type=self.type)
            res.data = self.async_status(options)
            for ro in resolved_options:
                res.resolved_data.append(self.async_status(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.blockinfile":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.blockinfile(options)
            for ro in resolved_options:
                res.resolved_data.append(self.blockinfile(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.copy":
            res = RiskAnnotation(type=self.type)
            res.data = self.copy(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.copy(ro, resolved_variables))
            annotations.append(res)

        if resolved_name == "ansible.builtin.cron":
            res = RiskAnnotation(type=self.type)
            res.data = self.cron(options)
            for ro in resolved_options:
                res.resolved_data.append(self.cron(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.debconf":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.CONFIG_CHANGE)
            res.data = self.debconf(options)
            for ro in resolved_options:
                res.resolved_data.append(self.debconf(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.debug":
            res = RiskAnnotation(type=self.type)
            res.data = self.debug(options)
            for ro in resolved_options:
                res.resolved_data.append(self.debug(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.dnf":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.PACKAGE_INSTALL)
            res.data = self.dnf(options)
            for ro in resolved_options:
                res.resolved_data.append(self.dnf(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.dpkg_selections":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.PACKAGE_INSTALL)
            res.data = self.dpkg_selections(options)
            for ro in resolved_options:
                res.resolved_data.append(self.dpkg_selections(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.expect":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.CMD_EXEC)
            res.data = self.expect(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.expect(ro, resolved_variables))
            annotations.append(res)

        if resolved_name == "ansible.builtin.fail":
            res = RiskAnnotation(type=self.type)
            res.data = self.fail(options)
            for ro in resolved_options:
                res.resolved_data.append(self.fail(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.file":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.file(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.file(ro, resolved_variables))
            annotations.append(res)

        if resolved_name == "ansible.builtin.find":
            res = RiskAnnotation(type=self.type)
            res.data = self.find(options)
            for ro in resolved_options:
                res.resolved_data.append(self.find(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.gather_facts":
            res = RiskAnnotation(type=self.type)
            res.data = self.gather_facts(options)
            for ro in resolved_options:
                res.resolved_data.append(self.gather_facts(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.getent":
            res = RiskAnnotation(type=self.type)
            res.data = self.getent(options)
            res.resolved_data = self.getent(resolved_options)
            annotations.append(res)

        if resolved_name == "ansible.builtin.git":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.INBOUND)
            res.data, res.category = self.git(options, mutable_vars_per_mo)
            for ro in resolved_options:
                rd, c = self.git(ro, mutable_vars_per_mo)
                res.resolved_data.append(rd)
            annotations.append(res)

        if resolved_name == "ansible.builtin.group":
            res = RiskAnnotation(type=self.type)
            res.data = self.group(options)
            for ro in resolved_options:
                res.resolved_data.append(self.group(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.group_by":
            res = RiskAnnotation(type=self.type)
            res.data = self.group_by(options)
            for ro in resolved_options:
                res.resolved_data.append(self.group_by(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.hostname":
            res = RiskAnnotation(type=self.type)
            res.data = self.hostname(options)
            for ro in resolved_options:
                res.resolved_data.append(self.hostname(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.iptables":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.NETWORK_CHANGE)
            res.data = self.iptables(options)
            for ro in resolved_options:
                res.resolved_data.append(self.iptables(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.known_hosts":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.NETWORK_CHANGE)
            res.data = self.known_hosts(options)
            for ro in resolved_options:
                res.resolved_data.append(self.known_hosts(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.lineinfile":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.lineinfile(options)
            for ro in resolved_options:
                res.resolved_data.append(self.lineinfile(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.meta":
            res = RiskAnnotation(type=self.type)
            res.data = self.meta(options)
            for ro in resolved_options:
                res.resolved_data.append(self.meta(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.package":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.PACKAGE_INSTALL)
            res.data = self.package(options)
            for ro in resolved_options:
                res.resolved_data.append(self.package(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.package_facts":
            res = RiskAnnotation(type=self.type)
            res.data = self.package_facts(options)
            for ro in resolved_options:
                res.resolved_data.append(self.package_facts(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.pause":
            res = RiskAnnotation(type=self.type)
            res.data = self.pause(options)
            for ro in resolved_options:
                res.resolved_data.append(self.pause(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.ping":
            res = RiskAnnotation(type=self.type)
            res.data = self.ping(options)
            for ro in resolved_options:
                res.resolved_data.append(self.ping(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.pip":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.PACKAGE_INSTALL)
            res.data = self.pip(options)
            for ro in resolved_options:
                res.resolved_data.append(self.pip(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.raw":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.CMD_EXEC)
            res.data = self.raw(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.raw(ro, resolved_variables))
            annotations.append(res)

        if resolved_name == "ansible.builtin.reboot":
            res = RiskAnnotation(type=self.type)
            res.data = self.reboot(options)
            for ro in resolved_options:
                res.resolved_data.append(self.reboot(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.replace":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.replace(options)
            for ro in resolved_options:
                res.resolved_data.append(self.replace(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.rpm_key":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.rpm_key(options)
            for ro in resolved_options:
                res.resolved_data.append(self.rpm_key(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.script":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.CMD_EXEC)
            res.data = self.script(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.script(ro, resolved_variables))
            annotations.append(res)

        if resolved_name == "ansible.builtin.service":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.SYSTEM_CHANGE)
            res.data = self.service(options)
            for ro in resolved_options:
                res.resolved_data.append(self.service(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.service_facts":
            res = RiskAnnotation(type=self.type)
            res.data = self.service_facts(options)
            for ro in resolved_options:
                res.resolved_data.append(self.service_facts(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.set_fact":
            res = RiskAnnotation(type=self.type)
            res.data = self.set_fact(options)
            for ro in resolved_options:
                res.resolved_data.append(self.set_fact(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.set_stats":
            res = RiskAnnotation(type=self.type)
            res.data = self.set_stats(options)
            for ro in resolved_options:
                res.resolved_data.append(self.set_stats(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.setup":
            res = RiskAnnotation(type=self.type)
            res.data = self.setup(options)
            for ro in resolved_options:
                res.resolved_data.append(self.setup(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.slurp":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.INBOUND)
            res.data = self.slurp(options)
            for ro in resolved_options:
                res.resolved_data.append(self.slurp(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.stat":
            res = RiskAnnotation(type=self.type)
            res.data = self.stat(options)
            for ro in resolved_options:
                res.resolved_data.append(self.stat(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.subversion":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.INBOUND)
            res.data = self.subversion(options)
            for ro in resolved_options:
                res.resolved_data.append(self.subversion(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.sysvinit":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.SYSTEM_CHANGE)
            res.data = self.sysvinit(options)
            for ro in resolved_options:
                res.resolved_data.append(self.sysvinit(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.systemd":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.SYSTEM_CHANGE)
            res.data = self.systemd(options)
            for ro in resolved_options:
                res.resolved_data.append(self.systemd(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.tempfile":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.tempfile(options)
            for ro in resolved_options:
                res.resolved_data.append(self.tempfile(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.template":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.FILE_CHANGE)
            res.data = self.template(options)
            for ro in resolved_options:
                res.resolved_data.append(self.template(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.unarchive":
            res = RiskAnnotation(type=self.type)
            res.data, res.category = self.unarchive(options, resolved_options, mutable_vars_per_mo)
            for ro in resolved_options:
                rores, _ = self.unarchive(ro, resolved_options, mutable_vars_per_mo)
                res.resolved_data.append(rores)
            annotations.append(res)

        if resolved_name == "ansible.builtin.uri":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.INBOUND)
            res.data, res.category = self.uri(options, mutable_vars_per_mo)
            for ro in resolved_options:
                rd, c = self.uri(ro, mutable_vars_per_mo)
                res.resolved_data.append(rd)
            annotations.append(res)

        if resolved_name == "ansible.builtin.user":
            res = RiskAnnotation(type=self.type)
            res.data = self.user(options)
            for ro in resolved_options:
                res.resolved_data.append(self.user(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.validate_argument_spec":
            res = RiskAnnotation(type=self.type)
            res.data = self.validate_argument_spec(options)
            for ro in resolved_options:
                res.resolved_data.append(self.validate_argument_spec(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.wait_for":
            res = RiskAnnotation(type=self.type)
            res.data = self.wait_for(options)
            for ro in resolved_options:
                res.resolved_data.append(self.wait_for(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.wait_for_connection":
            res = RiskAnnotation(type=self.type)
            res.data = self.wait_for_connection(options)
            for ro in resolved_options:
                res.resolved_data.append(self.wait_for_connection(ro))
            res = self.wait_for_connection(taskcall)
            annotations.append(res)

        if resolved_name == "ansible.builtin.yum":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.PACKAGE_INSTALL)
            res.data = self.yum(options)
            for ro in resolved_options:
                res.resolved_data.append(self.yum(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.yum_repository":
            res = RiskAnnotation(type=self.type)
            res.data = self.yum_repository(options)
            for ro in resolved_options:
                res.resolved_data.append(self.yum_repository(ro))
            annotations.append(res)

        if resolved_name == "ansible.builtin.shell":
            res = RiskAnnotation(type=self.type, category=AnnotatorCategory.CMD_EXEC)
            res.data = self.shell(options, resolved_variables)
            for ro in resolved_options:
                res.resolved_data.append(self.shell(ro, resolved_variables))
            annotations.append(res)

        if len(annotations) != 0:
            # root
            res = self.root(taskcall)
            if res.data["root"]:
                annotations.append(res)

        return annotations

    def root(self, taskcall: TaskCall):
        is_root = False
        if "become" in taskcall.spec.options and taskcall.spec.options["become"]:
            is_root = True
        res = RiskAnnotation(
            type=self.type,
            category=AnnotatorCategory.PRIVILEGE_ESCALATION,
            data={"root": is_root},
        )
        return res

    def get_url(self, options, mutable_vars_per_mo):
        data = {}
        mutable_vars_per_type = {}
        # original options
        if type(options) is not dict:
            return data
        if "url" in options:
            data["src"] = options["url"]
            mutable_vars_per_type["src"] = mutable_vars_per_mo.get("url", [])
        if "dest" in options:
            data["dest"] = options["dest"]
            mutable_vars_per_type["dest"] = mutable_vars_per_mo.get("dest", [])
        if "mode" in options:
            # todo: check if octal number
            data["mode"] = options["mode"]
        if "checksum" in options:
            data["checksum"] = options["checksum"]
        if "validate_certs" in options:
            if not options["validate_certs"] or options["validate_certs"] == "no":
                data["validate_certs"] = False
        # injection risk
        if "src" in data and type(data["src"]) is str:
            mutable_vars = mutable_vars_per_type.get("src", [])
            if len(mutable_vars) > 0:
                data = self.embed_mutable_vars(data, mutable_vars, "undetermined_src", "mutable_src_vars")
        if "dest" in data and type(data["dest"]) is str:
            mutable_vars = mutable_vars_per_type.get("dest", [])
            if len(mutable_vars) > 0:
                data = self.embed_mutable_vars(
                    data,
                    mutable_vars,
                    "undetermined_dest",
                    "mutable_dest_vars",
                )
        # unsecure src/dest

        return data

    def fetch(self, options):
        data = {}
        if type(options) is not dict:
            return data
        data["src"] = options["src"]
        data["dest"] = options["dest"]
        return data

    def command(self, options, resolved_variables):
        data = {}
        if type(options) is not dict:
            data["cmd"] = options
        else:
            if "cmd" in options:
                data["cmd"] = options["cmd"]
            if "argv" in options:
                data["cmd"] = options["argv"]
        for rv in resolved_variables:
            if "cmd" in data and type(data["cmd"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["cmd"], rv)
                if undetermined:
                    data["undetermined_cmd"] = True
        return data

    def apt(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "pkg" in options:
            data["pkg"] = options["pkg"]
        if "name" in options:
            data["pkg"] = options["name"]
        if "package" in options:
            data["pkg"] = options["package"]
        if "deb" in options:
            data["pkg"] = options["deb"]
        if "allow_unauthenticated" in options and options["allow_unauthenticated"]:
            data["unauthenticated"] = True
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        return data

    def assemble(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "dest" in options:
            data["file"] = options["dest"]
        if "src" in options:
            data["content"] = options["src"]
        if "mode" in options:
            data["mode"] = options["mode"]
        return data

    def blockinfile(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "path" in options:
            data["file"] = options["path"]
        if "dest" in options:
            data["file"] = options["dest"]
        if "block" in options:
            data["content"] = options["block"]
        if "mode" in options:
            data["mode"] = options["mode"]
        if "unsafe_writes" in options and options["unsafe_writes"]:
            data["unsafe_writes"] = True
        return data

    def copy(self, options, resolved_variables):
        data = {}
        if type(options) is not dict:
            return data
        if "dest" in options:
            data["dest"] = options["dest"]
        if "src" in options:
            data["src"] = options["src"]
        if "content" in options:
            data["src"] = options["content"]
        if "mode" in options:
            data["mode"] = options["mode"]
        for rv in resolved_variables:
            if "dest" in data and type(data["dest"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["dest"], rv)
                if undetermined:
                    data["undetermined_dest"] = True
            if "src" in data and type(data["src"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["src"], rv)
                if undetermined:
                    data["undetermined_src"] = True
        return data

    def git(self, options, mutable_vars_per_mo):
        data = {}
        category = AnnotatorCategory.INBOUND
        mutable_vars_per_type = {}
        if type(options) is not dict:
            return data
        if "repo" in options:
            data["src"] = options["repo"]
            mutable_vars_per_type["src"] = mutable_vars_per_mo.get("repo", [])
        if "dest" in options:
            data["dest"] = options["dest"]
            mutable_vars_per_type["dest"] = mutable_vars_per_mo.get("dest", [])
        if "version" in options:
            data["version"] = options["version"]
        if "clone" in options and (not options["clone"] or options["clone"] == "no"):
            category = AnnotatorCategory.NONE
            return data, category
        if "update" in options and (not options["update"] or options["update"] == "no"):
            category = AnnotatorCategory.NONE
            return data, category
        # injection risk
        if "src" in data and type(data["src"]) is str:
            mutable_vars = mutable_vars_per_type.get("src", [])
            if len(mutable_vars) > 0:
                data = self.embed_mutable_vars(data, mutable_vars, "undetermined_src", "mutable_src_vars")
        if "dest" in data and type(data["dest"]) is str:
            mutable_vars = mutable_vars_per_type.get("dest", [])
            if len(mutable_vars) > 0:
                data = self.embed_mutable_vars(
                    data,
                    mutable_vars,
                    "undetermined_dest",
                    "mutable_dest_vars",
                )
        return data, category

    def iptables(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "chain" in options:
            data["chain"] = options["chain"]
        if "jump" in options:
            data["rule"] = options["jump"]
        if "policy" in options:
            data["rule"] = options["policy"]
        if "protocol" in options:
            data["protocol"] = options["protocol"]
        return data

    def known_hosts(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "path" in options:
            data["file"] = options["path"]
        if "name" in options:
            data["name"] = options["name"]
        if "key" in options:
            data["key"] = options["key"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        return data

    def lineinfile(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "dest" in options:
            data["file"] = options["dest"]
        if "path" in options:
            data["file"] = options["path"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        if "line" in options:
            data["content"] = options["line"]
        if "mode" in options:
            data["mode"] = options["mode"]
        return data

    def package(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["pkg"] = options["name"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        return data

    def pip(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["pkg"] = options["name"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        return data

    def raw(self, options, resolved_variables):
        data = {}
        if type(options) is str:
            data["cmd"] = options
        for rv in resolved_variables:
            if "cmd" in data and type(data["cmd"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["cmd"], rv)
                if undetermined:
                    data["undetermined_cmd"] = True
        return data

    def replace(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "replace" in options:
            data["content"] = options["replace"]  # after
        if "regexp" in options:
            data["regexp"] = options["regexp"]  # before
        if "path" in options:
            data["file"] = options["path"]
        if "dest" in options:
            data["file"] = options["dest"]
        if "mode" in options:
            data["mode"] = options["mode"]
        if "unsafe_writes" in options and options["unsafe_writes"]:
            data["unsafe_writes"] = True
        return data

    def rpm_key(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "key" in options:
            data["file"] = options["key"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        return data

    def script(self, options, resolved_variables):
        data = {}
        if type(options) is not dict:
            data["cmd"] = options
        else:
            if "cmd" in options:
                data["cmd"] = options["cmd"]
        if "cmd" not in data:
            return data
        for rv in resolved_variables:
            if "cmd" in data and type(data["cmd"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["cmd"], rv)
                if undetermined:
                    data["undetermined_cmd"] = True
        return data

    # proxy for multiple more specific service manager modules
    def service(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["name"] = options["name"]
        if "state" in options:
            data["state"] = options["state"]
        if "enabled" in options:
            data["enabled"] = options["enabled"]
            if options["enabled"] == "yes":
                data["enabled"] = True
            if not options["enabled"] == "no":
                data["enabled"] = False
        return data

    def sysvinit(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["name"] = options["name"]
        if "state" in options:
            data["state"] = options["state"]
        if "enabled" in options:
            data["enabled"] = options["enabled"]
            if options["enabled"] == "yes":
                data["enabled"] = True
            if not options["enabled"] == "no":
                data["enabled"] = False
        return data

    def shell(self, options, resolved_variables):
        data = {}
        if type(options) is not dict:
            data["cmd"] = options
        else:
            if "cmd" in options:
                data["cmd"] = options["cmd"]
        for rv in resolved_variables:
            if "cmd" in data and type(data["cmd"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["cmd"], rv)
                if undetermined:
                    data["undetermined_cmd"] = True
        return data

    def slurp(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "src" in options:
            data["src"] = options["src"]
        if "path" in options:
            data["src"] = options["path"]
        return data

    def subversion(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "repo" in options:
            data["src"] = options["repo"]
        if "dest" in options:
            data["dest"] = options["dest"]
        return data

    def systemd(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["name"] = options["name"]
        if "state" in options:
            data["state"] = options["state"]
        if "enabled" in options:
            data["enabled"] = options["enabled"]
            if options["enabled"] == "yes":
                data["enabled"] = True
            if not options["enabled"] == "no":
                data["enabled"] = False
        return data

    def tempfile(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "path" in options:
            data["file"] = options["path"]
        if "prefix" in options:
            data["file"] = options["prefix"]
        if "suffix" in options:
            data["file"] = options["suffix"]
        return data

    def template(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "src" in options:
            data["content"] = options["src"]
        if "dest" in options:
            data["file"] = options["dest"]
        if "mode" in options:
            data["mode"] = options["mode"]
        if "group" in options:
            data["group"] = options["group"]
        if "owner" in options:
            data["owner"] = options["owner"]
        if "unsafe_writes" in options and options["unsafe_writes"]:
            data["unsafe_writes"] = True
        return data

    def uri(self, options, mutable_vars_per_mo):
        category = AnnotatorCategory.NONE
        data = {}
        mutable_vars_per_type = {}
        if type(options) is not dict:
            return data, category
        if "method" in options and (options["method"] == "POST" or options["method"] == "PUT" or options["method"] == "PATCH"):
            category = AnnotatorCategory.OUTBOUND
            if "url" in options:
                data["dest"] = options["url"]
                mutable_vars_per_type["dest"] = mutable_vars_per_mo.get("url", [])
            if "dest" in data and type(data["dest"]) is str:
                mutable_vars = mutable_vars_per_type.get("dest", [])
                if len(mutable_vars) > 0:
                    data = self.embed_mutable_vars(
                        data,
                        mutable_vars,
                        "undetermined_dest",
                        "mutable_dest_vars",
                    )
        elif "method" in options and options["method"] == "GET":
            if "url" in options:
                data["src"] = options["url"]
                mutable_vars_per_type["src"] = mutable_vars_per_mo.get("url", [])
            if "dest" in options:
                data["dest"] = options["dest"]
                mutable_vars_per_type["dest"] = mutable_vars_per_mo.get("dest", [])
            if "validate_certs" in options:
                data["validate_certs"] = options["validate_certs"]
            if "unsafe_writes" in options:
                data["unsafe_writes"] = options["unsafe_writes"]
            # injection risk
            if "src" in data and type(data["src"]) is str:
                mutable_vars = mutable_vars_per_type.get("src", [])
                if len(mutable_vars) > 0:
                    data = self.embed_mutable_vars(
                        data,
                        mutable_vars,
                        "undetermined_src",
                        "mutable_src_vars",
                    )
            if "dest" in data and type(data["dest"]) is str:
                mutable_vars = mutable_vars_per_type.get("dest", [])
                if len(mutable_vars) > 0:
                    data = self.embed_mutable_vars(
                        data,
                        mutable_vars,
                        "undetermined_dest",
                        "mutable_dest_vars",
                    )
        return data, category

    def validate_argument_spec(self, options):
        data = {}
        return data

    def wait_for(self, options):
        data = {}
        return data

    def wait_for_connection(self, options):
        data = {}
        return data

    def yum(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["pkg"] = options["name"]
        if "list" in options:
            data["pkg"] = options["list"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        if "validate_certs" in options:
            data["validate_certs"] = options["validate_certs"]
        return data

    def yum_repository(self, options):
        data = {}
        return data

    def user(self, options):  # config change?
        data = {}
        return data

    def unarchive(self, options, resolved_options, mutable_vars_per_mo):
        category = AnnotatorCategory.NONE
        data = {}
        mutable_vars_per_type = {}
        if type(options) is not dict:
            return data, category
        if "dest" in options:
            data["dest"] = options["dest"]
            mutable_vars_per_type["dest"] = mutable_vars_per_mo.get("dest", [])
        if "src" in options:
            data["src"] = options["src"]
            mutable_vars_per_type["src"] = mutable_vars_per_mo.get("src", [])
        if "remote_src" in options:  # if yes, don't copy
            data["remote_src"] = options["remote_src"]
        if "unsafe_writes" in options:
            data["unsafe_writes"] = options["unsafe_writes"]
        if "validate_certs" in options:
            data["validate_certs"] = options["validate_certs"]

        # set category
        # if remote_src=yes and src contains :// => inbound_transfer
        if "remote_src" in data and (data["remote_src"] == "yes" or data["remote_src"]):
            if "src" in data and type(data["src"]) is str and "://" in data["src"]:
                category = AnnotatorCategory.INBOUND
        # check resolved option
        for ro in resolved_options:
            if "remote_src" in ro and (ro["remote_src"] == "yes" or ro["remote_src"]):
                if "src" in ro and type(ro["src"]) is str and "://" in ro["src"]:
                    category = AnnotatorCategory.INBOUND

        if "src" in data and type(data["src"]) is str:
            mutable_vars = mutable_vars_per_type.get("src", [])
            if len(mutable_vars) > 0:
                data = self.embed_mutable_vars(data, mutable_vars, "undetermined_src", "mutable_src_vars")
        if "dest" in data and type(data["dest"]) is str:
            mutable_vars = mutable_vars_per_type.get("dest", [])
            if len(mutable_vars) > 0:
                data = self.embed_mutable_vars(
                    data,
                    mutable_vars,
                    "undetermined_dest",
                    "mutable_dest_vars",
                )
        return data, category

    def cron(self, options):
        data = {}
        return data

    def debconf(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["pkg"] = options["name"]
        if "question" in options:
            data["config"] = options["question"]
        return data

    def debug(self, options):
        data = {}
        return data

    def expect(self, options, resolved_variables):
        data = {}
        if type(options) is not dict:
            data["cmd"] = options
        else:
            if "command" in options:
                data["cmd"] = options["command"]
        for rv in resolved_variables:
            if "cmd" in data and type(data["cmd"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["cmd"], rv)
                if undetermined:
                    data["undetermined_cmd"] = True
        return data

    def dnf(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["pkg"] = options["name"]
        if "list" in options:
            data["pkg"] = options["list"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        if "validate_certs" in options:
            data["validate_certs"] = options["validate_certs"]
        return data

    def dpkg_selections(self, options):
        data = {}
        if type(options) is not dict:
            return data
        if "name" in options:
            data["pkg"] = options["name"]
        if "selection" in options and options["selection"] == "deinstall":
            data["delete"] = True
        return data

    def fail(self, options):
        data = {}
        return data

    def file(self, options, resolved_variables):
        data = {}
        if type(options) is not dict:
            return data
        if "path" in options:
            data["file"] = options["path"]
        if "src" in options:
            data["file"] = options["src"]
        if "state" in options and options["state"] == "absent":
            data["delete"] = True
        if "mode" in options:
            data["mode"] = options["mode"]
            # if data["mode"] == "":
            #     data[""]
        if "file" not in data:
            return data
        for rv in resolved_variables:
            if "file" in data and type(data["file"]) is str:
                data, undetermined = self.resolved_variable_check(data, data["file"], rv)
                if undetermined:
                    data["undetermined_file"] = True
        return data

    def find(self, options):
        data = {}
        return data

    def add_host(self, options):
        data = {}
        return data

    def apt_key(self, options):
        data = {}
        return data

    def apt_repository(self, options):
        data = {}
        return data

    def builtin_assert(self, options):
        data = {}
        return data

    def async_status(self, options):
        data = {}
        return data

    def gather_facts(self, options):
        data = {}
        return data

    def getent(self, options):
        data = {}
        return data

    def group(self, options):
        data = {}
        return data

    def group_by(self, options):
        data = {}
        return data

    def hostname(self, options):
        data = {}
        return data

    def meta(self, options):
        data = {}
        return data

    def package_facts(self, options):
        data = {}
        return data

    def pause(self, options):
        data = {}
        return data

    def ping(self, options):
        data = {}
        return data

    def reboot(self, options):
        data = {}
        return data

    def service_facts(self, options):
        data = {}
        return data

    def set_fact(self, options):
        data = {}
        return data

    def set_stats(self, options):
        data = {}
        return data

    def setup(self, options):
        data = {}
        return data

    def stat(self, options):
        data = {}
        return data

    def check_nest_variable(self, value, resolved_variables):
        # check nested variables
        variables = []
        for rv in resolved_variables:
            if rv["key"] not in value:
                continue
            if type(rv["value"]) is list:
                for v in rv["value"]:
                    key = "{{ " + rv["key"] + " }}"
                    if type(v) is dict:
                        v = json.dumps(v)
                    if "{{" in v:
                        variables.append(value.replace(key, v))
        return variables

    def resolved_variable_check(self, data, value, rv):
        undetermined = False
        if type(value) is not str:
            return data, undetermined
        if rv["key"] in value and "{{" in value:
            undetermined = True
            if rv["type"] in [
                "inventory_vars",
                "role_defaults",
                "role_vars",
                "special_vars",
            ]:
                data["injection_risk"] = True
                if "injection_risk_variables" in data:
                    data["injection_risk_variables"].append(rv["key"])
                else:
                    data["injection_risk_variables"] = [rv["key"]]
        return data, undetermined

    def embed_mutable_vars(self, data, mutable_vars, key="", vars_key=""):
        if len(mutable_vars) == 0:
            return data
        data["injection_risk"] = True
        injection_risk_vars = [mv for mv in mutable_vars if mv != ""]
        if "injection_risk_variables" not in data:
            data["injection_risk_variables"] = []
        data["injection_risk_variables"].extend(injection_risk_vars)
        if key != "":
            data[key] = True
        if vars_key != "":
            if vars_key not in data:
                data[vars_key] = []
            data[vars_key].extend(injection_risk_vars)
        return data
