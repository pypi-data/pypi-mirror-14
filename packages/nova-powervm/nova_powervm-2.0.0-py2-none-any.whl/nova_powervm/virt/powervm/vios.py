# Copyright 2015, 2016 IBM Corp.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging

from pypowervm import const as pvm_const
from pypowervm.utils import transaction as pvm_tx
from pypowervm.wrappers import base_partition as pvm_bp
from pypowervm.wrappers import managed_system as pvm_ms
from pypowervm.wrappers import virtual_io_server as pvm_vios


LOG = logging.getLogger(__name__)

# RMC must be either active or busy.  Busy is allowed because that simply
# means that something is running against the VIOS at the moment...but
# it should recover shortly.
VALID_RMC_STATES = [pvm_bp.RMCState.ACTIVE, pvm_bp.RMCState.BUSY]

# Only a running state is OK for now.
VALID_VM_STATES = [pvm_bp.LPARState.RUNNING]


def get_active_vioses(adapter, host_uuid, xag=None):
    """Returns a list of active Virtual I/O Server Wrappers for a host.

    Active is defined by powered on and RMC state being 'active'.

    :param adapter: The pypowervm adapter for the query.
    :param host_uuid: The host servers UUID.
    :param xag: Optional list of extended attributes to use.  If not passed
                in defaults to None.
    :return: List of VIOS wrappers.
    """
    vio_feed_resp = adapter.read(pvm_ms.System.schema_type, root_id=host_uuid,
                                 child_type=pvm_vios.VIOS.schema_type,
                                 xag=xag)
    wrappers = pvm_vios.VIOS.wrap(vio_feed_resp)
    return [vio for vio in wrappers if is_vios_active(vio)]


def is_vios_active(vios):
    """Returns a boolean to indicate if the VIOS is active.

    Active is defined by running, and the RMC being 'active'.
    :param vios: The Virtual I/O Server wrapper to validate.
    :return: Boolean
    """
    return (vios.rmc_state in VALID_RMC_STATES and
            vios.state in VALID_VM_STATES)


def get_physical_wwpns(adapter, ms_uuid):
    """Returns the active WWPNs of the FC ports across all VIOSes on system."""
    resp = adapter.read(pvm_ms.System.schema_type, root_id=ms_uuid,
                        child_type=pvm_vios.VIOS.schema_type,
                        xag=[pvm_const.XAG.VIO_STOR])
    vios_feed = pvm_vios.VIOS.wrap(resp)
    wwpn_list = []
    for vios in vios_feed:
        wwpn_list.extend(vios.get_active_pfc_wwpns())
    return wwpn_list


def build_tx_feed_task(adapter, host_uuid, name='vio_feed_mgr',
                       xag=[pvm_const.XAG.VIO_STOR,
                            pvm_const.XAG.VIO_SMAP,
                            pvm_const.XAG.VIO_FMAP]):
    """Builds the pypowervm transaction FeedTask.

    The transaction FeedTask enables users to collect a set of
    'WrapperTasks' against a feed of entities (in this case a set of VIOSes).
    The WrapperTask (within the FeedTask) handles lock and retry.

    This is useful to batch together a set of updates across a feed of elements
    (and multiple updates within a given wrapper).  This allows for significant
    performance improvements.

    :param adapter: The pypowervm adapter for the query.
    :param host_uuid: The host server's UUID.
    :param name: (Optional) The name of the feed manager.  Defaults to
                 vio_feed_mgr.
    :param xag: (Optional) List of extended attributes to use.  If not passed
                in defaults to all storage options (as this is most common
                case for using a transaction manager).
    """
    return pvm_tx.FeedTask(name,
                           get_active_vioses(adapter, host_uuid, xag=xag))
