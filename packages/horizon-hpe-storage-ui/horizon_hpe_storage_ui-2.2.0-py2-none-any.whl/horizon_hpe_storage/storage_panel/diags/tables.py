# (c) Copyright [2015] Hewlett Packard Enterprise Development LP
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from django.core.urlresolvers import NoReverseMatch  # noqa
from django.core.urlresolvers import reverse
from django.utils import html
from django.utils.translation import ugettext_lazy as _
from django.utils import safestring

from horizon import forms
from horizon import tables

import horizon_hpe_storage.api.keystone_api as keystone
import horizon_hpe_storage.api.barbican_api as barbican


class RunTimeColumn(tables.Column):
    # Customized column class.
    def get_raw_data(self, node):
        if 'diag_run_time' in node:
            return node['diag_run_time']
        else:
            return "-- Not Yet Run --"


class SSHTestResultsColumn(tables.Column):
    # Customized column class.
    def get_raw_data(self, node):
        if 'validation_time' in node:
            results = node['validation_time']
            if results == 'Failed':
                results = '<font color="red">Failed</font>'
            else:
                results = '<font color="green">Passed</font>'
            return safestring.mark_safe(results)
        else:
            return "-- Not Yet Run --"


class DiagConfigTestResultsColumn(tables.Column):
   # Customized column class.
   def get_raw_data(self, node):
       if 'diag_run_time' in node:
           if node['validation_time'] == 'Failed':
               return "N/A"
           elif 'diag_test_status' in node and 'software_test_status' in node:
               if ":fail:" in node['diag_test_status'] or \
                       ":fail" in node['software_test_status']:
                   result_str = '<font color="red">Failed </font>'
               else:
                   result_str = '<font color="green">Passed </font>'

               node_name = node['node_name'] + "::" + \
                           node['node_type']
               url = reverse("horizon:admin:hpe_storage:diags:" + \
                             "test_detail",
                             args=(node_name,)) + \
                             "test_details"
               # link = '<a href="%s">%s</a>' % (url, run_time)
               link = '%s <a href="%s">(details)</a>' % (result_str, url)
               return safestring.mark_safe(link)

       return "N/A"


class DiagSoftwareTestResultsColumn(tables.Column):
    # Customized column class.
    def get_raw_data(self, node):
       if 'diag_run_time' in node:
           if node['validation_time'] == 'Failed':
               return "N/A"
           else:
               if ":fail:" in node['software_test_status']:
                   result_str = '<font color="red">Failed </font>'
               else:
                   result_str = '<font color="green">Passed </font>'

               node_name = node['node_name'] + "::" + \
                           node['node_type']
               url = reverse("horizon:admin:hpe_storage:diags:" + \
                             "software_test_detail",
                             args=(node_name,)) + \
                             "software_test_details"
               # link = '<a href="%s">%s</a>' % (url, run_time)
               link = '%s <a href="%s">(details)</a>' % (result_str, url)
               return safestring.mark_safe(link)
       else:
           return "N/A"


def get_backend_name(node_name, backend_name):
    try:
        full_name = node_name + "::" + backend_name
        url = reverse("horizon:admin:hpe_storage:diags:" + \
                      "backend_detail", args=(full_name,)) + \
                      "backend_details"
        backend_name = "[" + backend_name + "]"
        backend = '<a href="%s">%s</a>' % (url, html.escape(backend_name))
    except NoReverseMatch:
        backend = html.escape(backend_name)
    return backend

class DiagBackendsColumn(tables.Column):
    # Customized column class.
    def get_raw_data(self, node):
        if 'diag_run_time' in node and \
                        node['validation_time'] != 'Failed' and \
                        'diag_test_status' in node:
            node_name = node['node_name']
            link = _('%(backend_name)s')
            backends = []
            items = node['diag_test_status'].split("::")
            for item in items:
                if item.startswith('Backend Section'):
                    fields = item.split(":")
                    backend_name = get_backend_name(node_name, fields[1])
                    vals = {"backend_name": backend_name}
                    backends.append(link % vals)

            return safestring.mark_safe("<br>".join(backends))
        else:
            return "N/A"


