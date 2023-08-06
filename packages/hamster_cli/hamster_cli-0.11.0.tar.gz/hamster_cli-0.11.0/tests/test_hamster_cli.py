# -*- coding: utf-8 -*-

import datetime
import logging
import os

import hamsterlib
import pytest
from click import ClickException
from freezegun import freeze_time

from hamster_cli import hamster_cli

try:
    from configparser import SafeConfigParser
except:
    from ConfigParser import SafeConfigParser


class TestSearch(object):
    """Unit tests for search command."""

    @freeze_time('2015-12-12 18:00')
    def test_search(self, controler, mocker, fact, search_parameter_parametrized):
        """Ensure that your search parameters get passed on to the apropiate backend function."""
        search_term, time_range, expectation = search_parameter_parametrized
        controler.facts.get_all = mocker.MagicMock(return_value=[fact])
        hamster_cli._search(controler, search_term, time_range)
        controler.facts.get_all.assert_called_with(**expectation)


class TestStart(object):
    """Unit test related to starting a new fact."""

    @pytest.mark.parametrize(('raw_fact', 'start', 'end', 'expectation'), [
        ('foo@bar', '2015-12-12 13:00', '2015-12-12 16:30', {
            'activity': 'foo',
            'category': 'bar',
            'start': datetime.datetime(2015, 12, 12, 13, 0, 0),
            'end': datetime.datetime(2015, 12, 12, 16, 30, 0),
        }),
        ('10:00-18:00 foo@bar', '2015-12-12 13:00', '', {
            'activity': 'foo',
            'category': 'bar',
            'start': datetime.datetime(2015, 12, 12, 13, 0, 0),
            'end': datetime.datetime(2015, 12, 25, 18, 00, 0),
        }),
        # 'ongoing fact's
        ('foo@bar', '2015-12-12 13:00', '', {
            'activity': 'foo',
            'category': 'bar',
            'start': datetime.datetime(2015, 12, 12, 13, 0, 0),
            'end': None,
        }),
        ('11:00 foo@bar', '2015-12-12 13:00', '', {
            'activity': 'foo',
            'category': 'bar',
            'start': datetime.datetime(2015, 12, 12, 13, 0, 0),
            'end': None,
        }),
    ])
    @freeze_time('2015-12-25 18:00')
    def test_start_add_new_fact(self, controler_with_logging, mocker, raw_fact,
            start, end, expectation):
        """
        Test that inpul validation and assignment of start/endtime works is done as expected.
        """
        controler = controler_with_logging
        controler.facts.save = mocker.MagicMock()
        hamster_cli._start(controler, raw_fact, start, end)
        assert controler.facts.save.called
        args, kwargs = controler.facts.save.call_args
        fact = args[0]
        assert fact.start == expectation['start']
        assert fact.end == expectation['end']
        assert fact.activity.name == expectation['activity']
        assert fact.category.name == expectation['category']


class TestStop(object):
    """Unit test concerning the stop command."""

    def test_stop_existing_tmp_fact(self, tmp_fact, controler_with_logging, mocker):
        """Make sure stoping an ongoing fact works as intended."""
        controler_with_logging.facts.stop_tmp_fact = mocker.MagicMock()
        hamster_cli._stop(controler_with_logging)
        assert controler_with_logging.facts.stop_tmp_fact.called

    def test_stop_no_existing_tmp_fact(self, controler_with_logging, capsys):
        """Make sure that stop without actually an ongoing fact leads to an error."""
        controler = controler_with_logging
        with pytest.raises(ClickException):
            hamster_cli._stop(controler)
            out, err = capsys.readouterr()
            assert 'Unable to continue' in err


