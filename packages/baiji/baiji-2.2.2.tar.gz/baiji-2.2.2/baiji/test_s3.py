# FIXME pylint: disable=protected-access, unnecessary-lambda, unused-variable
import os
import shutil
import unittest
import uuid
import mock
from baiji import s3
from baiji.util.testing import create_random_temporary_file
from baiji.util import tempfile

TEST_BUCKET = 'baiji-test'

class TestS3TmpDir(unittest.TestCase):
    '''
    We test this separately since we use it in TestAWSBase.setUp()

    '''
    def setUp(self):
        self.s3_path = 'tmp/' + str(uuid.uuid4()) + '/'

    def tearDown(self):
        b = s3.S3Connection()._bucket(TEST_BUCKET)
        for key in b.list(self.s3_path[0:-1]):
            b.delete_key(key)

    def test_s3_tmpdir(self):
        def fake_uuid():
            fake_uuid.counter += 1
            return "FAKE-UUID-%d" % fake_uuid.counter
        fake_uuid.counter = 0
        self.assertEqual(
            s3.path.gettmpdir(bucket=TEST_BUCKET, prefix=self.s3_path, uuid_generator=fake_uuid),
            's3://%s/%sFAKE-UUID-1/' % (TEST_BUCKET, self.s3_path))
        self.assertEqual(
            len(list(s3.ls('s3://%s/%sFAKE-UUID-1' % (TEST_BUCKET, self.s3_path)))),
            1)
        self.assertTrue(
            s3.exists('s3://%s/%sFAKE-UUID-1/.tempdir' % (TEST_BUCKET, self.s3_path)))
        self.assertEqual(
            s3.path.gettmpdir(bucket=TEST_BUCKET, prefix=self.s3_path, uuid_generator=fake_uuid),
            's3://%s/%sFAKE-UUID-2/' % (TEST_BUCKET, self.s3_path))
        self.assertEqual(len(list(s3.ls('s3://%s/%sFAKE-UUID-2' % (TEST_BUCKET, self.s3_path)))), 1)
        self.assertTrue(s3.exists('s3://%s/%sFAKE-UUID-2/.tempdir' % (TEST_BUCKET, self.s3_path)))

class TestS3Path(unittest.TestCase):

    def test_s3_parse(self):
        def test(s, expect, on_windows=None):
            if on_windows and os.name == 'nt':
                expect = expect[:2] + (on_windows,)
            o = s3.path.parse(s)
            for ii in range(3):
                self.assertEqual(o[ii], expect[ii])

        test('s3://foo/path/to/bar', ('s3', 'foo', '/path/to/bar'))
        test('s3://xx', ('s3', 'xx', ''))
        test('s3://xx/', ('s3', 'xx', '/'))
        self.assertRaises(ValueError, s3.path.parse, 's3:///path/to/bar')
        test('file:///path/to/blah', ('file', '', '/path/to/blah'), on_windows=r'C:\path\to\blah')
        test('/path/to/blah', ('file', '', '/path/to/blah'), on_windows=r'C:\path\to\blah')
        test('path/to/blah', ('file', '', os.path.abspath('./path/to/blah')))
        test('~/path/to/blah', ('file', '', os.path.abspath(os.path.expanduser('~/path/to/blah'))))
        test('', ('file', '', os.path.abspath('.')))

        self.assertTrue(s3.path.islocal('/path/to/bar'))
        self.assertFalse(s3.path.islocal('s3://foo/path/to/bar'))
        self.assertFalse(s3.path.isremote('/path/to/bar'))
        self.assertTrue(s3.path.isremote('s3://foo/path/to/bar'))

        self.assertEqual(s3.path.join('s3://foo/path', 'to/bar'), 's3://foo/path/to/bar')
        if os.name == 'nt':
            self.assertEqual(s3.path.join('/foo/path', 'to/bar'), r'C:\foo\path\to\bar')
        else:
            self.assertEqual(s3.path.join('/foo/path', 'to/bar'), '/foo/path/to/bar')

        self.assertEqual(s3.path.basename('file:///foo/path/to/bar.baz'), 'bar.baz')
        self.assertEqual(s3.path.basename('s3://bucket/foo/path/to/bar.baz'), 'bar.baz')

        test('C:\\path\\of\\quux', ('file', '', 'C:\\path\\of\\quux'))
        test('file:///C:\\path\\of\\quux', ('file', '', 'C:\\path\\of\\quux'))

        with self.assertRaises(ValueError):
            s3.path.parse('file:///foo;bar')

        # Make sure it preserves trailing slashes
        test('path/to/blah/', ('file', '', os.path.join(os.path.abspath('./path/to/blah'), '')))
        test('s3://foo/path/to/blah/', ('s3', 'foo', '/path/to/blah/'))


