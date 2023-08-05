# -*- coding: utf-8 -*-

"""The **action** layer (also called "service" layer) stands between the
    model layer and the view layer.  It is the heart of an application and
    contains its business rules.  MVC/MVT is insufficient for large apps.
    """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from nine import IS_PYTHON2, nimport, nine, range, str, basestring
import deform as d
from .events import ProfileUpdatedEvent
from .exceptions import FormValidationFailure


def validate_form(controls, form):
    try:
        captured = form.validate(controls)
    except d.ValidationFailure as e:
        # NOTE(jkoelker) normally this is superfluous, but if the app is
        #                debug logging, then log that we "ate" the exception
        LOG.debug('Form validation failed', exc_info=True)
        raise FormValidationFailure(form, e)
    return captured


def edit_user(user, form, adict):
    try:
        captured = validate_form(adict, form)
    except FormValidationFailure as e:
        if hasattr(user, 'username'):
            # We pre-populate username
            return e.result(self.request, username=user.username)
        else:
            return e.result(self.request)

    changed = False
    email = captured.get('email', None)
    if email:
        email_user = self.User.get_by_email(self.request, email)
        if email_user and email_user.id != user.id:
            FlashMessage(self.request,
                         _('That e-mail is already used.'),
                         kind='error')
            return HTTPFound(location=self.request.url)
        if email != user.email:
            user.email = email
            changed = True

    password = captured.get('password')
    if password:
        user.password = password
        changed = True

    if changed:
        FlashMessage(self.request, self.Str.edit_profile_done,
                     kind='success')
        self.request.registry.notify(
            ProfileUpdatedEvent(self.request, user, captured)
        )

