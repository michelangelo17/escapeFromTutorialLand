import graphene

from graphene_django.types import DjangoObjectType, ObjectType

from .models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class Query(ObjectType):
    all_notes = graphene.List(NoteType)

    def resolve_all_notes(self, info, **kwargs):
        return Note.objects.all()


schema = graphene.Schema(query=Query)