class TestCancel():
    """Unit tests related to cancelation of an ongoing fact."""

    def test_cancel_existing_tmp_fact(self, tmp_fact, controler_with_logging, mocker,
            capsys):
        """Test cancelation in case there is an ongoing fact."""
        controler = controler_with_logging
        controler.facts.cancel_tmp_fact = mocker.MagicMock(return_value=None)
        hamster_cli._cancel(controler)
        out, err = capsys.readouterr()
        assert controler.facts.cancel_tmp_fact.called
        assert 'canceled' in out

    def test_cancel_no_existing_tmp_fact(self, controler_with_logging, capsys):
        """Test cancelation in case there is no actual ongoing fact."""
        with pytest.raises(ClickException):
            hamster_cli._cancel(controler_with_logging)
            out, err = capsys.readouterr()
            assert 'Nothing tracked right now' in err


class TestExport():
    """Unittests related to data export."""
    @pytest.mark.parametrize('format', ['ical', 'html'])
    def test_invalid_format(self, controler_with_logging, format, mocker):
        """Make sure that passing an invalid format exits prematurely."""
        controler = controler_with_logging
        with pytest.raises(ClickException):
            hamster_cli._export(controler, format, None, None)

    def test_valid_format(self, controler, controler_with_logging, tmpdir, mocker):
        """Make sure that a valid format returns the apropiate writer class."""
        path = os.path.join(tmpdir.mkdir('report').strpath, 'report.csv')
        hamsterlib.reports.TSVWriter = mocker.MagicMock(return_value=hamsterlib.reports.TSVWriter(
            path))
        hamster_cli._export(controler, 'csv', None, None)
        assert hamsterlib.reports.TSVWriter.called


class TestCategories():
    """Unittest related to category listings."""

    def test_categories(self, controler_with_logging, category, mocker, capsys):
        """Make sure the categories get displayed to the user."""
        controler = controler_with_logging
        controler.categories.get_all = mocker.MagicMock(return_value=[category])
        hamster_cli._categories(controler)
        out, err = capsys.readouterr()
        assert category.name in out
        assert controler.categories.get_all.called


class TestCurrent():
    """Unittest for dealing with 'ongoing facts'."""

    def test_tmp_fact(self, controler, tmp_fact, controler_with_logging, capsys, fact, mocker):
        """Make sure the current fact is displayed if there is one."""
        controler = controler_with_logging
        controler.facts.get_tmp_fact = mocker.MagicMock(return_value=fact)
        hamster_cli._current(controler)
        out, err = capsys.readouterr()
        assert controler.facts.get_tmp_fact
        assert str(fact) in out

    def test_no_tmp_fact(self, controler_with_logging, capsys):
        """Make sure we display proper feedback if there is no current 'ongoing fact."""
        controler = controler_with_logging
        with pytest.raises(ClickException):
            hamster_cli._current(controler)
            out, err = capsys.readouterr()
            assert 'There seems no be no activity beeing tracked right now' in err


class TestActivities():
    def test_activities_no_category(self, controler, activity, mocker, capsys):
        activity.category = None
        controler.activities.get_all = mocker.MagicMock(
            return_value=[activity])
        mocker.patch('hamster_cli.hamster_cli.tabulate')
        hamster_cli.tabulate = mocker.MagicMock(
            return_value='{}, {}'.format(activity.name, None))
        hamster_cli._activities(controler, '')
        out, err = capsys.readouterr()
        assert activity.name in out
        hamster_cli.tabulate.call_args[0] == [(activity.name, None)]

    def test_activities_with_category(self, controler, activity, mocker,
            capsys):
        controler.activities.get_all = mocker.MagicMock(
            return_value=[activity])
        hamster_cli._activities(controler, '')
        out, err = capsys.readouterr()
        assert activity.name in out
        assert activity.category.name in out

    def test_activities_with_search_term(self, controler, activity, mocker,
            capsys):
        """Make sure the search term is passed on."""
        controler.activities.get_all = mocker.MagicMock(
            return_value=[activity])
        hamster_cli._activities(controler, 'foobar')
        out, err = capsys.readouterr()
        assert controler.activities.get_all.called
        controler.activities.get_all.assert_called_with(search_term='foobar')
        assert activity.name in out
        assert activity.category.name in out


