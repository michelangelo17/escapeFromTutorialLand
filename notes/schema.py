import graphene

from graphene_django.types import DjangoObjectType, ObjectType

from .models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class Query(ObjectType):
    all_notes = graphene.List(NoteType)
    note = graphene.Field(NoteType, id=graphene.Int(), title=graphene.String())

    def resolve_all_notes(self, info, **kwargs):
        return Note.objects.all()

    def resolve_note(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Note.objects.get(pk=id)

        if title is not None:
            return Note.objects.get(title=title)

        return None


schema = graphene.Schema(query=Query)