class TestAWSBase(unittest.TestCase):
    """
    Provides framework for testing.
    Among others:
    self.local_file                         # A local file that exists
    self.tmp_dir                            # A local temporary directory (that exists)
    self.existing_remote_file               # A remote file that exists
    self.s3_path                            # A remote temporary "directory" (N.B. it does not "exist" a priori)
                                            # Note: this should be accessed with self.remote_file(filename) for full s3 url
    self.retriable_s3_call(call, retries=3) # For testing methods that may fail due to bad connections
    """
    def setUp(self):
        self.bucket = TEST_BUCKET
        self.s3_test_location = s3.path.gettmpdir(bucket=self.bucket)
        loc = s3.path.parse(self.s3_test_location)
        self.s3_path = loc.path

        b = s3.S3Connection()._bucket(self.bucket)
        for key in b.list(self.s3_path[1:]):
            b.delete_key(key)
        self.assertEqual(len([x for x in b.list(self.s3_path[1:])]), 0) # just make sure we're starting with a clean slate

        self.tmp_dir = tempfile.mkdtemp('bodylabs-test')
        self.local_file = create_random_temporary_file()


    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        os.remove(self.local_file)
        b = s3.S3Connection()._bucket(self.bucket)
        for key in b.list(self.s3_path[1:]):
            b.delete_key(key)
        self.assertEqual(len([x for x in b.list(self.s3_path[1:])]), 0)

    def retriable_s3_call(self, call, retries=3):
        from boto.exception import S3ResponseError
        import time
        try:
            return call()
        except S3ResponseError:
            if retries > 0:
                time.sleep(0.1)
                return self.retriable_s3_call(call, retries=retries-1)
            else:
                raise

    def assert_s3_exists(self, path):
        self.assertTrue(self.retriable_s3_call(lambda: s3.exists(path)))

    def assert_s3_does_not_exist(self, path):
        self.assertFalse(self.retriable_s3_call(lambda: s3.exists(path)))

    def assert_is_public(self, s3_url, is_public):
        from urlparse import urlparse
        url = urlparse(s3_url)
        acl = self.retriable_s3_call(lambda: s3.S3Connection()._bucket(url.netloc).get_acl(url.path[1:]))
        actual_is_public = False
        for grant in acl.acl.grants:
            if grant.permission == 'READ':
                if grant.uri == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    actual_is_public = True
        self.assertEquals(actual_is_public, is_public)

    def remote_file(self, path):
        return s3.path.join(self.s3_test_location, path)

    @property
    def existing_remote_file(self):
        '''
        In some tests it is convenient to have a file already on s3;
        in some others we need it not to be there (e.g. for clarity in the s3.ls test)
        '''
        uri = self.remote_file("FOO/A_preexisting_file.md")
        if not s3.exists(uri):
            s3.cp(self.local_file, uri)
        return uri


class TestAWS(TestAWSBase):

    def test_credentials(self):
        from baiji.config import credentials
        from baiji.util import yaml
        bodylabs_file_path = os.getenv('BODYLABS_CREDENTIAL_FILE', os.path.expanduser('~/.bodylabs'))
        if not os.path.exists(bodylabs_file_path):
            raise unittest.SkipTest("Skipping test_credentials because ~/.bodylabs doesn't exist.")
        truth = yaml.load(bodylabs_file_path)
        self.assertEqual(credentials.key, truth['AWS_ACCESS_KEY'])
        self.assertEqual(credentials.secret, truth['AWS_SECRET'])


class TestS3Exists(TestAWSBase):

    @mock.patch('baiji.s3.S3Connection._lookup')
    def test_s3_exists_retries_if_not_found_at_first(self, mock_lookup):
        import warnings
        from baiji.exceptions import EventualConsistencyWarning
        mock_key = "all_we_care_is_that_it's not None"
        mock_lookup.side_effect = [None, None, mock_key]
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            self.assertTrue(s3.exists('s3://foo'))
            # Verify the warning was triggered
            self.assertEqual(len(w), 1)
            self.assertIs(w[-1].category, EventualConsistencyWarning)
            self.assertEqual(str(w[-1].message), "S3 is behaving in an eventually consistent way in s3.exists(s3://foo) -- it took 3 attempts to locate the key")
        self.assertEqual(mock_lookup.call_count, 3)

    @mock.patch('baiji.s3.S3Connection._lookup')
    def test_s3_exists_does_not_retry_if_found_immidiately(self, mock_lookup):
        mock_key = "all_we_care_is_that_it's not None"
        mock_lookup.return_value = mock_key
        self.assertTrue(s3.exists('s3://foo'))
        self.assertEqual(mock_lookup.call_count, 1)

    @mock.patch('baiji.s3.S3Connection._lookup')
    def test_s3_exists_return_false_if_the_file_never_shows_up(self, mock_lookup):
        mock_key = "all_we_care_is_that_it's not None"
        mock_lookup.return_value = None
        self.assertFalse(s3.exists('s3://foo'))
        self.assertEqual(mock_lookup.call_count, 3)


