from django.utils.translation import ugettext as _
from django.contrib.admin.utils import quote
from wagtailmodeladmin.helpers import ButtonHelper, PermissionHelper


class TreebeardPermissionHelper(PermissionHelper):
    """
    A custom PermissionHelper class for working with tree-based models that
    extend Treebeard's `MP_Node` model
    """

    def can_delete_object(self, user, obj):
        """Disable deletion of an object/node if it has children"""
        if obj.numchild:
            return False
        return super(TreebeardPermissionHelper, self).can_delete_object(
            user, obj)


class TreebeardButtonHelper(ButtonHelper):
    """
    A custom ButtonHelper class for working with tree-based models that
    extend Treebeard's `MP_Node` model
    """

    def add_sibling_after_button(self, pk, extra_classnames=[]):
        return {
            'url': '%s?sibling_id=%s&pos=right' % (
                self.get_action_url('create'), pk),
            'label': _('Add after'),
            'classname': self.combine_classnames(extra_classnames),
            'title': _('Add a new %s after this one, at the same level') % (
                self.model_name),
        }

    def add_sibling_before_button(self, pk, extra_classnames=[]):
        return {
            'url': '%s?sibling_id=%s&pos=left' % (
                self.get_action_url('create'), pk),
            'label': _('Add before'),
            'classname': self.combine_classnames(extra_classnames),
            'title': _('Add a new %s before this one, at the same level') % (
                self.model_name),
        }

    def add_sibling_button(self, pk, extra_classnames=[]):
        return {
            'url': '%s?sibling_id=%s' % (
                self.get_action_url('create'), pk),
            'label': _('Add sibling'),
            'classname': self.combine_classnames(extra_classnames),
            'title': _('Add a new %s at the same level as this one') % (
                self.model_name),
        }

    def add_child_button(self, pk, extra_classnames=[]):
        return {
            'url': '%s?parent_id=%s' % (
                self.get_action_url('create'), pk),
            'label': _('Add child'),
            'classname': self.combine_classnames(extra_classnames),
            'title': _('Add a new %s as a child, beneath this one') % (
                self.model_name),
        }

    def move_button(self, pk, extra_classnames=[]):
        return {
            'url': self.get_action_url('move', pk),
            'label': _('Move'),
            'classname': self.combine_classnames(extra_classnames),
            'title': _(
                "Move this %s and it's descendants to a different part of "
                "the tree") % self.model_name,
        }

    def get_buttons_for_obj(self, obj, allow_inspect_button=True,
                            extra_classnames=[]):
        """
        Provide different sets of buttons, depending on whether the model
        uses 'node_order_by' to automatically order tree nodes, or the
        positioning is user controlled.
        """
        pk = quote(getattr(obj, self.opts.pk.attname))
        buttons = []
        if self.inspect_view_enabled and allow_inspect_button:
            buttons.append(self.inspect_button(pk, extra_classnames))
        if self.permission_helper.can_edit_object(self.user, obj):
            buttons.append(self.edit_button(pk, extra_classnames))
            buttons.append(self.move_button(pk, extra_classnames))
        if self.permission_helper.has_add_permission(self.user):
            if self.model.node_order_by:
                buttons.append(self.add_child_button(pk, extra_classnames))
                buttons.append(self.add_sibling_button(pk, extra_classnames))
            else:
                buttons.append(self.add_sibling_before_button(pk, extra_classnames))
                buttons.append(self.add_sibling_after_button(pk, extra_classnames))
                buttons.append(self.add_child_button(pk, extra_classnames))
        if self.permission_helper.can_delete_object(self.user, obj):
            buttons.append(self.delete_button(pk, extra_classnames))
        return buttons
