from unittest import mock

import six

from motivation import commands

def test_jm():
	res = commands.jm(None, None, "#inane", None, "")
	assert isinstance(res, six.text_type)

def test_schneier():
	res = commands.schneier(None, None, "#inane", None, "foo")
	assert 'foo' in res

@mock.patch('requests.get',
	mock.Mock(
		return_value=mock.Mock(text='<p class="fact">How awesome is BRUCE SCHNEIER!</p>',
	)))
def test_schneier_all_caps():
	"At least one schneier fact features BRUCE SCHNEIER"
	res = commands.schneier(None, None, "#inane", None, "darwin")
	assert res == "How awesome is darwin!"

@mock.patch('requests.get',
	mock.Mock(
		return_value=mock.Mock(text='<p class="fact">How awesome is Bruce Schneier? Bruce Schneier!</p>',
	)))
def test_schneier_multi():
	"At least one schneier fact features the phrase twice"
	res = commands.schneier(None, None, "#inane", None, "darwin")
	assert res == "How awesome is darwin? darwin!"

@mock.patch('requests.get',
	mock.Mock(
		return_value=mock.Mock(text='<p class="fact">How awesome is BruceSchneier!</p>',
	)))
def test_schneier_no_space():
	"At least one fact contains BRUCESCHNEIER"
	res = commands.schneier(None, None, "#inane", None, "darwin")
	assert res == "How awesome is darwin!"

@mock.patch('requests.get',
	mock.Mock(
		return_value=mock.Mock(text='<p class="fact">How awesome is Schneier!</p>',
	)))
def test_schneier_no_bruce():
	"At least one fact contains only 'schneier'"
	res = commands.schneier(None, None, "#inane", None, "darwin")
	assert res == "How awesome is darwin!"

@mock.patch('requests.get',
	mock.Mock(
		return_value=mock.Mock(text='<p class="fact">How awesome is Bruce!</p>',
	)))
def test_schneier_no_schneier():
	"At least one fact contains only 'bruce'"
	res = commands.schneier(None, None, "#inane", None, "darwin")
	assert res == "How awesome is darwin!"
