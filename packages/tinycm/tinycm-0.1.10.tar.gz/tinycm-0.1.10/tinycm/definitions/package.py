from tinycm import DefinitionConflictError, InvalidParameterError, ExecutionResult
from tinycm.basedefinition import BaseDefinition
import subprocess
import distro
from tinycm.reporting import VerifyResult
import logging

logger = None


class PackageDefinition(BaseDefinition):
    def __init__(self, identifier, parameters, source, after, context):
        self.source = source
        self.after = after
        self.identifier = identifier
        self.package = parameters['name']
        self.ensure = parameters['ensure']
        self.packagemanager = 'autodetect'
        if 'packagemanager' in parameters:
            self.packagemanager = parameters['packagemanager']
        super().__init__(identifier)

        global logger
        logger = logging.getLogger('tinycm')

    def try_merge(self, other):
        if self.ensure != other.ensure:
            raise DefinitionConflictError('Duplicate definition for {} with different ensure'.format(self.identifier))
        if self.packagemanager != other.packagemanager:
            if self.packagemanager == 'autodetect':
                self.packagemanager = other.packagemanager
            elif other.packagemanager != 'autodetect':
                raise DefinitionConflictError(
                        'Duplicate definition for {} with different packagemanager'.format(self.identifier))
        return self

    def _pm_check(self):
        if self.packagemanager == 'autodetect':
            current_distro = distro.identify()
            command_template = current_distro.command['package']['is-installed']
        elif self.packagemanager == 'apt':
            command_template = 'dpkg -s {}'
        elif self.packagemanager == 'pacman':
            command_template = 'pacman -Q {}'
        else:
            raise NotImplementedError()

        try:
            subprocess.check_output(command_template.format(self.package), shell=True, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def _pm_install(self):
        if self.packagemanager == 'autodetect':
            current_distro = distro.identify()
            command_template = current_distro.command['package']['install']
        elif self.packagemanager == 'apt':
            command_template = 'apt-get -y install --no-install-recommends {}'
        elif self.packagemanager == 'pacman':
            command_template = 'pacman -S --noconfirm {}'
        else:
            raise NotImplementedError()
        command = command_template.format(self.package)
        logger.info("Executing: {}".format(command))
        subprocess.check_call(command, shell=True, stderr=subprocess.STDOUT)

    def _pm_remove(self):
        if self.packagemanager == 'autodetect':
            current_distro = distro.identify()
            command_template = current_distro.command['package']['purge']
        elif self.packagemanager == 'apt':
            command_template = 'apt-get -y remove {}'
        elif self.packagemanager == 'pacman':
            command_template = 'pacman -Rs --noconfirm {}'
        else:
            raise NotImplementedError()

        command = command_template.format(self.package)
        logger.info("Executing: {}".format(command))
        subprocess.check_call(command, shell=True, stderr=subprocess.STDOUT)

    def lint(self):
        if self.ensure not in ['installed', 'removed']:
            raise InvalidParameterError('Ensure not in [installed, removed]')

    def verify(self):
        should_be_installed = self.ensure == 'installed'
        is_installed = self._pm_check()
        if is_installed != should_be_installed:
            if should_be_installed:
                return VerifyResult(self.identifier, success=False,
                                    message='Package {} is not installed but should be'.format(self.package))
            else:
                return VerifyResult(self.identifier, success=False,
                                    message="Package {} is installed but shouldn't be".format(self.package))
        else:
            return VerifyResult(self.identifier, success=True)

    def execute(self):
        verify_result = self.verify()

        if not verify_result.success:
            if self.ensure == 'installed':
                self._pm_install()
                return ExecutionResult("Installed package {}".format(self.package))
            else:
                self._pm_remove()
                return ExecutionResult("Removed package {}".format(self.package))
        return None
