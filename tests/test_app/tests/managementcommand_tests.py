from io import StringIO

import minio
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from minio_storage.policy import Policy

from .utils import BaseTestMixin, bucket_name


@override_settings(
    MINIO_STORAGE_MEDIA_USE_PRESIGNED=False, MINIO_STORAGE_STATIC_USE_PRESIGNED=False
)
class CommandsTests(BaseTestMixin, TestCase):
    @override_settings(
        MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET=False,
        MINIO_STORAGE_AUTO_CREATE_MEDIA_POLICY=False,
    )
    def test_management_command(self):

        storage = self.media_storage
        bucket = self.media_storage.bucket_name

        call_command("minio", "check")

        with self.assertRaisesRegex(CommandError, "bucket {} is not empty".format(bucket)):
            call_command("minio", "delete")

        try:
            self.obliterate_bucket(self.media_storage.bucket_name)
        except minio.error.NoSuchBucket:
            pass

        with self.assertRaisesRegex(CommandError, "bucket {} does not exist".format(bucket)):
            call_command("minio", "check")

        with self.assertRaisesRegex(CommandError, "bucket {} does not exist".format(bucket)):
            call_command("minio", "policy")

        with self.assertRaisesRegex(CommandError, "bucket {} does not exist".format(bucket)):
            call_command("minio", "ls")

        with self.assertRaisesRegex(CommandError, "bucket {} does not exist".format(bucket)):
            call_command("minio", "delete")

        call_command("minio", "create")

        call_command("minio", "check")

        with self.assertRaisesRegex(CommandError, "you have already created {}".format(bucket)):
            call_command("minio", "create")

        with self.assertRaisesRegex(CommandError, "bucket {} has no policy".format(bucket)):
            call_command("minio", "policy")

        for p in [p.value for p in Policy]:
            call_command("minio", "policy", "--set", p)

        call_command("minio", "policy", "--set", "GET_ONLY")

        call_command("minio", "policy")

        call_command("minio", "delete")

        with self.assertRaisesRegex(CommandError, "bucket {} does not exist".format(bucket)):
            call_command("minio", "check")

        call_command("minio", "create")

        files = [
            "animals/cats/cat1.txt",
            "animals/cats/cat2.txt",
            "animals/dogs/dog1.txt",
            "animals/dogs/dog2.txt",
            "what.txt",
        ]
        for p in files:
            self.assertEqual(p, storage.save(p, ContentFile(b"abc")))

        def ls_test(expected, *args):
            out = StringIO()
            call_command("minio", "ls", stdout=out, *args)
            out.seek(0)
            lines = out.read().splitlines()
            self.assertEqual(sorted(lines), sorted(expected))

        test_data = (
            (
                ["-r"],
                #
                [
                    "animals/dogs/dog1.txt",
                    "animals/dogs/dog2.txt",
                    "animals/cats/cat1.txt",
                    "animals/cats/cat2.txt",
                    "what.txt",
                ],
            ),
            (
                ["--files"],
                #
                ["what.txt"],
            ),
            (
                ["--dirs"],
                #
                ["animals/"],
            ),
            (
                [],
                #
                ["animals/", "what.txt"],
            ),
            (
                ["--prefix", "animals/"],
                #
                ["animals/dogs/", "animals/cats/"],
            ),
            (
                ["--prefix", "animals/", "--dirs"],
                #
                ["animals/dogs/", "animals/cats/"],
            ),
            (
                ["--prefix", "animals/", "--files"],
                #
                [],
            ),
            (
                ["-r", "-p", "animals/do"],
                #
                ["animals/dogs/dog1.txt", "animals/dogs/dog2.txt"],
            ),
            (
                ["-r", "-p", "animals/do", "--dirs"],
                #
                [],
            ),
        )

        for test in test_data:
            (args, expected) = test
            ls_test(expected=expected, *args)

    def test_check(self):
        out = StringIO()
        call_command("minio", "check", stdout=out)
        self.assertIn("", out.getvalue())

    def test_check_not_exists(self):
        name = bucket_name("new")
        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command("minio", "--bucket", name, "check", stdout=out, stderr=err)
        self.assertEqual("", out.getvalue())
        self.assertEqual("", err.getvalue())

    def test_list_files(self):
        out = StringIO()
        call_command("minio", "ls", stdout=out)
        out.seek(0)
        lines = sorted(out.readlines())
        expected = sorted(["{}\n".format(self.new_file), "{}\n".format(self.second_file)])
        self.assertEqual(lines, expected)

    def test_list_buckets(self):
        out = StringIO()
        call_command("minio", "ls", "--buckets", stdout=out)
        out.seek(0)
        lines = sorted(out.readlines())
        self.assertIn("{}\n".format(self.media_storage.bucket_name), lines)
