import graphene
import graphql_jwt

import notes.users.schema
from graphene_django.types import DjangoObjectType, ObjectType

from .models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note


class Query(notes.users.schema.Query, ObjectType):
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


class NoteInput(graphene.InputObjectType):
    title = graphene.String()
    content = graphene.String()


class CreateNote(graphene.Mutation):
    class Arguments:
        input = NoteInput(required=True)

    ok = graphene.Boolean()
    note = graphene.Field(NoteType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        note_instance = Note(title=input.title, content=input.content)
        note_instance.save()
        return CreateNote(ok=ok, note=note_instance)


class UpdateNote(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = NoteInput(required=True)

    ok = graphene.Boolean()
    note = graphene.Field(NoteType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        note_instance = Note.objects.get(pk=id)
        if note_instance:
            ok = True
            note_instance.title = input.title
            note_instance.content = input.content
            note_instance.save()
            return UpdateNote(ok=ok, note=note_instance)
        return UpdateNote(ok=ok, note=None)


class DeleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    note = graphene.Field(NoteType)

    @staticmethod
    def mutate(root, info, id):
        ok = False
        note_instance = Note.objects.get(pk=id)
        if note_instance:
            ok = True
            note_instance.delete()
        return DeleteNote(ok=ok)


class Mutation(notes.users.schema.Mutation, graphene.ObjectType,):
    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
