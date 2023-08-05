# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models
import otree.models.varsmixin


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedGroupWaitPage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('session_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('group_pk', otree.db.models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedSubsessionWaitPage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('session_pk', otree.db.models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalSingleton',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('admin_access_code', otree.db.models.RandomCharField(max_length=8, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSize',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_label', otree.db.models.CharField(max_length=300, null=True)),
                ('subsession_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('group_index', otree.db.models.PositiveIntegerField(null=True)),
                ('group_size', otree.db.models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PageCompletion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('app_name', otree.db.models.CharField(max_length=300, null=True)),
                ('page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('page_name', otree.db.models.CharField(max_length=300, null=True)),
                ('time_stamp', otree.db.models.PositiveIntegerField(null=True)),
                ('seconds_on_page', otree.db.models.PositiveIntegerField(null=True)),
                ('subsession_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('participant_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('session_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('auto_submitted', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
            ],
        ),
        migrations.CreateModel(
            name='PageTimeout',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('participant_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('expiration_time', otree.db.models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('vars', otree.db.models.JSONField(default=dict, null=True)),
                ('exclude_from_data_analysis', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('time_started', otree.db.models.DateTimeField(null=True)),
                ('mturk_assignment_id', otree.db.models.CharField(max_length=50, null=True)),
                ('mturk_worker_id', otree.db.models.CharField(max_length=50, null=True)),
                ('start_order', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('label', otree.db.models.CharField(max_length=50, null=True)),
                ('_index_in_subsessions', otree.db.models.PositiveIntegerField(default=0, null=True)),
                ('_index_in_pages', otree.db.models.PositiveIntegerField(default=0, null=True, db_index=True)),
                ('id_in_session', otree.db.models.PositiveIntegerField(null=True)),
                ('_waiting_for_ids', otree.db.models.CharField(max_length=300, null=True)),
                ('code', otree.db.models.RandomCharField(max_length=8, blank=True, db_index=True)),
                ('last_request_succeeded', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], verbose_name='Health of last server request')),
                ('visited', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, db_index=True)),
                ('ip_address', otree.db.models.GenericIPAddressField(null=True)),
                ('_last_page_timestamp', otree.db.models.PositiveIntegerField(null=True)),
                ('_last_request_timestamp', otree.db.models.PositiveIntegerField(null=True)),
                ('is_on_wait_page', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_current_page_name', otree.db.models.CharField(max_length=200, verbose_name='page', null=True)),
                ('_current_app_name', otree.db.models.CharField(max_length=200, verbose_name='app', null=True)),
                ('_round_number', otree.db.models.PositiveIntegerField(null=True)),
                ('_current_form_page_url', otree.db.models.URLField(null=True)),
                ('_max_page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('_is_auto_playing', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=(otree.models.varsmixin._SaveTheChangeWithCustomFieldSupport, models.Model),
        ),
        migrations.CreateModel(
            name='ParticipantLockModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('participant_code', otree.db.models.CharField(max_length=10, null=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantToPlayerLookup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('participant_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('app_name', otree.db.models.CharField(max_length=300, null=True)),
                ('player_pk', otree.db.models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('vars', otree.db.models.JSONField(default=dict, null=True)),
                ('config', otree.db.models.JSONField(default=dict, null=True)),
                ('label', otree.db.models.CharField(help_text='For internal record-keeping', blank=True, null=True, max_length=300)),
                ('experimenter_name', otree.db.models.CharField(help_text='For internal record-keeping', blank=True, null=True, max_length=300)),
                ('code', otree.db.models.RandomCharField(max_length=8, blank=True, db_index=True)),
                ('time_scheduled', otree.db.models.DateTimeField(help_text='For internal record-keeping', blank=True, null=True)),
                ('time_started', otree.db.models.DateTimeField(null=True)),
                ('mturk_HITId', otree.db.models.CharField(help_text='Hit id for this session on MTurk', blank=True, null=True, max_length=300)),
                ('mturk_HITGroupId', otree.db.models.CharField(help_text='Hit id for this session on MTurk', blank=True, null=True, max_length=300)),
                ('mturk_qualification_type_id', otree.db.models.CharField(help_text='Qualification type that is assigned to each worker taking hit', blank=True, null=True, max_length=300)),
                ('mturk_num_participants', otree.db.models.IntegerField(help_text='Number of participants on MTurk', default=-1, null=True)),
                ('mturk_sandbox', otree.db.models.BooleanField(help_text='Should this session be created in mturk sandbox?', choices=[(True, 'Yes'), (False, 'No')], default=True)),
                ('archived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, db_index=True)),
                ('git_commit_timestamp', otree.db.models.CharField(max_length=200, null=True)),
                ('comment', otree.db.models.TextField(blank=True, null=True)),
                ('_ready_to_play', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_anonymous_code', otree.db.models.RandomCharField(max_length=8, blank=True)),
                ('special_category', otree.db.models.CharField(max_length=20, null=True, db_index=True)),
                ('demo_already_used', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, db_index=True)),
                ('ready', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_pre_create_id', otree.db.models.CharField(max_length=300, null=True, db_index=True)),
            ],
            options={
                'ordering': ['pk'],
            },
            bases=(otree.models.varsmixin._SaveTheChangeWithCustomFieldSupport, models.Model),
        ),
        migrations.CreateModel(
            name='StubModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='WaitPageVisit',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('session_pk', otree.db.models.PositiveIntegerField(null=True)),
                ('page_index', otree.db.models.PositiveIntegerField(null=True)),
                ('id_in_session', otree.db.models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.AlterIndexTogether(
            name='waitpagevisit',
            index_together=set([('session_pk', 'page_index', 'id_in_session')]),
        ),
        migrations.AlterIndexTogether(
            name='participanttoplayerlookup',
            index_together=set([('participant_pk', 'page_index')]),
        ),
        migrations.AddField(
            model_name='participant',
            name='session',
            field=otree.db.models.ForeignKey(to='otree.Session'),
        ),
        migrations.AlterIndexTogether(
            name='pagetimeout',
            index_together=set([('participant_pk', 'page_index')]),
        ),
        migrations.AlterIndexTogether(
            name='groupsize',
            index_together=set([('app_label', 'subsession_pk')]),
        ),
        migrations.AddField(
            model_name='globalsingleton',
            name='default_session',
            field=otree.db.models.ForeignKey(null=True, blank=True, to='otree.Session'),
        ),
        migrations.AlterIndexTogether(
            name='completedsubsessionwaitpage',
            index_together=set([('page_index', 'session_pk')]),
        ),
        migrations.AlterIndexTogether(
            name='completedgroupwaitpage',
            index_together=set([('page_index', 'session_pk', 'group_pk')]),
        ),
        migrations.AlterIndexTogether(
            name='participant',
            index_together=set([('session', 'mturk_worker_id', 'mturk_assignment_id')]),
        ),
    ]
