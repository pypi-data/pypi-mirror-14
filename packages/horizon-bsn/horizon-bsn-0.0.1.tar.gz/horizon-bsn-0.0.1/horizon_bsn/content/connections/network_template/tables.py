# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.utils.translation import ugettext_lazy as _
from horizon import messages
from horizon import tables
from horizon_bsn.api import neutron

import logging

LOG = logging.getLogger(__name__)


class DeleteTemplateAction(tables.DeleteAction):
    data_type_singular = _("Network Template")
    data_type_plural = _("Network Templates")

    def delete(self, request, obj_id):
        try:
            neutron.networktemplate_delete(request, obj_id)
        except Exception as e:
            LOG.info(str(e))
            messages.error(
                request, _("Unable to delete template. Template may "
                           "be in use by a tenant."))


class CreateTemplateAction(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Network Template")
    url = "horizon:admin:connections:network_template_admin:create"
    classes = ("ajax-modal", "btn-create")


class RemoveTemplateAction(tables.LinkAction):
    name = "remove"
    url = "horizon:project:connections:network_template:remove"
    classes = ("ajax-modal", "btn-danger")
    verbose_name = _("Remove Network Template Instance")

    def allowed(self, request, datum):
        try:
            assign = neutron\
                .networktemplateassignment_get(request,
                                               request.user.tenant_id)
            if assign:
                return True
        except Exception:
            return False


class ApplyTemplateAction(tables.LinkAction):
    name = "apply"
    verbose_name = _("Apply Network Template")
    url = "horizon:project:connections:network_template:select"
    classes = ("ajax-modal", "btn-create")

    def allowed(self, request, datum):
        try:
            assign = neutron\
                .networktemplateassignment_get(request,
                                               request.user.tenant_id)
            if assign:
                return False
        except Exception:
            return True


class NetworkTemplateTable(tables.DataTable):
    template_name = tables.Column("template_name",
                                  verbose_name=_("Template Name"))
    heat_stack_name = tables.Column("heat_stack_name",
                                    verbose_name=_("Heat Stack Name"))
    description = tables.Column("description", verbose_name=_("Description"))
    status = tables.Column("status", verbose_name=_("Status"))
    resources = tables.Column("resources", verbose_name=_("Resources"))

    def get_object_id(self, stack):
        return None

    class Meta(object):
        multi_select = False
        name = "networktemplate"
        verbose_name = _("Network Template")
        table_actions = (ApplyTemplateAction, RemoveTemplateAction)
        # row_actions = tuple()


class NetworkTemplateAdminTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("Template ID"), hidden=True)
    name = tables.Column(
        "name", verbose_name=_("Name"),
        link="horizon:admin:connections:network_template_admin:detail")

    class Meta(object):
        name = "networktemplate_admin"
        verbose_name = _("Network Template Administration")
        table_actions = (CreateTemplateAction, DeleteTemplateAction)
        row_actions = (DeleteTemplateAction,)