class TestS3(TestAWSBase):

    def test_s3_cp_local_to_local(self):
        s3.cp(self.local_file, os.path.join(self.tmp_dir, 'TEST.foo'))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'TEST.foo')))

    def test_s3_cp_local_to_local_file_in_dir_that_needs_making(self):
        s3.cp(self.local_file, os.path.join(self.tmp_dir, 'FOO', 'TEST.foo'))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'FOO', 'TEST.foo')))

    def test_s3_cp_local_to_local_dir(self):
        s3.cp(self.local_file, self.tmp_dir)
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, os.path.basename(self.local_file))))

    def test_s3_cp_upload(self):
        s3.cp(self.local_file, self.remote_file("FOO/NAMED.md"))
        self.assert_s3_exists(self.remote_file("FOO/NAMED.md"))

    def test_s3_cp_download(self):
        s3.cp(self.existing_remote_file, os.path.join(self.tmp_dir, 'DL', 'TEST.foo'))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'DL', 'TEST.foo')))
        s3.cp(self.existing_remote_file, os.path.join(self.tmp_dir, 'DL'))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'DL', s3.path.basename(self.existing_remote_file))))

    @mock.patch('baiji.s3.S3CopyOperation.ensure_integrity')
    def test_s3_cp_download_corrupted_recover_in_one_retry(self, ensure_integrity_mock):
        from baiji.s3 import get_transient_error_class
        ensure_integrity_mock.side_effect = [get_transient_error_class()('etag does not match'), None]
        s3.cp(self.existing_remote_file, self.tmp_dir, force=True)

    @mock.patch('boto.s3.key.Key.get_contents_to_file')
    def test_downloads_from_s3_are_atomic_under_truncation(self, download_mock):
        from baiji.s3 import get_transient_error_class
        def write_fake_truncated_file(fp, **kwargs): # just capturing whatever is thrown at us: pylint: disable=unused-argument
            fp.write("12345")
        download_mock.side_effect = write_fake_truncated_file
        # Now when the call to download the file is made, the etags won't match
        with self.assertRaises(get_transient_error_class()):
            s3.cp(self.existing_remote_file, os.path.join(self.tmp_dir, 'truncated.foo'), validate=True)
        self.assertFalse(os.path.exists(os.path.join(self.tmp_dir, 'truncated.foo')))

    @mock.patch('baiji.s3.S3CopyOperation.ensure_integrity')
    def test_downloads_from_s3_are_atomic_under_exceptions(self, download_mock):
        download_mock.side_effect = ValueError()
        # Now when the call to download the file is made, an exception will be thrown.
        # ideally, we'd throw it "in" boto via a mock, but we really want to test that
        # the file doesn't get written, so let's go ahead and let boto do the download
        # and then throw the exception in the validation
        with self.assertRaises(ValueError):
            s3.cp(self.existing_remote_file, os.path.join(self.tmp_dir, 'erroneous.foo'), validate=True)
        self.assertFalse(os.path.exists(os.path.join(self.tmp_dir, 'erroneous.foo')))

    @mock.patch('baiji.s3.S3CopyOperation.ensure_integrity')
    def test_s3_cp_download_corrupted_raise_transient_error_after_retried_once(self, ensure_integrity_mock):

        from baiji.s3 import get_transient_error_class

        ensure_integrity_mock.side_effect = get_transient_error_class()('etag does not match')

        with self.assertRaises(get_transient_error_class()):
            s3.cp(self.existing_remote_file, self.tmp_dir, force=True)

    def test_s3_cp_in_s3(self):
        s3.cp(self.existing_remote_file, self.remote_file("COPY/NAMED.md"))
        self.assert_s3_exists(self.remote_file("COPY/NAMED.md"))

    def test_s3_cp_overwrite_errors_unless_force(self):
        s3.cp(self.local_file, os.path.join(self.tmp_dir, os.path.basename(self.local_file)))
        # local to local
        with self.assertRaises(s3.KeyExists):
            s3.cp(self.local_file, os.path.join(self.tmp_dir, os.path.basename(self.local_file)))
        with self.assertRaises(s3.KeyExists):
            s3.cp(self.local_file, self.tmp_dir)
        s3.cp(self.local_file, os.path.join(self.tmp_dir, os.path.basename(self.local_file)), force=True)
        s3.cp(self.local_file, self.tmp_dir, force=True)
        # local to remote
        with self.assertRaises(s3.KeyExists):
            s3.cp(self.local_file, self.existing_remote_file)
        # remote to local
        with self.assertRaises(s3.KeyExists):
            s3.cp(self.existing_remote_file, self.local_file)
        # remote to remote
        with self.assertRaises(s3.KeyExists):
            s3.cp(self.existing_remote_file, self.existing_remote_file)

    def test_s3_cp_errors_if_source_is_missing(self):
        # remote
        with self.assertRaisesRegexp(s3.KeyNotFound, "Error copying"):
            s3.cp(self.remote_file("definitely_not_there.foo"), self.tmp_dir)
        # local
        with self.assertRaisesRegexp(s3.KeyNotFound, "Error copying"):
            s3.cp(os.path.join(self.tmp_dir, "definitely_not_there.foo"), self.tmp_dir)


    def test_s3_cp_skip_existing_files_without_raise_exceptions(self):
        import warnings
        s3.cp(self.local_file, os.path.join(self.tmp_dir, os.path.basename(self.local_file)))
        with self.assertRaises(s3.KeyExists):
            s3.cp(self.local_file, os.path.join(self.tmp_dir, os.path.basename(self.local_file)))
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            s3.cp(self.local_file, os.path.join(self.tmp_dir, os.path.basename(self.local_file)), skip=True)
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Skipping" in str(w[-1].message)

    def test_s3_cp_errors_raised_by_missing_source_file(self):
        self.assertRaises(s3.KeyNotFound, s3.cp, os.path.join(self.tmp_dir, 'MISSING.file'), self.tmp_dir)
        self.assertRaises(s3.KeyNotFound, s3.cp, self.remote_file("MISSING.file"), self.tmp_dir)

    def test_s3_cp_errors_raised_by_unimplemented_source_scheme(self):
        self.assertRaises(s3.InvalidSchemeException, s3.cp, 'http://www.google.com/', self.tmp_dir)
        self.assertRaises(s3.InvalidSchemeException, s3.cp, self.local_file, 'http://www.google.com/')

    def test_s3_cp_relative_paths(self):
        s3.cp(self.local_file, 'test-DELETEME', force=True)
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'test-DELETEME')))
        s3.cp('test-DELETEME', self.remote_file("local"), force=True)
        self.assert_s3_exists(self.remote_file("local"))
        s3.rm('test-DELETEME')
        self.assertFalse(os.path.exists(os.path.join(os.getcwd(), 'test-DELETEME')))

    def test_s3_cp_HOME_paths(self):
        s3.cp(self.local_file, '~/test-DELETEME', force=True)
        self.assertTrue(os.path.exists(os.path.expanduser('~/test-DELETEME')))
        s3.cp('~/test-DELETEME', self.remote_file("local"), force=True)
        self.assert_s3_exists(self.remote_file("local"))
        s3.rm('~/test-DELETEME')
        self.assertFalse(os.path.exists(os.path.expanduser('~/test-DELETEME')))

    def test_s3_cp_policy(self):
        # test policy for file -> s3
        s3.cp(self.local_file, self.remote_file("public.md"), policy='public-read')
        self.assert_is_public(self.remote_file("public.md"), is_public=True)
        s3.cp(self.local_file, self.remote_file("private.md"), policy='bucket-owner-read')
        self.assert_is_public(self.remote_file("private.md"), is_public=False)

        # test policy for s3 -> s3
        s3.cp(self.remote_file("private.md"), self.remote_file("made_public_on_copy.md"), policy='public-read')
        self.assert_is_public(self.remote_file("made_public_on_copy.md"), is_public=True)

        s3.cp(self.remote_file("private.md"), self.remote_file("left_private_on_copy.md"))
        self.assert_is_public(self.remote_file("left_private_on_copy.md"), is_public=False)

        with self.assertRaises(ValueError):
            s3.cp(self.remote_file("private.md"), os.path.join(self.tmp_dir, 'NoCanDo.txt'), policy='public-read')

    def test_s3_cp_preserve_acl(self):
        s3.cp(self.local_file, self.remote_file("also_public.md"), policy='public-read')
        s3.cp(self.remote_file("also_public.md"), self.remote_file("still_public.md"), preserve_acl=True)
        self.assert_is_public(self.remote_file("also_public.md"), is_public=True)
        s3.cp(self.remote_file("also_public.md"), self.remote_file("no_longer_public.md"))
        self.assert_is_public(self.remote_file("no_longer_public.md"), is_public=False)

        with self.assertRaises(ValueError):
            s3.cp(self.remote_file("also_public.md"), os.path.join(self.tmp_dir, 'NoCanDo.txt'), preserve_acl=True)

    def test_s3_cp_content_encoding(self):
        s3.cp(self.local_file, self.remote_file("encoded.md"), encoding='gzip')
        self.assertEqual(s3.info(self.remote_file("encoded.md"))['content_encoding'], 'gzip')
        s3.cp(self.local_file, self.remote_file("notencoded.md")) # just make sure gzip isn't the default ;)
        self.assertNotEqual(s3.info(self.remote_file("notencoded.md"))['content_encoding'], 'gzip')
        s3.cp(self.remote_file("encoded.md"), self.remote_file("still_encoded.md"))
        self.assertEqual(s3.info(self.remote_file("still_encoded.md"))['content_encoding'], 'gzip')
        s3.cp(self.remote_file("notencoded.md"), self.remote_file("now_encoded.md"), encoding='gzip')
        self.assertEqual(s3.info(self.remote_file("now_encoded.md"))['content_encoding'], 'gzip')

    def test_s3_cp_content_type(self):
        s3.cp(self.local_file, self.remote_file("typed.md"), content_type='text/html')
        self.assertEqual(s3.info(self.remote_file("typed.md"))['content_type'], 'text/html')

        s3.cp(self.local_file, self.remote_file("nottyped.md")) # default is
        self.assertEqual(s3.info(self.remote_file("nottyped.md"))['content_type'], 'application/octet-stream')

        s3.cp(self.remote_file("typed.md"), self.remote_file("still_typed.md"))
        self.assertEqual(s3.info(self.remote_file("still_typed.md"))['content_type'], 'text/html')
        s3.cp(self.remote_file("nottyped.md"), self.remote_file("now_typed.md"), content_type='text/html')
        self.assertEqual(s3.info(self.remote_file("now_typed.md"))['content_type'], 'text/html')

    def test_s3_cp_gzip(self):
        s3.cp(self.local_file, self.remote_file("big.md"))
        s3.cp(self.local_file, self.remote_file("small.md"), gzip=True)
        self.assertNotEqual(s3.info(self.remote_file("big.md"))['content_encoding'], 'gzip')
        self.assertEqual(s3.info(self.remote_file("small.md"))['content_encoding'], 'gzip')
        self.assertLess(s3.info(self.remote_file("small.md"))['size'], s3.info(self.remote_file("big.md"))['size'])

    def test_s3_cp_trailing_slashes_in_dst(self):
        # https://bitbucket.org/bodylabs/core/issue/25
        s3.cp(self.local_file, os.path.join(self.tmp_dir, 'FOO2', ''))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'FOO2', os.path.basename(self.local_file))))
        s3.cp(self.local_file, self.remote_file("FOO2/"))
        self.assert_s3_exists(self.remote_file("FOO2/%s" % os.path.basename(self.local_file)))
        s3.cp(self.existing_remote_file, os.path.join(self.tmp_dir, 'DL2', ''))
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, 'DL2', s3.path.basename(self.existing_remote_file))))

    def test_s3_rm(self):
        for path in [os.path.join(self.tmp_dir, 'foo'), self.remote_file("foo")]:
            s3.cp(self.local_file, path)
            self.assert_s3_exists(path)
            s3.rm(path)
            self.assert_s3_does_not_exist(path)
            with self.assertRaises(s3.KeyNotFound):
                s3.rm(path)
        self.assertRaises(s3.InvalidSchemeException, s3.rm, ("http://example.com/foo"))

    def test_s3_ls(self):
        files = ["foo", "bar.baz", "quack/foo.foo"]
        for f in files:
            s3.cp(self.local_file, self.remote_file(f))
        self.assertEqual(set(s3.ls(self.s3_test_location)), set(map(lambda x: self.s3_path+x, files)))
        self.assertEqual(set(s3.ls(self.s3_test_location, return_full_urls=True)), set(map(lambda x: self.remote_file(x), files)))
        self.assertEqual(set(s3.ls(self.s3_test_location, shallow=True)), set(map(lambda x: self.s3_path+x, ['foo', 'bar.baz', 'quack/'])))

    def test_s3_md5(self):
        s3.cp(self.local_file, self.remote_file("file_to_md5"))
        from baiji.util.md5 import md5_for_file
        self.assertEqual(s3.md5(self.remote_file("file_to_md5")), md5_for_file(self.local_file))

    def test_strings(self):
        s = "TEST STRING"
        s3.put_string(self.remote_file("string"), s)
        self.assertEqual(s3.get_string(self.remote_file("string")), s)

    # TODO: Test with local paths. Instead of having a single local file
    # we can have a local subdirectory that is cleaned up on teardown.
    def test_s3_glob_match_single_wildcard(self):
        files = ['a.obj', 'b.obj', 'a.ply', 'a.object']
        for f in files:
            s3.cp(self.local_file, self.remote_file(f))
        glob_results = list(s3.glob(self.s3_test_location, '*.obj'))
        self.assertEqual(2, len(glob_results))
        self.assertEqual(set(glob_results), set(map(lambda f: self.remote_file(f), ['a.obj', 'b.obj'])))

    def test_s3_glob_match_multiple_wildcards(self):
        files = ['body_1_pose_T.obj', 'body_1_pose_Fun.obj', 'body_2_pose_T.obj', 'body_02_pose_T.obj']
        for f in files:
            s3.cp(self.local_file, self.remote_file(f))
        glob_results = list(s3.glob(self.s3_test_location, 'body_?_pose_*.obj'))
        self.assertEqual(3, len(glob_results))
        self.assertEqual(
            set(glob_results),
            set(map(lambda f: self.remote_file(f),
                    ['body_1_pose_T.obj', 'body_1_pose_Fun.obj', 'body_2_pose_T.obj']))
        )

    def test_s3_glob_exclude(self):
        files = ['pose_T.obj', 'pose_A.obj', 'pose_Scan.obj']
        for f in files:
            s3.cp(self.local_file, self.remote_file(f))
        glob_results = list(s3.glob(self.s3_test_location, 'pose_[!T].obj'))
        self.assertEqual(1, len(glob_results))
        self.assertEqual(set(glob_results), set(map(lambda f: self.remote_file(f), ['pose_A.obj'])))

    def test_s3_with_double_slashes_in_key(self):
        '''
        boto has a nasty behavior by default where it collapses `//` to `/` in keys
        '''
        s3.cp(self.local_file, self.remote_file('double//slashes//bork//boto.foo'))
        self.assertEqual([self.remote_file('double//slashes//bork//boto.foo')], list(s3.ls(self.remote_file(''), return_full_urls=True)))

    def test_s3_path_isdir(self):
        existing_remote_dir = os.path.dirname(self.existing_remote_file)
        #case: local dir, exists
        self.assertTrue(s3.path.isdir(self.tmp_dir))
        #case: local dir, does not exist
        self.assertFalse(s3.path.isdir(os.path.join(self.tmp_dir, 'does_not_exist')))
        #case: local dir, exists but is file
        self.assertFalse(s3.path.isdir(self.local_file))
        #case: remote dir, exists
        self.assertTrue(s3.path.isdir(existing_remote_dir))
        #case: remote dir, does not exist
        self.assertFalse(s3.path.isdir(self.remote_file('does_not_exist')))
        #case: remote dir, exists but is file
        self.assertFalse(s3.path.isdir(self.existing_remote_file))

    def test_s3_path_isfile(self):
        existing_remote_dir = os.path.dirname(self.existing_remote_file)
        #case: local file, exists
        self.assertTrue(s3.path.isfile(self.local_file))
        #case: local file, does not exist
        self.assertFalse(s3.path.isfile(os.path.join(self.tmp_dir, 'does_not_exist')))
        #case: local file, exists but is directory
        self.assertFalse(s3.path.isfile(self.tmp_dir))
        #case: remote file, exists
        self.assertTrue(s3.path.isfile(self.existing_remote_file))
        #case: remote file, does not exist
        self.assertFalse(s3.path.isfile(self.remote_file('does_not_exist')))
        #case: remote file, "exists" but is directory (so it actually doesn't exist but could return false positive)
        self.assertFalse(s3.path.isfile(existing_remote_dir))


