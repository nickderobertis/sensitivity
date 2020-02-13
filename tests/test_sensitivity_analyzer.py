from pandas.testing import assert_frame_equal

from sensitivity import SensitivityAnalyzer
from tests.base import EXPECT_DF_TWO_VALUE, SENSITIVITY_VALUES_TWO_VALUE, add_5_to_values, RESULT_NAME, \
    SENSITIVITY_VALUES_THREE_VALUE, add_10_to_values, EXPECT_DF_THREE_VALUE


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
        # TODO [#1]: determine how to test pandas Styler object beyond creation without error

    def test_create_styled_dfs_three_values(self):
        sa = self.create_sa(
            sensitivity_values=SENSITIVITY_VALUES_THREE_VALUE,
            func=add_10_to_values,
        )
        result = sa.styled_dfs()

    def test_create_plot(self):
        sa = self.create_sa()
        result = sa.plot()
        # TODO [#2]: determine how to test matplotlib figures beyond creation without error

    def test_create_plot_three_values(self):
        sa = self.create_sa(
            sensitivity_values=SENSITIVITY_VALUES_THREE_VALUE,
            func=add_10_to_values,
        )
        result = sa.plot()
