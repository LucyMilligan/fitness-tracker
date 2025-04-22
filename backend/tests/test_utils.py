from common.utils import (
    calculate_pace_mins_per_km,
    calculate_speed_km_per_hr, 
    calculate_time_secs, 
    convert_pace_to_float,
    convert_date_to_dt_format,
    format_query_output,
    update_activities_dict
)


class TestCalculateTimeSecs:
    def test_calculate_time_secs_just_secs(self):
        moving_time = "00:00:40"
        expected = 40
        result = calculate_time_secs(moving_time)
        assert result == expected

    def test_calculate_time_secs_munites_and_secs(self):
        moving_time = "00:02:30"
        expected = 150
        result = calculate_time_secs(moving_time)
        assert result == expected

    def test_calculate_time_secs_hours_munites_and_secs(self):
        moving_time = "01:01:30"
        expected = 3690
        result = calculate_time_secs(moving_time)
        assert result == expected


class TestCalculatePace:
    def test_calculate_pace_min_per_km_30_mins(self):
        moving_time = "00:30:00"
        distance = 5.0
        expected = "6:00"
        result = calculate_pace_mins_per_km(distance, moving_time)
        assert result == expected

    def test_calculate_pace_min_per_km_33_mins(self):
        moving_time = "00:33:00"
        distance = 5.0
        expected = "6:36"
        result = calculate_pace_mins_per_km(distance, moving_time)
        assert result == expected

    def test_calculate_pace_min_per_km_greater_than_10_mins_per_km(self):
        moving_time = "02:15:30"
        distance = 5.0
        expected = "27:06"
        result = calculate_pace_mins_per_km(distance, moving_time)
        assert result == expected


class TestConvertPaceToFloat:
    def test_convert_pace_to_float(self):
        pace_string = "6:53"
        result = convert_pace_to_float(pace_string)
        assert result == 6.88


class TestConvertDateToDtFormat:
    def test_convert_date_to_dt_format(self):
        pace_string = "2025/03/25"
        result = convert_date_to_dt_format(pace_string)
        assert result == "2025-03-25T00:00:00.000Z"


class TestCalculateSpeed:
    def test_calculate_speed_km_per_hr_basic(self):
        moving_time = "01:00:00"
        distance = 20.0
        result = calculate_speed_km_per_hr(distance, moving_time)
        assert result == 20.00

    def test_calculate_speed_km_per_hr_to_2_dp(self):
        moving_time = "00:35:00"
        distance = 7.5
        result = calculate_speed_km_per_hr(distance, moving_time)
        assert result == 12.86


class TestUpdateActivitiesDict:
    def test_update_activities_dict_single_dict(self):
        activities = [
            {
                "activity": "run",
                "time": "20:16",
                "date": "2025/03/25",
                "moving_time": "00:49:21",
                "distance_km": 7.16
            }
        ]
        expected = [
            {
                "activity": "run",
                "time": "20:16",
                "date": "2025/03/25",
                "moving_time": "00:49:21",
                "distance_km": 7.16,
                "pace_str_mps": "6:53",
                "pace_float_mps": 6.88,
                "speed_kmphr": 8.71,
                "formatted_time": "2025-03-25T00:00:00.000Z"
            }
        ]
        result = update_activities_dict(activities)
        assert result == expected

    def test_update_activities_dict_multiple_dicts(self):
        activities = [
            {
                "activity": "run",
                "time": "10:10",
                "date": "2025/04/25",
                "moving_time": "01:00:00",
                "distance_km": 10.0
            },
            {
                "activity": "run",
                "time": "20:16",
                "date": "2025/03/25",
                "moving_time": "00:49:21",
                "distance_km": 7.16
            }
        ]
        expected = [
            {
                "activity": "run",
                "time": "10:10",
                "date": "2025/04/25",
                "moving_time": "01:00:00",
                "distance_km": 10.0,
                "pace_str_mps": "6:00",
                "pace_float_mps": 6.00,
                "speed_kmphr": 10.00,
                "formatted_time": "2025-04-25T00:00:00.000Z"
            },
            {
                "activity": "run",
                "time": "20:16",
                "date": "2025/03/25",
                "moving_time": "00:49:21",
                "distance_km": 7.16,
                "pace_str_mps": "6:53",
                "pace_float_mps": 6.88,
                "speed_kmphr": 8.71,
                "formatted_time": "2025-03-25T00:00:00.000Z"
            }
        ]
        result = update_activities_dict(activities)
        assert len(result) == len(activities)
        assert result == expected


class TestFormatQueryOutput:
    def test_format_query_output_single_row(self):
        data = [("test1", "test2", "test3")]
        col_names = ["col1", "col2", "col3"]
        result = format_query_output(data, col_names)
        assert result == [{"col1": "test1", "col2": "test2", "col3": "test3"}]

    def test_format_query_output_multiple_rows(self):
        data = [("test1", "test2"), ("test3", "test4")]
        col_names = ["col1", "col2"]
        result = format_query_output(data, col_names)
        assert result == [
            {"col1": "test1", "col2": "test2"},
            {"col1": "test3", "col2": "test4"},
        ]
