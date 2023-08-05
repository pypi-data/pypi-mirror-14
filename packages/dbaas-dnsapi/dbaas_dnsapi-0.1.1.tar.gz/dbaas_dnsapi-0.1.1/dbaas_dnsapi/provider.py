# -*- coding: utf-8 -*-

from client import DNSAPI
from models import DatabaseInfraDNSList
from django.db import transaction
import string
import random
import logging

LOG = logging.getLogger(__name__)


class DNSAPIProvider(object):

    @classmethod
    def create_dns(self, dnsapi, name, ip, domain):

        LOG.info('Create dns %s.%s to IP %s' % (name, domain, ip))
        domain_id = dnsapi.get_domain_id_by_name(domain=domain)
        if domain_id is None:
            LOG.error('Domain %s not found!' % domain)
            return None

        record_id = dnsapi.get_record_by_name(name=name, domain_id=domain_id)

        cont = 0
        while record_id:
            LOG.warning('DNS %s.%s alredy exists!' % (name, domain))
            name = '%s%s' % (name, random.choice(string.letters))
            record_id = dnsapi.get_record_by_name(
                name=name, domain_id=domain_id)
            if cont > 10:
                LOG.error(
                    'Could not create dns %s.%s, it already exists!' % (name, domain))
                return None
            cont += 1

        dnsapi.create_record(name=name, content=ip, domain_id=domain_id)

        dns = '%s.%s' % (name, domain)
        LOG.info('DNS %s successfully created.' % dns)
        return dns

    @classmethod
    def delete_dns(self, dnsapi, name, ip, domain):

        dns = '%s.%s' % (name, domain)
        LOG.info('Delete dns %s' % (dns))

        domain_id = dnsapi.get_domain_id_by_name(domain=domain)
        if domain_id is None:
            LOG.error('Domain %s not found!' % domain)
            return None

        dnsapi.delete_record_by_name(host_name=name, ip=ip, domain=domain)
        LOG.info('DNS %s successfully deleted.' % dns)

        return True

    @classmethod
    @transaction.commit_on_success
    def create_database_dns(self, databaseinfra):

        dnsapi = DNSAPI(environment=databaseinfra.environment)

        for databaseinfradnslist in DatabaseInfraDNSList.objects.filter(databaseinfra=databaseinfra.id):
            dns = self.create_dns(dnsapi=dnsapi, name=databaseinfradnslist.name,
                                  ip=databaseinfradnslist.ip, domain=databaseinfradnslist.domain)
            if dns:
                databaseinfradnslist.dns = dns
                databaseinfradnslist.save()

        dnsapi.export(now=False)

    @classmethod
    @transaction.commit_on_success
    def remove_database_dns(self, environment, databaseinfraid):

        dnsapi = DNSAPI(environment=environment)

        for databaseinfradnslist in DatabaseInfraDNSList.objects.filter(databaseinfra=databaseinfraid):
            name = databaseinfradnslist.dns.split('.' + databaseinfradnslist.domain)[0]
            ret = self.delete_dns(dnsapi=dnsapi,
                                  name=name,
                                  ip=databaseinfradnslist.ip,
                                  domain=databaseinfradnslist.domain)
            if ret:
                databaseinfradnslist.delete()

        dnsapi.export(now=False)

    @classmethod
    @transaction.commit_on_success
    def update_database_dns_ttl(self, databaseinfra, ttl):

        dnsapi = DNSAPI(environment=databaseinfra.environment)

        for databaseinfradnslist in DatabaseInfraDNSList.objects.filter(databaseinfra=databaseinfra.id):
            name = databaseinfradnslist.dns.split(
                '.' + databaseinfradnslist.domain)[0]
            self.update_dns_ttl(
                dnsapi=dnsapi, name=name, domain=databaseinfradnslist.domain, ttl=ttl)

    @classmethod
    def update_dns_ttl(self, dnsapi, name, domain, ttl):

        dns = '%s.%s' % (name, domain)
        LOG.info('Updating dns %s ttl to %s' % (dns, str(ttl)))

        domain_id = dnsapi.get_domain_id_by_name(domain=domain)
        if domain_id is None:
            LOG.error('Domain %s not found!' % domain)
            return None

        record_id = dnsapi.get_record_by_name(name=name, domain_id=domain_id)
        record = dnsapi.get_record(record_id)
        dnsapi.update_record_ttl(
            record_id=record_id, name=record['name'], content=record['content'], ttl=ttl)

        LOG.info('DNS %s successfully updated.' % dns)

        return True

    @classmethod
    @transaction.commit_on_success
    def update_database_dns_content(self, databaseinfra, dns, old_ip, new_ip):

        dnsapi = DNSAPI(environment=databaseinfra.environment)

        for databaseinfradnslist in DatabaseInfraDNSList.objects.filter(databaseinfra=databaseinfra.id, dns=dns, ip=old_ip):
            name = databaseinfradnslist.dns.split(
                '.' + databaseinfradnslist.domain)[0]
            databaseinfradnslist.ip = new_ip
            databaseinfradnslist.save()
            self.update_dns_content(
                dnsapi=dnsapi, name=name, domain=databaseinfradnslist.domain, newcontent=new_ip)

    @classmethod
    def update_dns_content(self, dnsapi, name, domain, newcontent):

        dns = '%s.%s' % (name, domain)
        LOG.info('Updating dns %s content to %s' % (dns, str(newcontent)))

        domain_id = dnsapi.get_domain_id_by_name(domain=domain)
        if domain_id is None:
            LOG.error('Domain %s not found!' % domain)
            return None

        record_id = dnsapi.get_record_by_name(name=name, domain_id=domain_id)
        record = dnsapi.get_record(record_id)
        dnsapi.update_record(
            record_id=record_id, name=record['name'], content=newcontent)

        LOG.info('DNS %s successfully updated.' % dns)

        return True
