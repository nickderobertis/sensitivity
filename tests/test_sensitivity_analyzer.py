import uuid

from pandas.testing import assert_frame_equal

from sensitivity import SensitivityAnalyzer
from tests.base import EXPECT_DF_TWO_VALUE, SENSITIVITY_VALUES_TWO_VALUE, add_5_to_values, RESULT_NAME, \
    SENSITIVITY_VALUES_THREE_VALUE, add_10_to_values, EXPECT_DF_THREE_VALUE, assert_styled_matches, \
    DF_STYLED_NUM_FMT_PATH, assert_graph_matches, PLOT_THREE_PATH, PLOT_OPTIONS_PATH, TWO_VALUE_LABELS, DF_LABELED_PATH


class TestSensitivityAnalyzer:

    def create_sa(self, **kwargs) -> SensitivityAnalyzer:
        sa_config = dict(
            sensitivity_values=SENSITIVITY_VALUES_TWO_VALUE,
            func=add_5_to_values,
            result_name=RESULT_NAME
        )
        sa_config.update(**kwargs)
        sa = SensitivityAnalyzer(**sa_config)
        return sa

    def test_create(self):
        sa = self.create_sa()

    def test_create_df(self):
        sa = self.create_sa()
        assert_frame_equal(sa.df, EXPECT_DF_TWO_VALUE, check_dtype=False)

    def test_create_df_three_values(self):
        sa = self.create_sa(
            sensitivity_values=SENSITIVITY_VALUES_THREE_VALUE,
            func=add_10_to_values,
        )
        assert_frame_equal(sa.df, EXPECT_DF_THREE_VALUE, check_dtype=False)

    def test_create_styled_dfs(self):
        sa = self.create_sa()
        result = sa.styled_dfs()
        assert_styled_matches(result)

    def test_create_styled_dfs_with_num_fmt(self):
        sa = self.create_sa(num_fmt='${:,.0f}')
        result = sa.styled_dfs()
        sa2 = self.create_sa()
        result2 = sa2.styled_dfs(num_fmt='${:,.0f}')
        assert_styled_matches(result, DF_STYLED_NUM_FMT_PATH)
        assert_styled_matches(result2, DF_STYLED_NUM_FMT_PATH)

    def test_create_styled_dfs_with_labels(self):
        sa = self.create_sa(labels=TWO_VALUE_LABELS)
        result = sa.styled_dfs()
        assert_styled_matches(result, DF_LABELED_PATH)

    def test_create_styled_dfs_three_values(self):
        sa = self.create_sa(
            sensitivity_values=SENSITIVITY_VALUES_THREE_VALUE,
            func=add_10_to_values,
        )
        result = sa.styled_dfs()

    def test_create_plot(self):
        sa = self.create_sa()
        result = sa.plot()
        assert_graph_matches(result)

    def test_create_plot_three_values(self):
        sa = self.create_sa(
            sensitivity_values=SENSITIVITY_VALUES_THREE_VALUE,
            func=add_10_to_values,
        )
        result = sa.plot()
        assert_graph_matches(result, file_path=PLOT_THREE_PATH)

    def test_create_plot_with_options(self):
        options = dict(
            grid_size=2, color_map='viridis', reverse_colors=True
        )
        sa = self.create_sa(labels=TWO_VALUE_LABELS, **options)
        result = sa.plot()
        assert_graph_matches(result, file_path=PLOT_OPTIONS_PATH)
        sa = self.create_sa(labels=TWO_VALUE_LABELS)
        result = sa.plot(**options)
        assert_graph_matches(result, file_path=PLOT_OPTIONS_PATH)
