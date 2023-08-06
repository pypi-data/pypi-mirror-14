import pytest
import os

here = os.path.dirname(__file__)


@pytest.mark.unit
def test_loading_simple_yaml():
    from tomb_cli.config import load_yaml

    result = load_yaml(os.path.join(here, './fixtures/logging.yaml'))
    assert result['handlers']['console']['class'] == 'logging.StreamHandler'


@pytest.mark.unit
def test_including_yaml():
    from tomb_cli.config import load_yaml
    result = load_yaml(os.path.join(here, './fixtures/server.yaml'))
    assert result['handlers']['console']['class'] == 'logging.StreamHandler'
    baz = result['foo']['bar']['baz']
    assert baz['handlers']['console']['class'] == 'logging.StreamHandler'


@pytest.mark.unit
def test_including_bad_yaml():
    from tomb_cli.config import load_yaml
    import yaml

    with pytest.raises(yaml.constructor.ConstructorError):
        load_yaml(os.path.join(here, './fixtures/bad_include.yaml'))


@pytest.mark.unit
def test_verify_vars_exist(monkeypatch):
    from tomb_cli.config import load_yaml

    monkeypatch.setenv('ANSVC_DB_URL', 'sqlite://:memory:')
    monkeypatch.setenv('MAIN_DB_USER', 'sontek')
    monkeypatch.setenv('MAIN_DB_PASSWORD', 'is awesome')
    monkeypatch.setenv('DB_1234', 'sm_AccountsNew')

    result = load_yaml(os.path.join(here, './fixtures/env_vars.yaml'))

    assert result['smlib']['smsqlalchemy']['url'] == 'sqlite://:memory:'
    expected = 'sontek:is awesome/sm_AccountsNew'
    assert result['smlib']['mongodb']['url'] == expected


@pytest.mark.unit
def test_verify_env_vars_dont_exist(monkeypatch):
    from tomb_cli.config import MissingEnvironmentKeys
    from tomb_cli.config import load_yaml

    monkeypatch.setenv('ANSVC_DB_URL', 'sqlite://:memory:')

    with pytest.raises(MissingEnvironmentKeys) as e:
        load_yaml(os.path.join(here, './fixtures/env_vars.yaml'))

    assert str(e.value) == 'missing environment variables: DB_1234, MAIN_DB_PASSWORD, MAIN_DB_USER'  # noqa


@pytest.mark.unit
def test_verify_env_var_directive_dont_exist(monkeypatch):
    from tomb_cli.config import MissingEnvironmentKey
    from tomb_cli.config import load_yaml

    monkeypatch.setenv('MAIN_DB_USER', 'sontek')
    monkeypatch.setenv('MAIN_DB_PASSWORD', 'is awesome')
    monkeypatch.setenv('DB_1234', 'sm_AccountsNew')

    with pytest.raises(MissingEnvironmentKey) as e:
        load_yaml(os.path.join(here, './fixtures/env_vars.yaml'))

    assert str(e.value) == 'missing environment variable: ANSVC_DB_URL'


@pytest.mark.unit
def test_bad_env_directive_type():
    from tomb_cli.config import load_yaml
    from yaml.constructor import ConstructorError

    with pytest.raises(ConstructorError) as e:
        load_yaml(
            os.path.join(here, './fixtures/bad_env_var_directive.yaml')
        )

    assert str(e.value) == 'Unrecognized node type in !env statement'
