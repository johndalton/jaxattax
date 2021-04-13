import copy
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import router
from django.db.migrations import RunPython
from django.db.models import TextField
from django.db.models.functions import Cast
from wagtail.core.blocks import StreamValue
from wagtail.core.fields import StreamField


class StreamFieldDataMigration(RunPython):
    atomic = True

    def __init__(
        self, model_name, name, forwards_code, backwards_code=None,
        *,
        atomic=False, elidable=False
    ):
        self.model_name = model_name
        self.name = name
        self.atomic = atomic

        # Forwards code
        if not callable(forwards_code):
            raise ValueError("StreamFieldDataMigration must be supplied with a callable")
        self.forwards_code = forwards_code

        # Reverse code
        if backwards_code is None:
            self.backwards_code = None
        else:
            if not callable(backwards_code):
                raise ValueError("StreamFieldDataMigration must be supplied with callable arguments")
            self.backwards_code = backwards_code
        self.elidable = elidable

    def deconstruct(self):
        kwargs = {
            'model_name': self.model_name,
            'name': self.name,
            'forwards_code': self.forwards_code,
            'atomic': self.atomic,
        }
        if self.backwards_code is not None:
            kwargs['backwards_code'] = self.backwards_code
        if self.atomic is not None:
            kwargs['atomic'] = self.atomic
        if self.hints:
            kwargs['hints'] = self.hints
        return (self.__class__.__qualname__, [], kwargs)

    @property
    def reversible(self):
        return self.backwards_code is not None

    def migrate_field(self, app_label, apps, code):
        model = apps.get_model(app_label, self.model_name)
        field: StreamField = model._meta.get_field(self.name)

        text_name = field.attname + '__text'
        annotation = {text_name: Cast(field.column, TextField())}
        for instance in model.objects.annotate(**annotation).all():
            in_data = json.loads(getattr(instance, text_name))
            out_data = code(instance, copy.deepcopy(in_data))
            if in_data != out_data:
                out_str = json.dumps(out_data, cls=DjangoJSONEncoder)
                # Bypass any validation by saving the encoded JSON. The
                # migrated JSONish data might not be valid stream field data
                # for this field at this point in the field migration.
                setattr(instance, field.attname, StreamValue(
                    field.stream_block, [], raw_text=out_str
                ))
                instance.save(update_fields=[field.name])

    def database_forwards(
        self, app_label, schema_editor, from_state, to_state,
    ):
        # RunPython has access to all models. Ensure that all models are
        # reloaded in case any are delayed.
        from_state.clear_delayed_apps_cache()
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            self.migrate_field(app_label, from_state.apps, self.forwards_code)

    def database_backwards(
        self, app_label, schema_editor, from_state, to_state,
    ):
        if self.backwards_code is None:
            raise NotImplementedError("You cannot reverse this operation")
        if router.allow_migrate(schema_editor.connection.alias, app_label):
            self.migrate_field(app_label, from_state.apps, self.backwards_code)
