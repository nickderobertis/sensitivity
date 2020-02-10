from pandas.testing import assert_frame_equal

from sensitivity import SensitivityAnalyzer
from tests.base import EXPECT_DF, SENSITIVITY_VALUES, add_5_to_values, RESULT_NAME


class TestSensitivityAnalyzer:

    def create_sa(self, **kwargs) -> SensitivityAnalyzer:
        sa_config = dict(
            sensitivity_values=SENSITIVITY_VALUES,
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
        assert_frame_equal(sa.df, EXPECT_DF, check_dtype=False)

    def test_create_styled_df(self):
        sa = self.create_sa()
        sa.styled_df
        # TODO: determine how to test pandas Styler object beyond creation without error

    def test_create_plot(self):
        sa = self.create_sa()
        sa.plot
        # TODO: determine how to test matplotlib figures beyond creation without error
