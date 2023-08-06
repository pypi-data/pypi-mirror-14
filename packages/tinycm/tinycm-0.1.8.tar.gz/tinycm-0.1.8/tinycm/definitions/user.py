from tinycm import DefinitionConflictError, InvalidParameterError, ExecutionResult
from tinycm.basedefinition import BaseDefinition
import os
import pwd
import grp
import spwd
import crypt
from hmac import compare_digest as compare_hash
from tinycm.reporting import VerifyResult
import subprocess


class UserDefinition(BaseDefinition):
    def __init__(self, identifier, parameters, source, after, context):

        # Run the BaseDefinition init so the graph library works
        super().__init__(identifier)

        # The usual fields
        self.identifier = identifier
        self.source = source
        self.after = after
        self.context = context
        self.name = parameters['name']
        self.ensure = parameters['ensure']

        # Optional fields
        self.password = parameters['password'] if 'pasword' in parameters else None
        self.password_hash = parameters['password-hash'] if 'password-hash' in parameters else None
        self.uid = parameters['uid'] if 'uid' in parameters else None
        self.gid = parameters['gid'] if 'gid' in parameters else None
        self.comment = parameters['comment'] if 'comment' in parameters else None
        self.homedir = parameters['homedir'] if 'homedir' in parameters else None
        self.shell = parameters['shell'] if 'shell' in parameters else "/bin/false"
        self.extra_groups = parameters['groups'] if 'groups' in parameters else None
        self.manage_home = parameters['manage-home'] if 'manage-home' in parameters else False

    def try_merge(self, other):

        # Check for conflicting parameters
        if self.ensure != other.ensure:
            raise DefinitionConflictError('Duplicate definition for {} with different ensure'.format(self.identifier))

        if self.comment and other.comment and self.comment != other.comment:
            raise DefinitionConflictError('Duplicate definition for {} with different comment'.format(self.identifier))

        if self.shell != "/bin/false" and other.shell != "/bin/false" and self.shell != other.shell:
            raise DefinitionConflictError('Duplicate definition for {} with different shell'.format(self.identifier))

        if self.uid and other.uid and self.uid != other.uid:
            raise DefinitionConflictError('Duplicate definition for {} with different uid'.format(self.identifier))

        if self.gid and other.gid and self.gid != other.gid:
            raise DefinitionConflictError('Duplicate definition for {} with different uid'.format(self.identifier))

        if self.password and other.password and self.password != other.password:
            raise DefinitionConflictError('Duplicate definition for {} with different password'.format(self.identifier))

        if self.password_hash and other.password_hash and self.password_hash != other.password_hash:
            raise DefinitionConflictError(
                    'Duplicate definition for {} with different password-hash'.format(self.identifier))

        # Merge non-conflicting parameters
        if not self.comment and other.comment:
            self.comment = other.comment

        if self.shell == "/bin/false" and other.shell != "/bin/false":
            self.shell = other.shell

        if not self.uid and other.uid:
            self.uid = other.uid

        if not self.gid and other.gid:
            self.gid = other.gid

        if not self.password and other.password:
            self.password = other.password

        if not self.password_hash and other.password_hash:
            self.password_hash = other.password_hash

        # The passwords are an edge case
        if self.password and self.password_hash:
            raise DefinitionConflictError("Both password and password-hash defined after merge")

        # Merge lists
        if self.extra_groups or other.extra_groups:
            if not self.extra_groups:
                self.extra_groups = []
            if not other.extra_groups:
                other.extra_groups = []
            self.extra_groups = list(set(self.extra_groups) | set(other.extra_groups))
        self.after = list(set(self.after) | set(other.after))

        return self

    def lint(self):

        # Verify some conflicting options
        if self.password and self.password_hash:
            raise InvalidParameterError('Both password and password-hash defined.')

        # Check input enum validity
        if self.ensure not in ['exists', 'removed']:
            raise InvalidParameterError('Ensure not in [exists, removed]')
        if not os.path.isfile(self.shell):
            raise InvalidParameterError('Shell "{}" does not exist'.format(self.shell))

    def verify(self):

        # Verify the state of this class against the current running linux config using the pwd, grp and spwd modules
        should_exist = self.ensure == 'exists'
        try:
            name, passwd, uid, gid, comment, homedir, shell = pwd.getpwnam(self.name)
            exists = True
        except KeyError:
            exists = False

        if should_exist and not exists:
            return VerifyResult(self.identifier, success=False, message="User '{}' doesn't exist".format(self.name))
        if not should_exist and exists:
            return VerifyResult(self.identifier, success=False, message="User '{}' exists".format(self.name))

        if exists:
            if self.uid and uid != self.uid:
                return VerifyResult(self.identifier, success=False,
                                    message="Uid {} doesn't match {}".format(uid, self.uid))

            if self.shell and self.shell != shell:
                return VerifyResult(self.identifier, success=False,
                                    message="Shell '{}' doesn't match '{}'".format(shell, self.shell))

            if self.gid and self.gid != gid:
                return VerifyResult(self.identifier, success=False,
                                    message="Shell {} doesn't match {}".format(gid, self.gid))

            if self.comment and self.comment != comment:
                return VerifyResult(self.identifier, success=False,
                                    message="Comment '{}' doesn't match '{}'".format(comment, self.comment))

            if self.homedir and self.homedir != homedir:
                return VerifyResult(self.identifier, success=False,
                                    message="Home directory '{}' doesn't match '{}'".format(homedir, self.homedir))

            if self.password or self.password_hash:
                pwhash = spwd.getspnam(self.name)[1]

                if self.password_hash and self.password_hash != pwhash:
                    return VerifyResult(self.identifier, success=False, message="Password hash doesn't match")

                if compare_hash(crypt.crypt(self.password, pwhash), pwhash):
                    return VerifyResult(self.identifier, success=False, message="Password doesn't match with hash")

            if self.extra_groups:
                groups = set([g.gr_name for g in grp.getgrall() if self.name in g.gr_mem])
                wanted_groups = set(self.extra_groups)

                missing = wanted_groups - groups
                invalid = groups - wanted_groups

                if len(missing) > 0:
                    return VerifyResult(self.identifier, success=False,
                                        message="Missing groups: {}".format(', '.join(missing)))

                if len(invalid) > 0:
                    return VerifyResult(self.identifier, success=False,
                                        message="Invalid groups: {}".format(', '.join(invalid)))
        return VerifyResult(self.identifier, success=True)

    def execute(self):
        vresult = self.verify()
        if not vresult.success:
            should_exist = self.ensure == 'exists'
            try:
                pwd.getpwnam(self.name)
                exists = True
            except KeyError:
                exists = False

            if not should_exist and exists:
                if self.manage_home:
                    subprocess.check_call(['userdel', '-r', self.name])
                else:
                    subprocess.check_call(['userdel', self.name])
                return ExecutionResult('Removed user {}'.format(self.name))

            if should_exist and not exists:
                command = ['useradd', '--shell', self.shell]
                if self.gid:
                    command.extend(['--gid', str(self.gid)])
                if self.extra_groups:
                    command.extend(['--groups', ','.join(self.extra_groups)])
                if self.uid:
                    command.extend(['--uid', str(self.uid)])
                if self.homedir:
                    command.extend(['--home', self.homedir])
                if self.comment:
                    command.extend(['--comment', self.comment])
                if self.password_hash:
                    command.extend(['--password', self.password_hash])
                    # TODO: Implement password hashing
                if self.manage_home:
                    command.append('--create-home')

                subprocess.check_call(command)

            if should_exist and exists:
                # TODO: Implement updating user
                pass
