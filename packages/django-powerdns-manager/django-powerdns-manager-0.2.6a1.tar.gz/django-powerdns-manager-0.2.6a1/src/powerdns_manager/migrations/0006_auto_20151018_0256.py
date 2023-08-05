# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerdns_manager', '0005_auto_20150311_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='modified_at',
            field=models.PositiveIntegerField(help_text=b'Timestamp for the last modification time.', verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='last_check',
            field=models.PositiveIntegerField(help_text=b'Last time this domain was checked for freshness.', null=True, verbose_name='last check'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='notified_serial',
            field=models.PositiveIntegerField(help_text=b'The last notified serial of a master domain. This is updated from the SOA record of the domain.', null=True, verbose_name='notified serial'),
        ),
        migrations.AlterField(
            model_name='dynamiczone',
            name='domain',
            field=models.OneToOneField(related_name='powerdns_manager_dynamiczone_domain', verbose_name='domain', to='powerdns_manager.Domain', help_text='Select the domain, the A and AAAA records of which might be updated dynamically over HTTP.'),
        ),
        migrations.AlterField(
            model_name='record',
            name='change_date',
            field=models.PositiveIntegerField(help_text=b'Timestamp for the last update. This is used by PowerDNS internally.', null=True, verbose_name='change date'),
        ),
        migrations.AlterField(
            model_name='record',
            name='prio',
            field=models.PositiveIntegerField(help_text=b'For MX records, this should be the priority of the mail exchanger specified.', null=True, verbose_name='priority'),
        ),
        migrations.AlterField(
            model_name='record',
            name='ttl',
            field=models.PositiveIntegerField(help_text=b'How long the DNS-client are allowed to remember this record. Also known as Time To Live(TTL) This value is in seconds.', null=True, verbose_name='TTL', blank=True),
        ),
    ]
