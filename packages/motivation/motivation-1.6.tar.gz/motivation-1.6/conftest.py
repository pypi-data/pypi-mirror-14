from unittest import mock


def pytest_configure(config):
	# mock the pmxbot imports
	pmxbot = mock.MagicMock()
	pmxbot.core = mock.MagicMock(command=mock.Mock(return_value=lambda func:func))
	pmxbot.karma = mock.MagicMock()

	config.patcher = mock.patch.dict('sys.modules', {
		'pmxbot': pmxbot,
		'pmxbot.core': pmxbot.core,
		'pmxbot.karma': pmxbot.karma,
	})
	config.patcher.__enter__()

def pytest_unconfigure(config):
	config.patcher.__exit__(None, None, None)
