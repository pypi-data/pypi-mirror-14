"""Specific views for baskets

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"

try:
    from cubicweb import _
except ImportError:
    _ = unicode

from logilab.mtconverter import xml_escape

from cubicweb import Unauthorized
from cubicweb.predicates import is_instance, none_rset, non_final_entity
from cubicweb.web import action, component
from cubicweb.web.views import primary, uicfg

# displayed by the basket box
uicfg.primaryview_section.tag_subject_of(('*', 'in_basket', '*'), 'hidden')
uicfg.primaryview_section.tag_object_of(('*', 'in_basket', '*'), 'hidden')


class BasketPrimaryView(primary.PrimaryView):
    __select__ = is_instance('Basket',)
    entity_name = 'Basket'
    nothing_msg = _('nothing in basket')
    content_msg = _('items in this basket')

    def display_title(self, entity):
        self.w(u"<span class='title'><b>%s : %s</b></span>" % (
            self._cw._(self.entity_name), xml_escape(entity.name)))

    def display_content(self, entity):
        rset = self._cw.execute('Any I WHERE I in_basket B,  B eid %(x)s',
                                {'x': entity.eid})
        self.w('<h5>%s</h5>' % self._cw._(self.content_msg))
        if rset:
            self.wview('list', rset)
        else:
            self.w(self._cw._(self.nothing_msg))

    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        self.w(u'&nbsp;')
        self.display_title(entity)
        if entity.description:
            self.w(u'<div class="contentBox">%s</div>' %
                   entity.printable_value('description'))
        self.display_content(entity)

def insert_eids(actions, eids):
    """ insert into the __linkto values of actions all the eids
        this processing also filters out all the actions which don't have a linkto action
    """
    processed_actions = []
    for action_id, action_label, action_dict in actions:
        if isinstance(action_dict, str):
            continue
        if action_dict.get('__linkto', None):
            r_type, old_eids, target = action_dict['__linkto'].split(':')
            action_dict['__linkto'] = '%s:%s:%s' % (r_type,
                                                    '_'.join([str(x) for x in eids]),
                                                    target)
            processed_actions.append((action_id, action_label, action_dict))
    return processed_actions



class BasketBox(component.CtxComponent):
    """display a box containing all user's basketitems"""
    __regid__ = 'basket_box'
    __select__ = component.CtxComponent.__select__ & (
        none_rset() | non_final_entity())
    # XXX disabled by default. One should remove the basket cube if he doesn't
    # want the basket box, or deactivate it explicitly
    visible = False
    order = 30
    title = _('basket')
    rql = 'Any B,N where B is Basket,B owned_by U, U eid %(x)s, B name N'
    etype = 'Basket'
    rtype = 'in_basket'

    def init_rendering(self):
        super(BasketBox, self).init_rendering()
        req = self._cw
        try:
            baskets = req.execute(self.rql, {'x': self._cw.user.eid})
        except Unauthorized:
            # can't access to something in the query, forget this box
            raise component.EmptyComponent()
        rschema = req.vreg.schema.rschema(self.rtype)
        selectedeids = self.selected_eids()
        for basket in baskets.entities():
            rset, inbasketeids = self.build_inbasket_link(basket)
            if selectedeids and rschema.has_perm(req, 'add'):
                addable = [str(eid) for eid in selectedeids if not eid in inbasketeids]
                if addable:
                    self.build_add_link(basket, addable)
            if not rset:
                continue
            if rschema.has_perm(req, 'delete'):
                self.build_delete_link(basket, inbasketeids)
        eschema = req.vreg.schema.eschema(self.etype)
        if eschema.has_perm(req, 'add'):
            url = req.vreg['etypes'].etype_class(self.etype).cw_create_url(req)
            self.append(self.build_link(req._('create basket'), url,
                                        klass='manage'))
        if not self.items:
            raise component.EmptyComponent()

    def render_body(self, w):
        self.render_items(w)

    def selected_eids(self):
        selectedeids = ()
        if self.cw_rset:
            # something is being displayed. If the first column contains eids,
            # fetch them so we can propose to add the selection to the basket
            selectedeids = set(row[0] for row in self.cw_rset.rows)
        return selectedeids

    def build_inbasket_link(self, basket):
        rset = basket.related('in_basket', 'object')
        title = u'%s <span class="basketName">%s</span> (%s)' % (
            _('view basket'), xml_escape(basket.name), len(rset))
        self.append(self.build_link(title, basket.absolute_url(),
                                    escapecontent=False))
        return rset, [row[0] for row in rset]

    def build_add_link(self, basket, addable):
        title = u'%s <span class="basketName">%s</span>' % (
            _('add to basket'), xml_escape(basket.name))
        linkto = u'in_basket:%s:object' % '_'.join(addable)
        msg =  self._cw._('selection added to basket')
        rql = self._cw.form.get('rql', '')
        vid = self._cw.form.get('vid', '')
        url = self._cw.build_url('edit', eid=basket.eid, rql=rql,
                                 __linkto=linkto, __message=msg,
                                 __redirectrql=rql, __redirect_vid=vid)
        self.append(self.build_link(title, url, klass='manage',
                                    escapecontent=False))

    def build_delete_link(self, basket, inbasketeids):
        title = '%s <span class="basketName">%s</span>' % (
            _('reset basket'), xml_escape(basket.name))
        delete = '%s:in_basket:%s' % ('_'.join(str(eid) for eid in inbasketeids),
                                      basket.eid)
        msg =  self._cw._('Basket %s emptied') % basket.name
        rql = self._cw.form.get('rql', '')
        vid = self._cw.form.get('vid', '')
        url = self._cw.build_url('edit', rql=rql, __delete=delete,
                                 __message=msg, __redirectrql=rql,
                                 __redirect_vid=vid)
        self.append(self.build_link(title, url, klass='manage',
                                    escapecontent=False))


class SelectBasketContentAction(action.Action):
    category = 'mainactions'
    __select__ = is_instance('Basket')

    __regid__ = 'select_basket_content'
    title = _('actions_select_basket_content')

    def url(self):
        rql = u'Any X WHERE X in_basket B, B eid %s' % self.cw_rset[self.cw_row or 0][self.cw_col or 0]
        return self._cw.build_url(rql=rql)


