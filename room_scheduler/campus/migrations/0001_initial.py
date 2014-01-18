# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attribute'
        db.create_table(u'campus_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'campus', ['Attribute'])

        # Adding model 'Room'
        db.create_table(u'campus_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('occupancy', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'campus', ['Room'])

        # Adding M2M table for field attributes on 'Room'
        m2m_table_name = db.shorten_name(u'campus_room_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm[u'campus.room'], null=False)),
            ('attribute', models.ForeignKey(orm[u'campus.attribute'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'attribute_id'])


    def backwards(self, orm):
        # Deleting model 'Attribute'
        db.delete_table(u'campus_attribute')

        # Deleting model 'Room'
        db.delete_table(u'campus_room')

        # Removing M2M table for field attributes on 'Room'
        db.delete_table(db.shorten_name(u'campus_room_attributes'))


    models = {
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

    complete_apps = ['campus']