class TestEncryption(TestAWSBase):
    def test_encrypt_in_place(self):
        s3.cp(self.local_file, self.remote_file("to_encrypt.txt"), encrypt=False) # just make sure there's something to copy
        self.assertFalse(s3.info(self.remote_file("to_encrypt.txt"))['encrypted'])
        s3.encrypt_at_rest(self.remote_file("to_encrypt.txt"))
        self.assertTrue(s3.info(self.remote_file("to_encrypt.txt"))['encrypted'])

    def test_upload(self):
        s3.cp(self.local_file, self.remote_file("unencrypted.txt"), encrypt=False)
        self.assertFalse(s3.info(self.remote_file("unencrypted.txt"))['encrypted'])
        s3.cp(self.local_file, self.remote_file("encrypted.txt")) # default now to encrypt
        self.assertTrue(s3.info(self.remote_file("encrypted.txt"))['encrypted'])

    def test_copy(self):
        s3.cp(self.local_file, self.remote_file("unencrypted.txt"), encrypt=False) # just make sure there's something to copy
        self.assertFalse(s3.info(self.remote_file("unencrypted.txt"))['encrypted'])
        s3.cp(self.remote_file("unencrypted.txt"), self.remote_file("encrypted.txt"))
        self.assertTrue(s3.info(self.remote_file("encrypted.txt"))['encrypted'])