class TestSetupLogging():
    def test_setup_logging(self, controler, client_config, lib_config):
        hamster_cli._setup_logging(controler)
        assert controler.lib_logger.level == (
            controler.client_config['log_level'])
        assert controler.client_logger.level == (
            controler.client_config['log_level'])

    def test_setup_logging_log_console_True(self, controler):
        controler.client_config['log_console'] = True
        hamster_cli._setup_logging(controler)
        assert isinstance(controler.client_logger.handlers[0],
            logging.StreamHandler)
        assert isinstance(controler.lib_logger.handlers[0],
            logging.StreamHandler)
        assert controler.client_logger.handlers[0].formatter

    def test_setup_logging_log_console_False(self, controler):
        hamster_cli._setup_logging(controler)
        assert controler.lib_logger.handlers == []
        assert controler.client_logger.handlers == []

    def test_setup_logging_log_file_True(self, controler, appdirs):
        controler.client_config['logfile_path'] = os.path.join(appdirs.user_log_dir, 'foobar.log')
        hamster_cli._setup_logging(controler)
        assert isinstance(controler.lib_logger.handlers[0],
            logging.FileHandler)
        assert isinstance(controler.client_logger.handlers[0],
            logging.FileHandler)

    def test_setup_logging_log_file_False(self, controler):
        hamster_cli._setup_logging(controler)
        assert controler.lib_logger.handlers == []
        assert controler.client_logger.handlers == []


class TestLaunchWindow(object):
    pass


class TestGetConfig(object):
    @pytest.mark.parametrize('log_level', ['debug'])
    def test_log_levels_valid(self, log_level, config_instance):
        backend, client = hamster_cli._get_config(
            config_instance(log_level=log_level))
        assert client['log_level'] == 10

    @pytest.mark.parametrize('log_level', ['foobar'])
    def test_log_levels_invalid(self, log_level, config_instance):
        with pytest.raises(ValueError):
            backend, client = hamster_cli._get_config(
                config_instance(log_level=log_level))

    @pytest.mark.parametrize('day_start', ['05:00:00'])
    def test_daystart_valid(self, config_instance, day_start):
        backend, client = hamster_cli._get_config(config_instance(
            daystart=day_start))
        assert backend['day_start'] == datetime.datetime.strptime(
            '05:00:00', '%H:%M:%S').time()

    @pytest.mark.parametrize('day_start', ['foobar'])
    def test_daystart_invalid(self, config_instance, day_start):
        with pytest.raises(ValueError):
            backend, client = hamster_cli._get_config(
                config_instance(daystart=day_start))


class TestGetConfigInstance():
    def test_no_file_present(self, appdirs, mocker):
        """Make sure a new vanilla config is written if no config is found."""
        mocker.patch('hamster_cli.hamster_cli._write_config_file')
        hamster_cli._get_config_instance()
        assert hamster_cli._write_config_file.called

    def test_file_present(self, config_instance, config_file, mocker):
        """Make sure we try parsing a found config file."""
        result = hamster_cli._get_config_instance()
        assert result.get('Backend', 'store') == config_instance().get('Backend', 'store')

    def test_get_config_path(self, appdirs, mocker):
        """Make sure the config target path is constructed to our expectations."""
        mocker.patch('hamster_cli.hamster_cli._write_config_file')
        hamster_cli._get_config_instance()
        expectation = os.path.join(appdirs.user_config_dir, 'hamster_cli.conf')
        assert hamster_cli._write_config_file.called_with(expectation)


class TestGenerateTable(object):
    def test_generate_table(self, fact):
        """Make sure the table contains all expected fact data."""
        table, header = hamster_cli._generate_facts_table([fact])
        assert table[0].start == fact.start.strftime('%Y-%m-%d %H:%M')
        assert table[0].activity == fact.activity.name

    def test_header(self):
        """Make sure the tables header matches our expectation."""
        table, header = hamster_cli._generate_facts_table([])
        assert len(header) == 6


