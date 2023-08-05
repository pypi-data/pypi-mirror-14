# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

# Allow everything in there to access the DB
pytestmark = pytest.mark.django_db

import copy
from django.core.urlresolvers import reverse
from django.conf import settings
import json
import logging
from rest_framework import status


from .fixtures import live_server, client, user, site
from .util import (
    assert_created, assert_error, assert_success, assert_deleted, load_json,
    Client, load, filter_networks, make_mac, TestSite, get_result
)


log = logging.getLogger(__name__)


def test_network_bug_issues_34(client, site):
    """Test set queries for Networks."""
    # URIs
    attr_uri = site.list_uri('attribute')
    net_uri = site.list_uri('network')

    # Pre-load the attributes
    client.post(attr_uri, data=load('attributes.json'))

    # Populate the network objects and retreive them for testing.
    client.post(net_uri, data=load('networks.json'))
    net_resp = client.retrieve(net_uri)
    networks = get_result(net_resp)

    # Filter networks w/ attribute hostname=foo-bar1, excluding IPs
    wanted = ['192.168.0.0/24', '192.168.0.0/25']
    expected = filter_networks(networks, wanted)

    assert_success(
        client.retrieve(
            net_uri, attributes='hostname=foo-bar1', include_ips=False
        ),
        expected
    )

    # Filter networks w/ attribute hostname=foo-bar1, including IPs
    wanted = ['192.168.0.1/32', '192.168.0.0/24', '192.168.0.0/25']
    expected = filter_networks(networks, wanted)

    assert_success(
        client.retrieve(
            net_uri, attributes='hostname=foo-bar1'
        ),
        expected
    )


def test_mac_address_bug_issues_111(client, site):
    """Test that a MAC coming in as an integer is properly formatted."""
    # Make sure that none of them ever match wrong.
    mac_int = 122191241314
    mac_str = '122191241314'
    mac_expected = '00:1c:73:2a:60:62'
    mac_wrong = '12:21:91:24:13:14'

    dev_uri = site.list_uri('device')
    ifc_uri = site.list_uri('interface')

    dev_resp = client.create(dev_uri, hostname='foo-bar1')
    dev = get_result(dev_resp)

    # Create the interface w/ an integer
    ifc_resp = client.create(
        ifc_uri, device=dev['id'], name='eth0', parent_id=None,
        mac_address=mac_int
    )
    ifc = get_result(ifc_resp)
    ifc_obj_uri = site.detail_uri('interface', id=ifc['id'])

    # Test that integer matches expected
    assert make_mac(ifc['mac_address']) == mac_expected

    # Update the interface w/ a string integer
    updated = copy.deepcopy(ifc)
    updated_resp = client.put(ifc_obj_uri, data=json.dumps(updated))
    expected = get_result(updated_resp)

    # Test that string integer matches expectd
    assert make_mac(expected['mac_address']) == mac_expected

    # And for completeness, make sure that a formatted string still comes back
    # the same.
    updated['mac_address'] = mac_expected
    updated_resp = client.put(ifc_obj_uri, data=json.dumps(updated))
    expected = get_result(updated_resp)

    # Test that expected matches expected
    assert make_mac(expected['mac_address']) == mac_expected


def test_options_bug_issues_126(client, site):
    """
    Test that OPTIONS query returns a 200 OK and has content.

    Ref: https://github.com/dropbox/nsot/issues/126
    """
    net_uri = site.list_uri('network')

    opts_resp = client.options(net_uri)

    # Assert 200 OK
    assert opts_resp.status_code == 200

    # Assert payload is a thing.
    expected = [u'actions', u'description', u'name', u'parses', u'renders']
    assert sorted(opts_resp.json()) == expected


def test_duplicate_400_issues_142(client, site):
    """
    Test that creating duplicate objects results in a 400.

    Ref: https://github.com/dropbox/nsot/issues/142
    """
    dev_uri = site.list_uri('device')
    net_uri = site.list_uri('network')

    # Device is created.
    client.create(dev_uri, hostname='foo-bar1')

    # Device duplicate fails.
    assert_error(
        client.create(dev_uri, hostname='foo-bar1'),
        status.HTTP_400_BAD_REQUEST
    )

    # Network is created.
    client.create(net_uri, cidr='10.0.0.0/8')

    # Network duplicate fails.
    assert_error(
        client.create(net_uri, cidr='10.0.0.0/8'),
        status.HTTP_400_BAD_REQUEST
    )


def test_natural_lookup_without_site(client, site):
    """
    Test that when retrieving objects by natural_key, that uniqueness is
    guaranteed. Since all uniqueness constraints are by Site, we could in
    theory have objects across multiple sites w/ the same natural_key value.

    - You've got multiple sites and an object w/ the same natural_key in
      different Sites. For example: Device 'foo-bar1' in Site 1 and Device
      'foo-bar1' in Site 2.
    - You're not using a site-specific end-point (e.g. /api/devices/ vs.
      /api/sites/1/devices/).
    """
    site1 = site  # For comparison against site2

    # Top-level URIs (e.g. /api/:resource_name/)
    site_uri = reverse('site-list')
    net_uri = reverse('network-list')
    dev_uri = reverse('device-list')

    # Create 2nd site
    site2_resp = client.create(site_uri, name='Test Site 2')
    site2 = TestSite(site2_resp.json())

    ###########
    # Devices #
    ###########
    hostname = 'foo-bar1'
    site1_dev_uri = site1.list_uri('device')
    site2_dev_uri = site2.list_uri('device')

    # Create a Device in each site w/ the same hostname
    client.create(site1_dev_uri, hostname=hostname)
    client.create(site2_dev_uri, hostname=hostname)

    # Site-specific: GOOD
    site1_dev_detail_uri = site1.detail_uri('device', id=hostname)
    site2_dev_detail_uri = site2.detail_uri('device', id=hostname)
    dev1_resp = client.get(site1_dev_detail_uri)
    dev2_resp = client.get(site2_dev_detail_uri)
    assert dev1_resp.status_code == 200
    assert dev2_resp.status_code == 200

    # Top-level: BAD
    root_dev_detail_uri = reverse('device-detail', args=(hostname,))
    assert_error(
        client.get(root_dev_detail_uri),
        status.HTTP_400_BAD_REQUEST
    )

    ############
    # Networks #
    ############
    cidr = '10.0.0.0/8'
    site1_net_uri = site1.list_uri('network')
    site2_net_uri = site2.list_uri('network')

    # Create a Network in each site w/ the same cidr
    client.create(site1_net_uri, cidr=cidr)
    client.create(site2_net_uri, cidr=cidr)

    # Site-specific: GOOD
    site1_net_detail_uri = site1.detail_uri('network', id=cidr)
    site2_net_detail_uri = site2.detail_uri('network', id=cidr)
    net1_resp = client.get(site1_net_detail_uri)
    net2_resp = client.get(site2_net_detail_uri)
    assert net1_resp.status_code == 200
    assert net2_resp.status_code == 200

    # Top-level: BAD
    root_net_detail_uri = reverse('network-detail', args=(cidr,))
    assert_error(
        client.get(root_net_detail_uri),
        status.HTTP_400_BAD_REQUEST
    )