class TestSync(TestAWSBase):
    def setUp(self):
        super(TestSync, self).setUp()

        # Files that are the same on both sides:
        self.create_random_file_at((self.tmp_dir, self.s3_test_location), 'foo/a.txt')
        self.create_random_file_at((self.tmp_dir, self.s3_test_location), 'foo/b.txt')
        self.create_random_file_at((self.tmp_dir, self.s3_test_location), 'foo/bar/c.txt')
        self.create_random_file_at((self.tmp_dir, self.s3_test_location), 'foo/bar/baz/d.txt')
        # Files that are different locally and remotely:
        self.create_random_file_at((self.tmp_dir,), 'foo/x.txt')
        self.create_random_file_at((self.s3_test_location,), 'foo/x.txt')
        self.create_random_file_at((self.tmp_dir,), 'foo/bar/x.txt')
        self.create_random_file_at((self.s3_test_location,), 'foo/bar/x.txt')
        # Files that are only local:
        self.create_random_file_at((self.tmp_dir,), 'foo/loc.txt')
        self.create_random_file_at((self.tmp_dir,), 'foo/bar/loc.txt')
        # Files that are only remote:
        self.create_random_file_at((self.s3_test_location,), 'foo/rem.txt')
        self.create_random_file_at((self.s3_test_location,), 'foo/bar/rem.txt')

        self.local_dir_to_sync = s3.path.join(self.tmp_dir, 'foo')
        self.remote_dir_to_sync = s3.path.join(self.s3_test_location, 'foo')

        self.expected_local_contents = s3.ls(self.local_dir_to_sync)
        self.expected_remote_contents = [x.replace(self.s3_path+'foo/', '') for x in s3.ls(self.remote_dir_to_sync)]

    def create_random_file_at(self, bases, path):
        from baiji.util.testing import random_data
        data = random_data()
        for base in bases:
            with s3.open(s3.path.join(base, path), 'w') as f:
                f.write(data)

    def assertContentsAre(self, expected_contents):
        self.assertSetEqual(set(s3.ls(self.local_dir_to_sync)), set(expected_contents))
        self.assertSetEqual(set([x.replace(self.s3_path+'foo/', '') for x in s3.ls(self.remote_dir_to_sync)]), set(expected_contents))
        # TODO files are equal:


    def test_sync_local_to_remote(self):
        s3.sync(self.local_dir_to_sync, self.remote_dir_to_sync)
        self.assertContentsAre(self.expected_local_contents)

    def test_sync_remote_to_local(self):
        s3.sync(self.remote_dir_to_sync, self.local_dir_to_sync)
        self.assertContentsAre(self.expected_remote_contents)

    @mock.patch('baiji.s3.S3Connection.cp')
    @mock.patch('baiji.s3.S3Connection.rm')
    def test_sync_file_same(self, rm, cp):
        # In these tests, we want to check that rm and cp are invoked only
        # when they should be, so we mock out cp and rm on a new instance of
        # S3Connection. (It seems difficult to use mock.patch on module
        # methods.)
        #
        # We also need s3.path.join but it's defined on the module, not on
        # instances of S3Connection.
        from baiji.s3 import S3Connection

        s3_with_mocks = S3Connection()

        s3_with_mocks.sync_file(
            s3.path.join(self.local_dir_to_sync, 'a.txt'),
            s3.path.join(self.remote_dir_to_sync, 'a.txt')
        )

        self.assertFalse(cp.called)
        self.assertFalse(rm.called)

    @mock.patch('baiji.s3.S3Connection.cp')
    @mock.patch('baiji.s3.S3Connection.rm')
    def test_sync_file_only_src(self, rm, cp):
        from baiji.s3 import S3Connection

        s3_with_mocks = S3Connection()

        s3_with_mocks.sync_file(
            s3.path.join(self.local_dir_to_sync, 'loc.txt'),
            s3.path.join(self.remote_dir_to_sync, 'loc.txt')
        )

        cp.assert_called_once_with(
            s3.path.join(self.local_dir_to_sync, 'loc.txt'),
            s3.path.join(self.remote_dir_to_sync, 'loc.txt'),
            force=False,
            progress=False,
            policy=None,
            encoding=None,
            encrypt=True,
            guess_content_type=False
        )
        self.assertFalse(rm.called)

    @mock.patch('baiji.s3.S3Connection.cp')
    @mock.patch('baiji.s3.S3Connection.rm')
    def test_sync_file_only_dst(self, rm, cp):
        from baiji.s3 import S3Connection

        s3_with_mocks = S3Connection()

        # Test with delete=True and delete=False.

        s3_with_mocks.sync_file(
            s3.path.join(self.local_dir_to_sync, 'rem.txt'),
            s3.path.join(self.remote_dir_to_sync, 'rem.txt'),
            delete=True
        )

        self.assertFalse(cp.called)
        rm.assert_called_once_with(
            s3.path.join(self.remote_dir_to_sync, 'rem.txt')
        )

        rm.reset_mock()

        with self.assertRaises(s3.KeyNotFound):
            s3_with_mocks.sync_file(
                s3.path.join(self.local_dir_to_sync, 'rem.txt'),
                s3.path.join(self.remote_dir_to_sync, 'rem.txt'),
                delete=False
            )

        self.assertFalse(cp.called)
        self.assertFalse(rm.called)

    @mock.patch('baiji.s3.S3Connection.cp')
    @mock.patch('baiji.s3.S3Connection.rm')
    def test_sync_file_exists_but_outdated(self, rm, cp):
        from baiji.s3 import S3Connection

        s3_with_mocks = S3Connection()

        # Test with update=True and update=False.

        s3_with_mocks.sync_file(
            s3.path.join(self.local_dir_to_sync, 'x.txt'),
            s3.path.join(self.remote_dir_to_sync, 'x.txt'),
            update=True
        )

        cp.assert_called_once_with(
            s3.path.join(self.local_dir_to_sync, 'x.txt'),
            s3.path.join(self.remote_dir_to_sync, 'x.txt'),
            force=True,
            progress=False,
            policy=None,
            encoding=None,
            encrypt=True,
            guess_content_type=False
        )
        self.assertFalse(rm.called)

        cp.reset_mock()

        s3_with_mocks.sync_file(
            s3.path.join(self.local_dir_to_sync, 'x.txt'),
            s3.path.join(self.remote_dir_to_sync, 'x.txt'),
            update=False
        )

        self.assertFalse(cp.called)
        self.assertFalse(rm.called)