class TestWriteConfigFile(object):
    def test_file_is_written(request, filepath):
        """Make sure the file is written. Content is not checked, this is ConfigParsers job."""
        hamster_cli._write_config_file(filepath)
        assert os.path.lexists(filepath)

    def test_return_config_instance(request, filepath):
        """Make sure we return a ``SafeConfigParser`` instance."""
        result = hamster_cli._write_config_file(filepath)
        assert isinstance(result, SafeConfigParser)

    def test_non_existing_path(request, tmpdir, filename):
        """Make sure that the path-parents are created ifnot present."""
        filepath = os.path.join(tmpdir.strpath, 'foobar')
        assert os.path.lexists(filepath) is False
        hamster_cli._write_config_file(filepath)
        assert os.path.lexists(filepath)


class TestHamsterAppDirs(object):
    """Make sure that our custom AppDirs works as intended."""

    def test_user_data_dir_returns_directoy(self, tmpdir, mocker):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_data_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        assert appdir.user_data_dir == path

    @pytest.mark.parametrize('create', [True, False])
    def test_user_data_dir_creates_file(self, tmpdir, mocker, create, faker):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}/'.format(faker.word()))
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_data_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        appdir.create = create
        assert os.path.exists(appdir.user_data_dir) is create

    def test_site_data_dir_returns_directoy(self, tmpdir, mocker):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        mocker.patch('hamster_cli.hamster_cli.appdirs.site_data_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        assert appdir.site_data_dir == path

    @pytest.mark.parametrize('create', [True, False])
    def test_site_data_dir_creates_file(self, tmpdir, mocker, create, faker):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}/'.format(faker.word()))
        mocker.patch('hamster_cli.hamster_cli.appdirs.site_data_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        appdir.create = create
        assert os.path.exists(appdir.site_data_dir) is create

    def test_user_config_dir_returns_directoy(self, tmpdir, mocker):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_config_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        assert appdir.user_config_dir == path

    @pytest.mark.parametrize('create', [True, False])
    def test_user_config_dir_creates_file(self, tmpdir, mocker, create, faker):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}/'.format(faker.word()))
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_config_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        appdir.create = create
        assert os.path.exists(appdir.user_config_dir) is create

    def test_site_config_dir_returns_directoy(self, tmpdir, mocker):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        mocker.patch('hamster_cli.hamster_cli.appdirs.site_config_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        assert appdir.site_config_dir == path

    @pytest.mark.parametrize('create', [True, False])
    def test_site_config_dir_creates_file(self, tmpdir, mocker, create, faker):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}/'.format(faker.word()))
        mocker.patch('hamster_cli.hamster_cli.appdirs.site_config_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        appdir.create = create
        assert os.path.exists(appdir.site_config_dir) is create

    def test_user_cache_dir_returns_directoy(self, tmpdir, mocker):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_cache_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        assert appdir.user_cache_dir == path

    @pytest.mark.parametrize('create', [True, False])
    def test_user_cache_dir_creates_file(self, tmpdir, mocker, create, faker):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}/'.format(faker.word()))
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_cache_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        appdir.create = create
        assert os.path.exists(appdir.user_cache_dir) is create

    def test_user_log_dir_returns_directoy(self, tmpdir, mocker):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_log_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        assert appdir.user_log_dir == path

    @pytest.mark.parametrize('create', [True, False])
    def test_user_log_dir_creates_file(self, tmpdir, mocker, create, faker):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}/'.format(faker.word()))
        mocker.patch('hamster_cli.hamster_cli.appdirs.user_log_dir', return_value=path)
        appdir = hamster_cli.HamsterAppDirs('hamster_cli')
        appdir.create = create
        assert os.path.exists(appdir.user_log_dir) is create
