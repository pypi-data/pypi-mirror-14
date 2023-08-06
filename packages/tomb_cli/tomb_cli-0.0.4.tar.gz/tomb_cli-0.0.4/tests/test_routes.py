import pytest
import os
from click.testing import CliRunner
here = os.path.dirname(__file__)
test_app_path = os.path.join(here, 'apps')


@pytest.mark.integration
def test_basic_routes():
    from tomb_cli.main import cli
    runner = CliRunner()
    ini_path = os.path.join(test_app_path, 'development.ini')

    result = runner.invoke(
        cli, ['-c', ini_path, 'routes']
    )

    expected_output = """Name                       Pattern                 View                                                        Method
-----------------------    --------------------    --------------------------------------------------------    ----------------
__static/                  /static/*subpath        tomb_cli_testapps:static/                                   *
__static2/                 /static2/*subpath       /var/www/static/                                            *
__pdt_images/              /pdt_images/*subpath    pyramid_debugtoolbar:static/img/                            *
a                          /                       <unknown>                                                   *
no_view_attached           /                       <unknown>                                                   *
route_and_view_attached    /                       tomb_cli_testapps.standard_views.route_and_view_attached    *
only_post_on_route         /route                  tomb_cli_testapps.standard_views.route_and_view_attached    POST
only_post_on_view          /view                   tomb_cli_testapps.standard_views.route_and_view_attached    POST
method_intersection        /intersection           tomb_cli_testapps.standard_views.route_and_view_attached    POST
method_conflicts           /conflicts              tomb_cli_testapps.standard_views.route_and_view_attached    <route mismatch>
multiview                  /multiview              tomb_cli_testapps.standard_views.route_and_view_attached    PATCH,GET
multiview                  /multiview              tomb_cli_testapps.standard_views.hello_world                POST
class_based_view           /classes                tomb_cli_testapps.standard_views.ClassBasedView             POST
factory                    /factory                tomb_cli_testapps.standard_views.route_and_view_attached    *
not_post                   /not_post               tomb_cli_testapps.standard_views.route_and_view_attached    !POST
not_post_only_get          /not_post_only_get      tomb_cli_testapps.standard_views.route_and_view_attached    <route mismatch>
permission_on_view         /permission_on_view     tomb_cli_testapps.standard_views.route_and_view_attached    *
"""  # noqa
    assert result.exit_code == 0
    final_lines = result.output.split('\n')
    expected_lines = expected_output.split('\n')

    error_msg = "We expect to have the same set of routes"
    assert len(final_lines) == len(expected_lines), error_msg

    for line_index, line in enumerate(expected_lines):
        columns = final_lines[line_index].strip().split()
        for col_index, column in enumerate(line.strip().split()):
            # Skip the separator
            if '-------' in column:
                continue

            assert column.strip() == columns[col_index].strip(), line
