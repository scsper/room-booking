# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'booking_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('setupTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('eventTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('teardownTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.Series'], null=True, blank=True)),
        ))
        db.send_create_signal(u'booking', ['Event'])

        # Adding M2M table for field attributes on 'Event'
        m2m_table_name = db.shorten_name(u'booking_event_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'booking.event'], null=False)),
            ('attribute', models.ForeignKey(orm[u'campus.attribute'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'attribute_id'])

        # Adding M2M table for field rooms on 'Event'
        m2m_table_name = db.shorten_name(u'booking_event_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'booking.event'], null=False)),
            ('room', models.ForeignKey(orm[u'campus.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'room_id'])

        # Adding model 'Series'
        db.create_table(u'booking_series', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('setupTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('eventTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('teardownTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'booking', ['Series'])

        # Adding M2M table for field attributes on 'Series'
        m2m_table_name = db.shorten_name(u'booking_series_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('series', models.ForeignKey(orm[u'booking.series'], null=False)),
            ('attribute', models.ForeignKey(orm[u'campus.attribute'], null=False))
        ))
        db.create_unique(m2m_table_name, ['series_id', 'attribute_id'])

        # Adding M2M table for field rooms on 'Series'
        m2m_table_name = db.shorten_name(u'booking_series_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('series', models.ForeignKey(orm[u'booking.series'], null=False)),
            ('room', models.ForeignKey(orm[u'campus.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['series_id', 'room_id'])

        # Adding model 'InfinitelyRecurring'
        db.create_table(u'booking_infinitelyrecurring', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.Series'], null=True, blank=True)),
            ('frequency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.Frequency'], null=True, blank=True)),
        ))
        db.send_create_signal(u'booking', ['InfinitelyRecurring'])

        # Adding model 'Frequency'
        db.create_table(u'booking_frequency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'booking', ['Frequency'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'booking_event')

        # Removing M2M table for field attributes on 'Event'
        db.delete_table(db.shorten_name(u'booking_event_attributes'))

        # Removing M2M table for field rooms on 'Event'
        db.delete_table(db.shorten_name(u'booking_event_rooms'))

        # Deleting model 'Series'
        db.delete_table(u'booking_series')

        # Removing M2M table for field attributes on 'Series'
        db.delete_table(db.shorten_name(u'booking_series_attributes'))

        # Removing M2M table for field rooms on 'Series'
        db.delete_table(db.shorten_name(u'booking_series_rooms'))

        # Deleting model 'InfinitelyRecurring'
        db.delete_table(u'booking_infinitelyrecurring')

        # Deleting model 'Frequency'
        db.delete_table(u'booking_frequency')


    models = {
        u'booking.event': {
            'Meta': {'object_name': 'Event'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['campus.Attribute']", 'symmetrical': 'False'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            'eventTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['campus.Room']", 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.Series']", 'null': 'True', 'blank': 'True'}),
            'setupTime': ('django.db.models.fields.DateTimeField', [], {}),
            'teardownTime': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'booking.frequency': {
            'Meta': {'object_name': 'Frequency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'booking.infinitelyrecurring': {
            'Meta': {'object_name': 'InfinitelyRecurring'},
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.Frequency']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.Series']", 'null': 'True', 'blank': 'True'})
        },
        u'booking.series': {
            'Meta': {'object_name': 'Series'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['campus.Attribute']", 'null': 'True', 'blank': 'True'}),
            'endTime': ('django.db.models.fields.DateTimeField', [], {}),
            'eventTime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['campus.Room']", 'null': 'True', 'blank': 'True'}),
            'setupTime': ('django.db.models.fields.DateTimeField', [], {}),
            'teardownTime': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'campus.attribute': {
            'Meta': {'object_name': 'Attribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'campus.room': {
            'Meta': {'object_name': 'Room'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['campus.Attribute']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'occupancy': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['booking']