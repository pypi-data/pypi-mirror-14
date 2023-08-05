# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2016 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys

from django.utils.translation import ugettext as _, ungettext
from django.utils.encoding import force_text
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST
from django.http import Http404

from weblate.trans.site import get_site_url
from weblate.trans.exporters import get_exporter
from weblate.trans.util import report_error
from weblate.trans.forms import get_upload_form
from weblate.trans.views.helper import get_translation, import_message
from weblate.trans.permissions import (
    can_author_translation, can_overwrite_translation
)


def download_translation_format(request, project, subproject, lang, fmt):
    obj = get_translation(request, project, subproject, lang)

    try:
        exporter = get_exporter(fmt)(
            obj.subproject.project,
            obj.language,
            get_site_url(obj.get_absolute_url())
        )
    except KeyError:
        raise Http404('File format not supported')

    for unit in obj.unit_set.iterator():
        exporter.add_unit(unit)

    # Save to response
    return exporter.get_response(
        '{{project}}-{0}-{{language}}.{{extension}}'.format(
            subproject
        )
    )


def download_translation(request, project, subproject, lang):
    obj = get_translation(request, project, subproject, lang)

    srcfilename = obj.get_filename()

    # Construct file name (do not use real filename as it is usually not
    # that useful)
    filename = '%s-%s-%s.%s' % (project, subproject, lang, obj.store.extension)

    # Create response
    with open(srcfilename) as handle:
        response = HttpResponse(
            handle.read(),
            content_type=obj.store.mimetype
        )

    # Fill in response headers
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def download_language_pack(request, project, subproject, lang):
    obj = get_translation(request, project, subproject, lang)
    if not obj.supports_language_pack():
        raise Http404('Language pack download not supported')

    filename, mime = obj.store.get_language_pack_meta()

    # Create response
    response = HttpResponse(
        obj.store.get_language_pack(),
        content_type=mime
    )

    # Fill in response headers
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@require_POST
@permission_required('trans.upload_translation')
def upload_translation(request, project, subproject, lang):
    '''
    Handling of translation uploads.
    '''
    obj = get_translation(request, project, subproject, lang)

    # Check method and lock
    if obj.is_locked(request.user):
        messages.error(request, _('Access denied.'))
        return redirect(obj)

    # Get correct form handler based on permissions
    form = get_upload_form(request.user, obj.subproject.project)(
        request.POST, request.FILES
    )

    # Check form validity
    if not form.is_valid():
        messages.error(request, _('Please fix errors in the form.'))
        return redirect(obj)

    # Create author name
    author = None
    if (can_author_translation(request.user, obj.subproject.project) and
            form.cleaned_data['author_name'] != '' and
            form.cleaned_data['author_email'] != ''):
        author = '%s <%s>' % (
            form.cleaned_data['author_name'],
            form.cleaned_data['author_email']
        )

    # Check for overwriting
    overwrite = False
    if can_overwrite_translation(request.user, obj.subproject.project):
        overwrite = form.cleaned_data['overwrite']

    # Do actual import
    try:
        ret, count = obj.merge_upload(
            request,
            request.FILES['file'],
            overwrite,
            author,
            merge_header=form.cleaned_data['merge_header'],
            merge_comments=form.cleaned_data['merge_comments'],
            method=form.cleaned_data['method'],
            fuzzy=form.cleaned_data['fuzzy'],
        )
        import_message(
            request, count,
            _('No strings were imported from the uploaded file.'),
            ungettext(
                'Processed %d string from the uploaded files.',
                'Processed %d strings from the uploaded files.',
                count
            )
        )
        if not ret:
            messages.warning(
                request,
                _('There were no new strings in uploaded file!')
            )
    except Exception as error:
        messages.error(
            request, _('File content merge failed: %s') % force_text(error)
        )
        report_error(error, sys.exc_info(), request)

    return redirect(obj)