class TestCachedFile(TestAWSBase):
    def setUp(self):
        super(TestCachedFile, self).setUp()
        s3.cp(self.local_file, self.remote_file("openable"))
        with open(self.local_file, 'rb') as f:
            self.truth = f.read()

    def test_s3_open_read_remote_file_with_context_manager(self):
        self.assert_s3_exists(self.remote_file("openable"))

        with s3.open(self.remote_file("openable"), 'r') as f:
            tempname = f.name
            self.assertEqual(self.truth, f.read())

        self.assertFalse(os.path.exists(tempname))

    def test_s3_open_read_remote_file_without_context_manager(self):
        self.assert_s3_exists(self.remote_file("openable"))

        f = s3.open(self.remote_file("openable"), 'r')
        tempname = f.name
        self.assertEqual(self.truth, f.read())
        f.close()

        self.assertFalse(os.path.exists(tempname))

    def test_s3_open_read_local_file_with_context_manager(self):
        self.assert_s3_exists(self.local_file)

        with s3.open(self.local_file, 'r') as f:
            self.assertEqual(self.truth, f.read())
            self.assertEqual(f.name, self.local_file)

    def test_s3_open_read_local_file_without_context_manager(self):
        self.assert_s3_exists(self.local_file)

        f = s3.open(self.local_file, 'r')
        self.assertEqual(self.truth, f.read())
        self.assertEqual(f.name, self.local_file)
        f.close()

    def test_s3_open_write_remote_file_with_context_manager(self):
        remote_file_name = self.remote_file("write_test_1")
        local_file_name = os.path.join(self.tmp_dir, "write_test_1")
        self.assert_s3_does_not_exist(remote_file_name)

        with s3.open(remote_file_name, 'w') as f:
            tempname = f.name
            f.write(self.truth)

        self.assertFalse(os.path.exists(tempname))
        self.assert_s3_exists(remote_file_name)
        # download and confirm that it contains the correct contents
        s3.cp(remote_file_name, local_file_name)
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_write_local_file_creates_parent_dirs(self):
        local_file_name = os.path.join(self.tmp_dir, "subdir", "write_test_subdir")
        self.assert_s3_does_not_exist(local_file_name)
        self.assert_s3_does_not_exist(os.path.dirname(local_file_name))

        with s3.open(local_file_name, 'w') as f:
            f.write(self.truth)

        self.assert_s3_exists(local_file_name)
        self.assert_s3_exists(os.path.dirname(local_file_name))

    def test_s3_open_write_remote_file_without_context_manager(self):
        remote_file_name = self.remote_file("write_test_2")
        local_file_name = os.path.join(self.tmp_dir, "write_test_2")
        self.assert_s3_does_not_exist(remote_file_name)

        f = s3.open(remote_file_name, 'w')
        tempname = f.name
        f.write(self.truth)
        f.close()

        self.assertFalse(os.path.exists(tempname))
        self.assert_s3_exists(remote_file_name)
        # download and confirm that it contains the correct contents
        s3.cp(remote_file_name, local_file_name)
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_write_local_file_with_context_manager(self):
        local_file_name = os.path.join(self.tmp_dir, "write_test_local_1")
        self.assert_s3_does_not_exist(local_file_name)

        with s3.open(local_file_name, 'w') as f:
            self.assertEqual(f.name, local_file_name)
            f.write(self.truth)

        self.assert_s3_exists(local_file_name)
        # confirm that it contains the correct contents
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_write_local_file_without_context_manager(self):
        local_file_name = os.path.join(self.tmp_dir, "write_test_local_2")
        self.assert_s3_does_not_exist(local_file_name)

        f = s3.open(local_file_name, 'w')
        self.assertEqual(f.name, local_file_name)
        f.write(self.truth)
        f.close()

        self.assert_s3_exists(local_file_name)
        # confirm that it contains the correct contents
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_exclusive_write_remote_file_throws_error_for_existing_file(self):
        self.assert_s3_exists(self.remote_file("openable"))
        with self.assertRaises(s3.KeyExists):
            s3.open(self.remote_file("openable"), 'x')

    def test_s3_open_exclusive_write_local_file_throws_error_for_existing_file(self):
        self.assert_s3_exists(self.local_file)
        with self.assertRaises(s3.KeyExists):
            s3.open(self.local_file, 'x')

    def test_s3_open_exclusive_write_remote_file_throws_error_for_double_open(self):
        self.assert_s3_does_not_exist(self.remote_file("exclusive_write_test_3"))
        with s3.open(self.remote_file("exclusive_write_test_3"), 'x') as f1:
            with self.assertRaises(s3.KeyExists):
                with s3.open(self.remote_file("exclusive_write_test_3"), 'x') as f2:
                    pass

    def test_s3_open_exclusive_write_local_file_throws_error_for_double_open(self):
        local_file_name = os.path.join(self.tmp_dir, "exclusive_write_test_local_3")
        self.assert_s3_does_not_exist(local_file_name)
        with s3.open(local_file_name, 'x') as f1:
            with self.assertRaises(s3.KeyExists):
                with s3.open(local_file_name, 'x') as f2:
                    pass

    def test_s3_open_exclusive_write_remote_file_with_context_manager(self):
        remote_file_name = self.remote_file("exclusive_write_test_1")
        local_file_name = os.path.join(self.tmp_dir, "exclusive_write_test_1")
        self.assert_s3_does_not_exist(remote_file_name)

        with s3.open(remote_file_name, 'x') as f:
            self.assert_s3_exists(remote_file_name)
            tempname = f.name
            f.write(self.truth)

        self.assertFalse(os.path.exists(tempname))
        self.assert_s3_exists(remote_file_name)
        # download and confirm that it contains the correct contents
        s3.cp(remote_file_name, local_file_name)
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_exclusive_write_remote_file_without_context_manager(self):
        remote_file_name = self.remote_file("exclusive_write_test_2")
        local_file_name = os.path.join(self.tmp_dir, "exclusive_write_test_2")
        self.assert_s3_does_not_exist(remote_file_name)

        f = s3.open(remote_file_name, 'x')
        self.assert_s3_exists(remote_file_name)
        tempname = f.name
        f.write(self.truth)
        f.close()

        self.assertFalse(os.path.exists(tempname))
        self.assert_s3_exists(remote_file_name)
        # download and confirm that it contains the correct contents
        s3.cp(remote_file_name, local_file_name)
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_exclusive_write_local_file_with_context_manager(self):
        local_file_name = os.path.join(self.tmp_dir, "exclusive_write_test_local_1")
        self.assert_s3_does_not_exist(local_file_name)

        with s3.open(local_file_name, 'x') as f:
            self.assertEqual(f.name, local_file_name)
            f.write(self.truth)

        self.assert_s3_exists(local_file_name)
        # confirm that it contains the correct contents
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_exclusive_write_local_file_without_context_manager(self):
        local_file_name = os.path.join(self.tmp_dir, "exclusive_write_test_local_2")
        self.assert_s3_does_not_exist(local_file_name)

        f = s3.open(local_file_name, 'x')
        self.assertEqual(f.name, local_file_name)
        f.write(self.truth)
        f.close()

        self.assert_s3_exists(local_file_name)
        # confirm that it contains the correct contents
        with open(local_file_name) as f:
            self.assertEqual(self.truth, f.read())

    def test_s3_open_read_raises_error_for_nonexistent_remote_file(self):
        nonexistent_file = self.remote_file(str(uuid.uuid4()))
        self.assert_s3_does_not_exist(nonexistent_file)
        with self.assertRaises(s3.KeyNotFound):
            s3.open(nonexistent_file, 'r')

    def test_s3_open_write_does_not_raise_error_for_nonexistent_remote_file(self):
        nonexistent_file = self.remote_file(str(uuid.uuid4()))
        self.assert_s3_does_not_exist(nonexistent_file)
        with s3.open(nonexistent_file, 'w') as f:
            test_string = 'FOO!\n'
            f.write(test_string)
        self.assert_s3_exists(nonexistent_file)

    def test_s3_open_write_update_raises_error_for_nonexistent_remote_file(self):
        nonexistent_file = self.remote_file(str(uuid.uuid4()))
        self.assert_s3_does_not_exist(nonexistent_file)
        with self.assertRaises(NotImplementedError):
            s3.open(nonexistent_file, 'w+')

    def test_s3_open_exclusive_write_does_not_raise_error_for_nonexistent_remote_file(self):
        nonexistent_file = self.remote_file(str(uuid.uuid4()))
        self.assert_s3_does_not_exist(nonexistent_file)
        with s3.open(nonexistent_file, 'x') as f:
            test_string = 'FOO!\n'
            f.write(test_string)
        self.assert_s3_exists(nonexistent_file)

    def test_s3_open_read_raises_error_for_nonexistent_local_file(self):
        nonexistent_file = os.path.join(self.tmp_dir, "test_s3_open_read_raises_error_for_nonexistent_local_file")
        self.assert_s3_does_not_exist(nonexistent_file)
        with self.assertRaises(s3.KeyNotFound):
            s3.open(nonexistent_file, 'r')

    def test_s3_open_write_does_not_raise_error_for_nonexistent_local_file(self):
        nonexistent_file = os.path.join(self.tmp_dir, "test_s3_open_write_does_not_raise_error_for_nonexistent_local_file")
        self.assert_s3_does_not_exist(nonexistent_file)
        with s3.open(nonexistent_file, 'w') as f:
            test_string = 'FOO!\n'
            f.write(test_string)
        self.assert_s3_exists(nonexistent_file)

    def test_s3_open_write_update_does_not_raise_error_for_nonexistent_local_file(self):
        nonexistent_file = os.path.join(self.tmp_dir, "test_s3_open_write_update_does_not_raise_error_for_nonexistent_local_file")
        self.assert_s3_does_not_exist(nonexistent_file)
        with s3.open(nonexistent_file, 'w+') as f:
            test_string = 'FOO!\n'
            f.write(test_string)
            f.seek(0)
            self.assertEqual(test_string, f.read())
        self.assert_s3_exists(nonexistent_file)

    def test_s3_open_exclusive_write_does_not_raise_error_for_nonexistent_local_file(self):
        nonexistent_file = os.path.join(self.tmp_dir, "test_s3_open_exclusive_write_does_not_raise_error_for_nonexistent_local_file")
        self.assert_s3_does_not_exist(nonexistent_file)
        with s3.open(nonexistent_file, 'x') as f:
            test_string = 'FOO!\n'
            f.write(test_string)
        self.assert_s3_exists(nonexistent_file)

    def test_s3_open_local_underlying_error_raises_ioerror_with_errno_and_strerror(self):
        import errno
        with self.assertRaises(IOError) as ctx:
            s3.open(os.getcwd(), 'w')
        self.assertEquals(ctx.exception.errno, errno.EISDIR)
        self.assertIn('Is a directory:', ctx.exception.strerror)

    @mock.patch('baiji.s3.CachedFile.upload')
    def test_s3_open_write_calls_upload(self, upload):
        remote_file_name = self.remote_file("write_test_1")
        with s3.open(remote_file_name, 'w') as f:
            self.assertFalse(upload.called)
        self.assertTrue(upload.called)

    @mock.patch('baiji.s3.CachedFile.upload')
    def test_s3_open_write_does_not_upload_if_exception_raised(self, upload):
        remote_file_name = self.remote_file("write_test_1")
        try:
            with s3.open(remote_file_name, 'w') as f:
                raise AttributeError()
        except AttributeError:
            pass
        self.assertFalse(upload.called)

        # Sanity check
        with s3.open(remote_file_name, 'w') as f:
            pass
        self.assertTrue(upload.called)

    @mock.patch('baiji.s3.CachedFile.upload')
    def test_s3_open_read_does_not_call_upload(self, upload):
        self.assert_s3_exists(self.remote_file("openable"))
        with s3.open(self.remote_file("openable"), 'r') as f:
            pass
        self.assertFalse(upload.called)
