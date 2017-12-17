# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('core_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['auth.User'], unique=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('country_alpha2', self.gf(
                'django.db.models.fields.CharField')(max_length=2)),
            ('b_day', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('b_month', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('b_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('activ_token', self.gf('django.db.models.fields.CharField')(
                max_length=64, null=True)),
            ('forgot_token', self.gf('django.db.models.fields.CharField')(
                max_length=64, null=True)),
            ('req_limit', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('core', ['UserProfile'])

        # Adding model 'UserStatus'
        db.create_table('core_userstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.UserProfile'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('updated_date', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('core', ['UserStatus'])

        # Adding model 'Photo'
        db.create_table('core_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(
                default='', max_length=64)),
            ('created_time', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('updated_time', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('marked_delete', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Photo'])

        # Adding model 'Image'
        db.create_table('core_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Photo'])),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('size_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('is_avail', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Image'])

        # Adding model 'Location'
        db.create_table('core_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lon', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('street', self.gf('django.db.models.fields.CharField')(
                max_length=64, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(
                max_length=64, null=True)),
            ('country', self.gf('django.db.models.fields.CharField')(
                max_length=64, null=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(
                max_length=16, null=True)),
            ('res_lat', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('res_lon', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('res_type', self.gf('django.db.models.fields.CharField')(
                max_length=64, null=True)),
        ))
        db.send_create_signal('core', ['Location'])

        # Adding model 'Request'
        db.create_table('core_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['auth.User'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Location'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('resource', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('submitted_date', self.gf(
                'django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('core', ['Request'])

        # Adding model 'PhotoRequest'
        db.create_table('core_photorequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Photo'])),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Request'])),
        ))
        db.send_create_signal('core', ['PhotoRequest'])

        # Adding model 'RequestStatus'
        db.create_table('core_requeststatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['core.Request'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['auth.User'], null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('comment', self.gf('django.db.models.fields.CharField')(
                max_length=140, null=True)),
            ('submitted_date', self.gf(
                'django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('core', ['RequestStatus'])

    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('core_userprofile')

        # Deleting model 'UserStatus'
        db.delete_table('core_userstatus')

        # Deleting model 'Photo'
        db.delete_table('core_photo')

        # Deleting model 'Image'
        db.delete_table('core_image')

        # Deleting model 'Location'
        db.delete_table('core_location')

        # Deleting model 'Request'
        db.delete_table('core_request')

        # Deleting model 'PhotoRequest'
        db.delete_table('core_photorequest')

        # Deleting model 'RequestStatus'
        db.delete_table('core_requeststatus')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'size_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'core.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lon': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'res_lat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'res_lon': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'res_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'core.photo': {
            'Meta': {'object_name': 'Photo'},
            'created_time': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marked_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'updated_time': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.photorequest': {
            'Meta': {'object_name': 'PhotoRequest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']"}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Request']"})
        },
        'core.request': {
            'Meta': {'object_name': 'Request'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Location']"}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Photo']", 'null': 'True', 'through': "orm['core.PhotoRequest']", 'symmetrical': 'False'}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'submitted_date': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'core.requeststatus': {
            'Meta': {'object_name': 'RequestStatus'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Request']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'submitted_date': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'core.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activ_token': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'b_day': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'b_month': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'b_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'country_alpha2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'forgot_token': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'req_limit': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'core.userstatus': {
            'Meta': {'object_name': 'UserStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'updated_date': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.UserProfile']"})
        }
    }

    complete_apps = ['core']
