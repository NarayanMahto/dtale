import mock
import pytest
from six import PY3

if PY3:
    from contextlib import ExitStack
else:
    from contextlib2 import ExitStack


@pytest.mark.unit
def test_build_file(test_data, state_data, scattergeo_data, builtin_pkg, unittest):
    from dtale import offline_chart

    if PY3:
        from unittest.mock import mock_open
    else:
        from mock import mock_open

    with ExitStack() as stack:
        stack.enter_context(
            mock.patch("dtale.views.in_ipython_frontend", mock.Mock(return_value=False))
        )
        stack.enter_context(mock.patch("dtale.views.open", mock_open()))

        output = offline_chart(
            test_data, chart_type="bar", x="date", y="foo", agg="sum"
        )
        assert output is not None
        output = offline_chart(
            test_data, chart_type="bar", x="date", y="foo", agg="sum", filepath="foo"
        )
        assert output is None
        output = offline_chart(
            test_data,
            chart_type="bar",
            x="date",
            y="foo",
            agg="sum",
            filepath="foo.html",
        )
        assert output is None
        output = offline_chart(
            state_data,
            chart_type="maps",
            map_type="choropleth",
            loc_mode="USA-states",
            loc="Code",
            map_val="val",
        )
        assert output is not None
        output = offline_chart(
            scattergeo_data,
            chart_type="maps",
            map_type="scattergeo",
            lat="lat",
            lon="lon",
            map_val="val",
            scope="world",
            proj="mercator",
        )
        assert output is not None


@pytest.mark.unit
def test_build_notebook(test_data, unittest):
    from dtale import offline_chart

    with ExitStack() as stack:
        stack.enter_context(
            mock.patch("dtale.views.in_ipython_frontend", mock.Mock(return_value=True))
        )
        output = offline_chart(
            test_data, chart_type="bar", x="date", y="foo", agg="sum"
        )
        assert output is None
