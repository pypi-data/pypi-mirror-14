import re

import django
from django.conf import settings

from .base import BaseNestedAdminTestCase
from .models import TopLevel, LevelOne, LevelTwo, LevelThree


if django.VERSION >= (1, 8):
    get_model_name = lambda m: m._meta.model_name
else:
    get_model_name = lambda m: m._meta.object_name.lower()


def xpath_cls(classname):
    return 'contains(concat(" ", @class, " "), " %s ")' % classname


def xpath_item(model_name):
    xpath_item_predicate = 'not(contains(@class, "-drag")) and not(self::thead)'
    expr = "%s and %s" % (xpath_cls('djn-item'), xpath_item_predicate)
    if model_name:
        expr += ' and contains(@class, "-%s")' % model_name
    return expr


class TestDeepNesting(BaseNestedAdminTestCase):

    root_model = TopLevel
    nested_models = (LevelOne, LevelTwo, LevelThree)

    @classmethod
    def setUpClass(cls):
        super(TestDeepNesting, cls).setUpClass()
        cls.nested_model_names = [get_model_name(model) for model in cls.nested_models]
        cls.inline_type = 'stacked'
        cls.is_grappelli = 'grappelli' in settings.INSTALLED_APPS

    def get_num_inlines(self, indexes=None):
        indexes = list(indexes or [])
        model_name = self.nested_model_names[len(indexes)]
        group = self.get_group(indexes=indexes)
        group_id = group.get_attribute('id')
        selector = "#%s .dynamic-form-%s" % (group_id, model_name)
        return self.selenium.execute_script("return $('%s').length" % selector)

    def get_group(self, indexes=None):
        indexes = list(indexes or [])
        expr_parts = []
        parent_models = self.nested_model_names[:len(indexes)]
        model_name = self.nested_model_names[len(indexes)]
        for parent_model, index in zip(parent_models, indexes):
            expr_parts += ["/*[%s][%d]" % (xpath_item(parent_model), index + 1)]
        expr_parts += ["/*[@data-inline-model='%s']" % model_name]
        expr = "/%s" % ("/".join(expr_parts))
        return self.selenium.find_element_by_xpath(expr)

    def get_item(self, indexes):
        indexes = list(indexes or [])
        index = indexes.pop()
        model_name = self.nested_model_names[len(indexes)]
        if len(indexes):
            group = self.get_group(indexes=indexes)
        else:
            group = self.selenium
        return group.find_element_by_xpath(".//*[%s][%d]" % (xpath_item(model_name), index + 1))

    # def drag_and_drop_item(self, from_section, from_item, to_section, to_item=None, screenshot_hack=False):
    #     action = DragAndDropAction(self, from_section, from_item, to_section, to_item)
    #     action.move_to_target(screenshot_hack=screenshot_hack)

    def add_inline(self, indexes=None, name=None):
        indexes = list(indexes or [])
        new_index = self.get_num_inlines(indexes)
        model_name = self.nested_model_names[len(indexes)]
        add_selector = "#%s .grp-add-item > a.grp-add-handler.%s" % (
            self.get_group(indexes).get_attribute('id'), model_name)
        with self.clickable_selector(add_selector) as el:
            el.click()
        if name is not None:
            indexes.append(new_index)
            self.set_inline_name(name, indexes=indexes)

    def remove_inline(self, indexes):
        model_name = self.nested_model_names[len(indexes)]
        remove_selector = "#%s .grp-remove-handler.%s" % (
            self.get_item(indexes).get_attribute('id'), model_name)
        with self.clickable_selector(remove_selector) as el:
            el.click()

    def delete_inline(self, indexes):
        model_name = self.nested_model_names[len(indexes)]
        delete_selector = "#%s .grp-delete-handler.%s" % (
            self.get_item(indexes).get_attribute('id'), model_name)
        with self.clickable_selector(delete_selector) as el:
            el.click()

    def undelete_inline(self, indexes):
        model_name = self.nested_model_names[len(indexes)]
        undelete_selector = "#%s .grp-delete-handler.%s" % (
            self.get_item(indexes).get_attribute('id'), model_name)
        with self.clickable_selector(undelete_selector) as el:
            el.click()
        delete_selector = "#%s:not(.grp-predelete) .grp-delete-handler.%s" % (
            self.get_item(indexes).get_attribute('id'), model_name)
        self.wait_until_clickable_selector(delete_selector)

    def get_form_field_selector(self, attname, indexes):
        item_id = self.get_item(indexes=indexes).get_attribute('id')
        field_prefix = re.sub(r'(?<=\D)(\d+)$', r'-\1', item_id)
        return "#id_%s-%s" % (field_prefix, attname)

    def set_inline_name(self, name, indexes=None):
        indexes = list(indexes or [])
        name_selector = self.get_form_field_selector("name", indexes=indexes)
        with self.clickable_selector(name_selector) as el:
            el.clear()
            el.send_keys(name)

    def test_add_three_deep(self):
        self.load_change_admin(TopLevel())
        import ipdb; ipdb.set_trace()
