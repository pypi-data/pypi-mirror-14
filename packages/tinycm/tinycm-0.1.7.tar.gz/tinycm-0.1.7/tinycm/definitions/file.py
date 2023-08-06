from tinycm import DefinitionConflictError, InvalidParameterError, ExecutionResult
from tinycm.basedefinition import BaseDefinition
from tinycm.reporting import VerifyResult
import os
import grp
import pwd
import stat
import requests
import difflib


class FileDefinition(BaseDefinition):
    def __init__(self, identifier, parameters, source, after, context):
        self.source = source
        self.after = after
        self.identifier = identifier
        self.type = parameters['type']
        self.path = parameters['name']
        self.contents = parameters['contents']
        self.context = context

        # Optional parameters
        self.interpolate = parameters['interpolate'] if 'interpolate' in parameters else False
        self.encoding = parameters['encoding'] if 'encoding' in parameters else 'utf-8'
        self.ensure = parameters['ensure'] if 'ensure' in parameters else 'contents'
        self.permission_mask = parameters['permission-mask'] if 'permission-mask' in parameters else None
        self.owner = parameters['owner'] if 'owner' in parameters else None
        self.group = parameters['group'] if 'group' in parameters else None

        # Internal parameters
        self._fetched_and_interpolated = False

        super().__init__(identifier)

    def try_merge(self, other):
        if self.type != other.type:
            raise DefinitionConflictError('Duplicate definition for {} with different type'.format(self.identifier))
        if self.contents != other.contents:
            raise DefinitionConflictError('Duplicate definition for {} with different contents'.format(self.identifier))

        if self.encoding and self.encoding != other.encoding:
            raise DefinitionConflictError('Duplicate definition for {} with different encoding'.format(self.identifier))

        if self.owner and self.owner != other.owner:
            raise DefinitionConflictError('Duplicate definition for {} with different owner'.format(self.identifier))

        if self.group and self.group != other.group:
            raise DefinitionConflictError('Duplicate definition for {} with different group'.format(self.identifier))

        if self.permission_mask and other.permission_mask:
            perm_user, perm_group, perm_other = self.permission_mask.split()
            other_user, other_group, other_other = other.permission_mask.split()

            if perm_user != 'x' and other_user != 'x' and perm_user != other_user:
                raise DefinitionConflictError('Duplicate definition for user in permission-mask')
            if perm_group != 'x' and other_group != 'x' and perm_group != other_group:
                raise DefinitionConflictError('Duplicate definition for group in permission-mask')
            if perm_other != 'x' and other_other != 'x' and perm_other != other_other:
                raise DefinitionConflictError('Duplicate definition for other in permission-mask')

            if perm_user == 'x':
                perm_user = other_user
            if perm_group == 'x':
                perm_group = other_group
            if perm_other == 'x':
                perm_other = other_other

            self.permission_mask = ''.join([perm_user, perm_group, perm_other])
        if not self.permission_mask:
            self.permission_mask = other.permission_mask

        return self

    def _ensure_contents(self):
        if self._fetched_and_interpolated:
            return

        if self.type == 'http':
            url = self.contents
            response = requests.get(url)
            self.contents = response.content().decode(self.encoding)

        if self.interpolate:
            self.contents = self.contents.format(**self.context)

        self._fetched_and_interpolated = True

    def lint(self):
        if self.type not in ['constant', 'http']:
            raise InvalidParameterError('Type not in [constant, http]')
        if self.ensure not in ['deleted', 'exists', 'contents']:
            raise InvalidParameterError('Ensure not in [deleted, exists, contents]')

    def verify(self):
        self._ensure_contents()
        if not os.path.isfile(self.path):
            return VerifyResult(self.identifier, success=False, message="File {} does not exist".format(self.path))
        if self.type == 'constant':
            with open(self.path) as input_file:
                contents = input_file.read()
            if contents != self.contents:
                return VerifyResult(self.identifier, success=False,
                                    message="File contents incorrect for {}".format(self.path))
        if self.permission_mask:
            file_info = os.stat(self.path)
            file_uid = file_info[stat.ST_UID]
            file_gid = file_info[stat.ST_GID]
            file_mask = str(oct(file_info[stat.ST_MODE]))[-3:]

            if isinstance(self.owner, int):
                if self.owner != file_uid:
                    return VerifyResult(self.identifier, success=False,
                                        message="Incorrect UID for file {}".format(self.path))
            else:
                file_owner = pwd.getpwuid(file_uid).pw_name
                if self.owner != file_owner:
                    return VerifyResult(self.identifier, success=False,
                                        message="Incorrect owner for file {}".format(self.path))

            if isinstance(self.group, int):
                if self.group != file_gid:
                    return VerifyResult(self.identifier, success=False,
                                        message="Incorrect GID for file {}".format(self.path))
            else:
                file_group = grp.getgrgid(file_gid).gr_name
                if self.group != file_group:
                    return VerifyResult(self.identifier, success=False,
                                        message="Incorrect group for file {}".format(self.path))

            mask_part = file_mask.split()
            mask_part_want = self.permission_mask.split()
            for i in range(0, 3):
                if mask_part_want[i] != 'x' and mask_part_want[i] != mask_part[i]:
                    return VerifyResult(self.identifier, success=False,
                                        message="Incorrect mode for file {}".format(self.path))

        return VerifyResult(self.identifier, success=True)

    def execute(self):
        self._ensure_contents()
        verify_result = self.verify()
        exists = os.path.isfile(self.path)
        if exists:
            with open(self.path, 'r') as input_file:
                old_file = input_file.readlines()

        if not verify_result.success:
            with open(self.path, 'w') as target_file:
                target_file.write(self.contents)

        if exists:
            new_lines = self.contents.splitlines(True)
            diff = difflib.unified_diff(old_file, new_lines,
                                        fromfile="old {}".format(self.path),
                                        tofile="new ".format(self.path))
            self._execute_permissions()
            return ExecutionResult(message="Updated file {}".format(self.path), diff=diff)
        else:
            self._execute_permissions()
            return ExecutionResult(message="Created file {}".format(self.path), diff=self.contents.split("\n"))

    def _execute_permissions(self):
        mask, uid, gid = self._get_file_perms()

        if self.owner:
            if isinstance(self.owner, int):
                uid = self.owner
            else:
                uid = pwd.getpwnam(self.owner).pw_uid

        if self.group:
            if isinstance(self.group, int):
                gid = self.group
            else:
                gid = grp.getgrnam(self.group).gr_gid

        if self.permission_mask:
            mask = self._merge_permission_mask(mask, self.permission_mask)

        os.chown(self.path, uid, gid)
        os.chmod(self.path, self._oct_to_dec(int(mask)))

    def _merge_permission_mask(self, mask1, mask2):
        mask1 = list(mask1)
        for i in range(0, 3):
            if mask2[i] != 'x':
                mask1[i] = mask2[i]

        return ''.join(mask1)

    def _get_file_perms(self):
        file_info = os.stat(self.path)
        file_uid = file_info[stat.ST_UID]
        file_gid = file_info[stat.ST_GID]
        file_mask = str(oct(file_info[stat.ST_MODE]))[-3:]
        return file_mask, file_uid, file_gid

    def _oct_to_dec(self, input_number):
        return sum(int(digit) * (8 ** power) for power, digit in enumerate(str(input_number)[::-1]))
