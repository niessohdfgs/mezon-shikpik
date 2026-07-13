from django.http import FileResponse
from django.shortcuts import get_object_or_404

from patterns.models import Pattern
from commerce.services.access import AccessService


def serve_pattern_file(user, pattern_id):

    pattern = get_object_or_404(
        Pattern,
        id=pattern_id,
        is_published=True
    )


    if not AccessService.has_pattern_access(
        user,
        pattern
    ):
        return None


    return FileResponse(
        pattern.file.open("rb"),
        as_attachment=True,
        filename=pattern.file.name.split("/")[-1]
    )