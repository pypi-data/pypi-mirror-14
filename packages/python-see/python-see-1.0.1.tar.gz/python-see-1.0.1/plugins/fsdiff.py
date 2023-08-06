"""SEE libguestfs based File System Hooks.

They allow to gather disks' states checkpoints and analyse them.

Dependencies:

 * lxml (http://lxml.de)
 * pebble (https://pypi.python.org/pypi/Pebble)
 * python-guestfs (http://libguestfs.org)
 * hivex

"""

import os
import libvirt
from pebble import thread

from see import Hook

from utils import create_folder, launch_process, collect_process_output
from filesystem.disk import Disk
from filesystem.analysis import FileSystemAnalyser


QEMU_IMG = 'qemu-img'


class DiskCheckpointHook(Hook):
    """
    Disk snapshotting hook.

    On the given event, it takes a checkpoint of the disk's state.

    configuration::

        {
          "results_folder": "/folder/where/to/store/disk/checkpoints",
          "checkpoint_on_event": ["event_triggering_checkpoint"],
          "delete_checkpoints": false
        }

    The "checkpoint_on_event" can be either a string representing the event
    or a list of multiple ones.

    If "delete_checkpoints" is set to True, it will delete the disk checkpoints
    at the end of the execution. Default behaviour is to keep them.

    """
    SNAPSHOT_XML = """
    <domainsnapshot>
      <name>{0}</name>
      <description>{1}</description>
    </domainsnapshot>
    """

    def __init__(self, parameters):
        super().__init__(parameters)
        self.checkpoints = []
        self.disk = Disk(self.context, self.identifier)

        self.setup_handlers()

    def setup_handlers(self):
        if 'checkpoint_on_event' in self.configuration:
            configured_events = self.configuration['checkpoint_on_event']
            events = (isinstance(configured_events, str)
                      and [configured_events] or configured_events)

            for event in events:
                self.context.subscribe(event, self.disk_checkpoint)
                self.logger.debug("Disk checkpoint registered at %s event",
                                  event)

    def disk_checkpoint(self, event):
        self.logger.debug("Event %s: taking disk checkpoint.", event)

        disk_snapshot = self.disk_snapshot(event)
        disk_path = checkpoint_from_snapshot(
            self.disk, disk_snapshot, self.configuration['results_folder'])
        self.checkpoints.append(disk_path)

        self.logger.info("Disk checkpoint %s taken.", disk_path)

    def disk_snapshot(self, snapshot_name):
        snapshot_xml = self.SNAPSHOT_XML.format(snapshot_name,
                                                'Disk Checkpoint')

        return self.context.domain.snapshotCreateXML(
            snapshot_xml, libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY)

    def cleanup(self):
        if self.configuration.get('delete_checkpoints', False):
            for disk in self.checkpoints:
                os.remove(disk)


class FileSystemStateComparator(DiskCheckpointHook):
    """
    Compares a File System in two different moments.

    configuration::

        {
          "results_folder": "/folder/where/to/store/result/files",
          "compare_registries": False,
          "extract_new_files": False,
          "delete_checkpoints": False,
          "first_checkpoint_event": "event_at_which_taking_first_snapshot",
          "second_checkpoint_event": "event_at_which_taking_second_snapshot",
          "start_processing_on_event": "event_starting_async_processing",
          "wait_processing_on_event": "event_waiting_async_processing"
        }

    A report will be written in the results_folder.

    If extract_new_files is true, all new files found in the second checkpoint
    will be extracted in the results_folder.

    On start_processing_on_event, the analysis process will be started
    with the given configuration.
    wait_processing_on_event allows to wait for the analysis process
    to terminate.

    If compare_registries is True, the windows registry will be compared.

    If delete_checkpoints is set to True, the disk checkpoints will be deleted
    at the end of the execution. Default behaviour is to keep them.

    """
    def __init__(self, parameters):
        super().__init__(parameters)
        self.fsanalyser = FileSystemAnalyser(self.configuration, self.logger)

    def setup_handlers(self):
        if {'first_checkpoint_event',
            'second_checkpoint_event'} <= set(self.configuration):
            self.configuration['checkpoint_on_event'] = (
                self.configuration['first_checkpoint_event'],
                self.configuration['second_checkpoint_event'])

            super().setup_handlers()

        if {'start_processing_on_event',
            'stop_processing_on_event'} <= set(self.configuration):
            event = self.configuration['start_processing_on_event']
            self.context.subscribe(event, self.start_processing_handler)
            self.logger.debug("FileSystem analysis scheduled at %s event",
                              event)

            event = self.configuration['wait_processing_on_event']
            self.context.subscribe(event, self.stop_processing_handler)
            self.logger.debug("FileSystem analysis wait at %s event", event)

    def start_processing_handler(self, event):
        self.logger.debug("Event %s: start File System state comparison.",
                          event)

        self.fsanalyser.start_analysis(self.checkpoints[0], self.checkpoints[1])

    def stop_processing_handler(self, event):
        self.logger.debug(
            "Event %s: waiting for File System state comparison.", event)

        self.fsanalyser.wait_analysis_results()

        self.logger.info("File System state comparison concluded.")

    def cleanup(self):
        self.fsanalyser.cleanup()
        super().cleanup()


def checkpoint_from_snapshot(disk, snapshot, folder_path):
    """Turns a libvirt internal snapshot into a QCOW file."""
    create_folder(folder_path)

    name = snapshot.getName()
    path = os.path.join(folder_path, '%s.qcow2' % name)

    command = [QEMU_IMG, "convert", "-f", "qcow2", "-o",
               "backing_file=%s" % disk.backing_path,
               "-O", "qcow2", "-s", name, disk.path, path]

    process = launch_process(command)
    collect_process_output(process)

    return path
