"""
Author: mentix02
Date: 2024-10-09

A crazy command to dump the specified model's serialized (also specified) data to the console.
"""

import json
import typing
import argparse
import importlib

from django.apps import apps
from django.db.models import Model
from django.core.management.base import BaseCommand

from rest_framework.serializers import Serializer


class Command(BaseCommand):

    help = 'Dump the specified model\'s serialized data to the console'

    def _model_validator_type(self, model_path: str) -> type[Model]:
        try:
            model: type[Model] = apps.get_model(model_path)
        except LookupError:
            models: list[Model] = apps.get_models()
            model_paths = ", ".join([f'{model._meta.app_label}.{model.__name__}' for model in models])
            self.stderr.write(f'Available models: {model_paths}')
            self.stderr.write(f'Model "{model_path}" not found')
            exit(1)

        return model

    def _serializer_validator_type(self, serializer_path: str) -> type[Serializer]:
        module_path, class_name = serializer_path.rsplit('.', 1)
        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            self.stderr.write(f'Module "{module_path}" not found')
            exit(1)

        try:
            serializer: type[typing.Any] = getattr(module, class_name)
        except AttributeError:
            self.stderr.write(f'Class "{class_name}" not found in module "{module_path}"')
            exit(1)

        if not issubclass(serializer, Serializer):
            self.stderr.write(f'Class "{class_name}" is not a subclass of Serializer')
            exit(1)

        return serializer

    def get_version(self) -> str:
        return '0a'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            'model',
            type=self._model_validator_type,
            help='Python path to the model to dump (example: user.User)',
        )
        parser.add_argument(
            'serializer',
            type=self._serializer_validator_type,
            help='Python path to the serializer to use (example: user.api.v1.serializers.UserSerializer)',
        )

    def handle(self, *args, **options):
        print(options['model'])
        print(options['serializer'])

        model: type[Model] = options['model']
        serializer: type[Serializer] = options['serializer']

        qs = model.objects.all()
        serialized_data = serializer(qs, many=True).data
        self.stdout.write(json.dumps(serialized_data, indent=2))