class RunAllCinderDiagsAction(tables.LinkAction):
    name = "test_cinder"
    verbose_name = _("Run Diagnostics Test on All Cinder Nodes")
    url = "horizon:admin:hpe_storage:diags:test_all_cinder_nodes"
    classes = ("ajax-modal",)
    keystone_api = keystone.KeystoneAPI()
    barbican_api = barbican.BarbicanAPI()

    def allowed(self, request, node=None):
        self.keystone_api.do_setup(request)
        self.barbican_api.do_setup(self.keystone_api.get_session())
        return self.barbican_api.nodes_exist(
            self.barbican_api.CINDER_NODE_TYPE)


class RunCinderDiagsAction(tables.LinkAction):
    name = "test_all_cinder"
    verbose_name = _("Run Diagnostics Test")
    url = "horizon:admin:hpe_storage:diags:test_cinder_node"
    classes = ("ajax-modal",)


class DumpCinderStatsAction(tables.LinkAction):
    name = "dump_stats"
    verbose_name = _("View Diagnostic Test and Discovery Results")
    url = "horizon:admin:hpe_storage:diags:dump_cinder_node"
    classes = ("ajax-modal",)

    def allowed(self, request, node=None):
        if 'diag_test_status' in node:
            # means we have run diag test
            return True

        return False


class CinderNodeTable(tables.DataTable):
    node_name = tables.Column(
        'node_name',
        verbose_name=_('Node Name'),
        form_field=forms.CharField(max_length=64))
    node_ip = tables.Column(
        'node_ip',
        verbose_name=_('IP Address'),
        form_field=forms.CharField(max_length=64))
    last_run = RunTimeColumn(
        'run_time',
        verbose_name=_('Last Run'))
    ssh_results = SSHTestResultsColumn(
        'ssh_results',
        verbose_name=_('SSH Connection Test'))
    cinder_results = DiagConfigTestResultsColumn(
        'cinder_results',
        verbose_name=_('Diagnostic Test'))
    # software_results = DiagSoftwareTestResultsColumn(
    #     'software_results',
    #     verbose_name=_('Software Test'))
    # backends = DiagBackendsColumn(
    #     'backends',
    #     verbose_name=_('Driver Configurations'))

    def get_object_id(self, node):
        return node['node_name']

    class Meta(object):
        name = "diag_cinder_nodes"
        verbose_name = _("Cinder Nodes")
        hidden_title = False
        table_actions = (RunAllCinderDiagsAction,)
        # row_actions = (RunCinderDiagsAction, DumpCinderStatsAction)
        row_actions = (RunCinderDiagsAction, )


class RunAllNovaDiagsAction(tables.LinkAction):
    name = "test_nova"
    verbose_name = _("Run Diagnostics Test on All Nova Nodes")
    url = "horizon:admin:hpe_storage:diags:test_all_nova_nodes"
    classes = ("ajax-modal",)
    keystone_api = keystone.KeystoneAPI()
    barbican_api = barbican.BarbicanAPI()

    def allowed(self, request, node=None):
        self.keystone_api.do_setup(request)
        self.barbican_api.do_setup(self.keystone_api.get_session())
        return self.barbican_api.nodes_exist(
            self.barbican_api.NOVA_NODE_TYPE)


class RunNovaDiagsAction(tables.LinkAction):
    name = "test_all_nova"
    verbose_name = _("Run Diagnostics Test")
    url = "horizon:admin:hpe_storage:diags:test_nova_node"
    classes = ("ajax-modal",)

    def get_link_url(self, node):
        return reverse(self.url, args=[node['node_name']])


class NovaNodeTable(tables.DataTable):
    node_name = tables.Column(
        'node_name',
        verbose_name=_('Node Name'),
        form_field=forms.CharField(max_length=64))
    node_ip = tables.Column(
        'node_ip',
        verbose_name=_('IP Address'),
        form_field=forms.CharField(max_length=64))
    last_run = RunTimeColumn(
        'run_time',
        verbose_name=_('Last Run'))
    ssh_results = SSHTestResultsColumn(
        'ssh_results',
        verbose_name=_('SSH Connection Test'))
    software_results = DiagSoftwareTestResultsColumn(
        'run_time',
        verbose_name=_('Diagnostic Test'))

    def get_object_id(self, node):
        return node['node_name']

    class Meta(object):
        name = "diag_nova_nodes"
        verbose_name = _("Nova Nodes")
        hidden_title = False
        table_actions = (RunAllNovaDiagsAction,)
        row_actions = (RunNovaDiagsAction,)
