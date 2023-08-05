# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.

# 部分代码参考与复制自 python-goose: https://github.com/grangier/python-goose
from collections import Counter
import re

from lxml import etree
import six

from gelid.extractors import html
from gelid.extractors.enums import ItemProp, Pack


class HtmlTree(object):
    def __init__(self, source, url=None):
        self.url = url
        self.stores = {Pack.html: etree.HTML(source, base_url=url)}

    @property
    def html(self):
        return self.stores.get(Pack.html)

    @property
    def author(self):
        """
        从itemprop获取作者名
        :return:
        """
        nodes = HtmlTree.item_prop(self.html, ItemProp.author.name)
        for node in nodes:
            name_nodes = HtmlTree.item_prop(node, ItemProp.name.name)
            if len(name_nodes) > 0:
                names = HtmlTree.texts(name_nodes[0])
                return u''.join([name.strip() for name in names if isinstance(name, six.string_types)])

    @staticmethod
    def item_prop(node, name):
        """
        从itemprop结构获取节点
        :param node:
        :param name:
        :return:
        """
        return HtmlTree.elements(node, attr=ItemProp.itemprop.name, value=name)

    @staticmethod
    def elements(node, tag=None, attr=None, value=None, child=False):
        """
        使用tag的attr属性值value获取节点
        :param node:原始节点数据
        :param tag:
        :param attr:
        :param value:
        :param child:
        :return:
        """
        ns = "http://exslt.org/regular-expressions"
        selector = 'descendant-or-self::%s' % (tag or '*')
        if attr and value:
            selector = '%s[re:test(@%s, "%s", "i")]' % (selector, attr, value)
        elems = node.xpath(selector, namespaces={"re": ns})
        if node in elems and (tag or child):
            elems.remove(node)
        return elems

    @staticmethod
    def texts(node):
        """
        获取节点内容
        :param node:
        :return:
        """
        return [i for i in node.itertext()]

    @staticmethod
    def content_c(source, template):
        tree1 = etree.HTML(HtmlTree._clear(source))
        tree2 = etree.HTML(HtmlTree._clear(template))
        e1, e2 = HtmlTree.check_element(tree1, tree2)
        return e1

    @staticmethod
    def conntent_html(source, template):
        e1 = HtmlTree.content_c(source, template)
        return etree.tounicode(e1, method="html")

    @staticmethod
    def _clear(source):
        source = html.set_html_clean(source)
        source = re.sub('<br\s*/?>', '', source)
        source = re.sub('<(option|a|span|select|iframe|noscript|script|style)[^>]*?>[\w\W]*?</\\1>', '', source)
        source = re.sub('<([^>]+?) [^>]+?>\s*</\\1>', '', source)
        return source

    @staticmethod
    def check_element(e1, e2):
        """
        比较两个lxml元素，直到分析至不同结构时返回
        :param e1:
        :param e2:
        :return:
        """

        l1 = len(e1)
        l2 = len(e2)
        if l1 and l1 != l2:
            return e1, e2  # e1.getparent()
        for i in range(0, l1):
            result = HtmlTree.check_element(e1[i], e2[i])
            if result is not None:
                return result

    @staticmethod
    def max_pattern(sources):
        pages1 = []
        pages2 = []
        for i, source in enumerate(sources):
            if i % 2 == 0:
                pages1.append(source)
            else:
                pages2.append(source)
        patterns = []
        pages1 = pages1[:len(pages2)]
        for i in range(len(pages1)):
            try:
                e = HtmlTree.content_c(pages1[i], pages2[i])
                p1 = '//{0}[@id="{1}"]'
                p2 = '//{0}[@class="{1}"]'
                p3 = '//{0}[@id="{1}"][@class="{2}"]'
                tag = e.tag
                id = e.attrib.get('id')
                cls = e.attrib.get('class')
                if id and cls:
                    p = p3.format(tag, id, cls)
                elif id:
                    p = p1.format(tag, id)
                elif cls:
                    p = p2.format(tag, cls)
                else:
                    p = ''
                patterns.append(p)
            except:
                pass
        c = Counter(patterns)
        ps = c.most_common(1)
        return ps[0][0]
